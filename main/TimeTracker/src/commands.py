from .database import Database
from .log import Log


def nargs(argc):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Assuming the first argument is always the list we want to check
            if len(args) != argc:
                Log.error(
                    f"invalid number of arguments (expected {argc}, received {len(args)})"
                )
                exit(1)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class Commands:

    @staticmethod
    def run_command(command, args):
        if hasattr(Commands, command) and callable(getattr(Commands, command)):
            getattr(Commands, command)(*args)
        else:
            Log.error("no such command")

    @staticmethod
    @nargs(0)
    def help(*args):
        Log.info("Available commands: new, spend, total, details, list, delete")

    @staticmethod
    @nargs(1)
    def new(*args):
        Database.new(args[0])

    @staticmethod
    @nargs(2)
    def spend(*args):
        Database.spend(args[0], args[1])

    @staticmethod
    @nargs(1)
    def total(*args):
        Database.total(args[0])

    @staticmethod
    @nargs(1)
    def details(*args):
        Database.details(args[0])

    @staticmethod
    @nargs(1)
    def delete(*args):
        Database.delete(args[0])

    @staticmethod
    @nargs(0)
    def list(*args):
        Database.list()
