from random import randint, random

import attr
import csv
import json

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
    last_oiled = attr.ib(type=str)  # timestamp
    last_homed = attr.ib(type=str)  # timestamp
    update_timestamp = attr.ib(type=str)  # timestamp
    peak_temperature = attr.ib(type=str)  # cm/s
    failure_description = attr.ib(type=str, default=FailureDescription.NONE)


if __name__ == "__main__":
    motors = [i for i in range(1, 16)]
    rows = []

    for i in range(1000):
        speed = randint(1, 3600)
        temp = (speed / 300) * random()

        last_oiled = ""  # todo: tolerances
        last_homed = ""  # todo: timestamps
        update_timestamp = ""
        motor_id = 0  # todo: ids

        failure_desc = FailureDescription.NONE
        ran = randint(0, 20)
        if temp >= 40:
            failure_desc = FailureDescription.OVERHEAT
        elif ran == 3:
            failure_desc = FailureDescription.CONTAMINATED
        elif temp > 60 or last_oiled > 10:
            failure_desc = FailureDescription.SEIZE
        elif last_homed > 80:
            failure_desc = FailureDescription.RESISTANCE
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

    with open("names.csv", "w", newline="") as csvfile:
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

        for row in rows:
            writer.writerow(json.load(row))
