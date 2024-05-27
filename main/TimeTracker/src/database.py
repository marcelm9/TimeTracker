import os
import re
import time

from .config import DB_PATH
from .log import Log


def now():
    return time.strftime("%Y %m %d %H %M %S")


def get_path(name):
    return os.path.join(DB_PATH, name)


class Database:

    @staticmethod
    def __get_all_tracker_names():
        return [f.name for f in os.scandir(DB_PATH) if not f.name == "__init__.py"]

    @staticmethod
    def __parse_time_input(time_input):
        # Check if the string is in a valid format
        pattern = re.compile(r"^-?\d+h\d+m$|^-?\d+h$|^-?\d+m$")
        if not pattern.match(time_input):
            Log.error(f"invalid time-input: {time_input}")
            exit(1)

        is_negative = time_input.startswith("-")

        # Remove the negative sign for easier processing if present
        if is_negative:
            time_input = time_input[1:]

        # Initialize total minutes
        total_minutes = 0

        # Regex to extract hours and minutes
        hours_pattern = re.compile(r"(\d+)h")
        minutes_pattern = re.compile(r"(\d+)m")

        hours_match = hours_pattern.search(time_input)
        minutes_match = minutes_pattern.search(time_input)

        if hours_match:
            hours = int(hours_match.group(1))
            total_minutes += hours * 60

        if minutes_match:
            minutes = int(minutes_match.group(1))
            total_minutes += minutes

        # Apply negative sign if the original string was negative
        if is_negative:
            total_minutes = -total_minutes

        return total_minutes

    @staticmethod
    def new(name):
        path = get_path(name)
        if os.path.exists(path):
            Log.error(f"Tracker with name '{name}' already exists")
            exit(1)
        with open(path, "w") as f:
            f.write(now() + " | created\n")
        Log.info(f"Created new tracker '{name}'")

    @staticmethod
    def spend(name, time_input):
        if name not in Database.__get_all_tracker_names():
            Log.error(f"No tracker with name '{name}' found")
            exit(1)

        m = Database.__parse_time_input(time_input)

        path = get_path(name)
        with open(path, "a") as f:
            f.write(f"{now()} | {m}m\n")

        h = int(m / 60)
        if h == 0:
            Log.info(f"Tracking {m}m for {name}")
        else:
            m = m % 60
            if m == 0:
                Log.info(f"Tracking {h}h for {name}")
            else:
                Log.info(f"Tracking {h}h {m}m for {name}")

    @staticmethod
    def delete(name):
        if name not in Database.__get_all_tracker_names():
            Log.error(f"No tracker with name '{name}' found")
            exit(1)

        if (
            Log.input(f"Do you really want to delete tracker '{name}'? (y/n) ").lower()
            == "y"
        ):
            os.remove(get_path(name))
            Log.info(f"Removed tracker '{name}'")
        else:
            Log.error("Aborting")

    @staticmethod
    def total(name):
        if name not in Database.__get_all_tracker_names():
            Log.error(f"No tracker with name '{name}' found")
            exit(1)

        with open(get_path(name), "r") as f:
            lines = f.readlines()

        del lines[0]  # removes the "created at" line

        m = sum([int(line.split("|")[1].strip().removesuffix("m")) for line in lines])

        h = int(m / 60)
        if h == 0:
            Log.info(f"Total time spent on '{name}': {m}m")
        else:
            m = m % 60
            if m == 0:
                Log.info(f"Total time spent on '{name}': {h}h")
            else:
                Log.info(f"Total time spent on '{name}': {h}h {m}m")
