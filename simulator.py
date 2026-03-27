"""Local IoT device simulator for Neura Connect."""

import random


def generate_sensor_reading() -> dict:
    return {"temperature_c": round(random.uniform(20.0, 35.0), 2)}


if __name__ == "__main__":
    print(generate_sensor_reading())
