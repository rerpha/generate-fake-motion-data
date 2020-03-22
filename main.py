from random import randint, random

import attr
import csv
import datetime

# goal - predict remaining useful lifetime(RUL) for motors used in beamline motion axis


class FailureDescription:
    NONE = ""
    OVERHEAT = "OVERHEATED"
    SEIZE = "SEIZED"
    DERAIL = "DERAILED"
    CORROSION = "CORRODED"
    CONTAMINATED = "CONTAMINATION"
    RESISTANCE = "RESISTANCE"


@attr.s
class Row:
    update_id = attr.ib(type=int)
    motor_id = attr.ib(type=int)
    peak_speed = attr.ib(type=int)  # rpm
    last_oiled = attr.ib(type=float)  # timestamp
    last_homed = attr.ib(type=float)  # timestamp
    update_timestamp = attr.ib(type=int)  # timestamp
    peak_temperature = attr.ib(type=float)  # cm/s
    failure_description = attr.ib(type=str, default=FailureDescription.NONE)


if __name__ == "__main__":
    motors = [i for i in range(1, 16)]
    rows = []

    timestamp = (
        datetime.datetime(2014, 11, 22, 14, 42, 21, 34435, tzinfo=datetime.timezone.utc)
        - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    ).total_seconds()

    last_oiled = (
        datetime.datetime(2014, 10, 21, 14, 00, 00, 22261, tzinfo=datetime.timezone.utc)
        - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    ).total_seconds()

    for i in range(100000):
        speed = randint(1, 3600)
        temp = round((speed / 30) * random(), 2)

        update_timestamp = timestamp
        last_homed = int(timestamp - randint(0, 20000))
        motor_id = 0  # todo: ids

        failure_desc = FailureDescription.NONE
        ran = randint(0, 20)
        if temp >= 90 and last_oiled > 10:
            failure_desc = FailureDescription.SEIZE
        elif last_oiled < 10:
            failure_desc = FailureDescription.CORROSION
        elif temp >= 80:
            failure_desc = FailureDescription.OVERHEAT
        elif last_homed < update_timestamp - 16000:
            failure_desc = FailureDescription.RESISTANCE
        elif ran == 3:
            failure_desc = FailureDescription.CONTAMINATED
        elif ran == 2:
            failure_desc = FailureDescription.DERAIL

        rows.append(
            Row(
                i,
                motor_id,
                speed,
                last_oiled,
                last_homed,
                update_timestamp,
                temp,
                failure_desc,
            )
        )
        timestamp += float(0.5)

    with open("sensors.csv", "w", newline="") as csvfile:
        fieldnames = [
            "update_id",
            "motor_id",
            "peak_speed",
            "last_oiled",
            "last_homed",
            "update_timestamp",
            "peak_temperature",
            "failure_description",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(attr.asdict(row))
