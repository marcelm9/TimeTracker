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
        return [f.name for f in os.scandir(DB_PATH) if f.name not in  ("__init__.py", "__pycache__")]

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
    def __format_h_m(m):
        h = int(m / 60)
        if h == 0:
            return f"{m}m"
        else:
            m = m % 60
            if m == 0:
                return f"{h}h"
            else:
                return f"{h}h {m}m"

    @staticmethod
    def new(name):
        if "." in name:
            Log.error("Periods are not allowed in tracker names")
            exit(1)
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

        Log.info(f"Tracking {Database.__format_h_m(m)} for '{name}'")

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
    def total(name: str):
        if "." in name:
            if not (name.count(".") == 1 and name[-1] == "."):
                Log.error(
                    "When using category syntax, the period can only be the last character"
                )
                exit(1)

            names = Database.__get_all_tracker_names()

            filtered_names = [n for n in names if n.startswith(name[:-1])]
            if len(filtered_names) == 0:
                Log.info(f"No trackers matched '{name}'")
                exit(1)
            else:
                total_m = 0
                for n in filtered_names:
                    with open(get_path(n), "r") as f:
                        total_m += sum(
                            [
                                int(line.split("|")[1].strip().removesuffix("m"))
                                for line in f.readlines()[1:]
                            ]
                        )
                Log.info(
                    f"Total time spend on category '{name[:-1]}' in {len(filtered_names)} trackers: {Database.__format_h_m(total_m)}"
                )

        else:
            if name not in Database.__get_all_tracker_names():
                Log.error(f"No tracker with name '{name}' found")
                exit(1)

            with open(get_path(name), "r") as f:
                lines = f.readlines()

            del lines[0]  # removes the "created at" line

            m = sum(
                [int(line.split("|")[1].strip().removesuffix("m")) for line in lines]
            )

            Log.info(f"Total time spent on '{name}': {Database.__format_h_m(m)}")

    @staticmethod
    def details(name):
        if name not in Database.__get_all_tracker_names():
            Log.error(f"No tracker with name '{name}' found")
            exit(1)

        with open(get_path(name), "r") as f:
            lines = f.readlines()

        Log.info(f"Details for '{name}'")
        print("YYYY MM DD HH MM SS")
        print(lines[0], end="")
        del lines[0]

        minutes = [int(line.split("|")[1].strip().removesuffix("m")) for line in lines]

        for l, m in zip(lines, minutes):
            print(l.split("|")[0] + "| " + Database.__format_h_m(m))

    @staticmethod
    def list():
        names = Database.__get_all_tracker_names()
        if len(names) == 0:
            Log.info("No trackers found")
        else:
            Log.info("Trackers:")
            for name in names:
                print(name)
