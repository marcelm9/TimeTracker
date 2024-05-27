from rich import print

class Log:

    @staticmethod
    def info(msg: str):
        print(f"\[[purple]TimeTracker[/]]\[[green]info[/]] {msg}")

    @staticmethod
    def warn(msg: str):
        print(f"\[[purple]TimeTracker[/]]\[[yellow]warn[/]] {msg}")

    @staticmethod
    def error(msg: str):
        print(f"\[[purple]TimeTracker[/]]\[[red]error[/]] {msg}")

    @staticmethod
    def input(msg: str):
        print(f"\[[purple]TimeTracker[/]]\[[cyan]input[/]] {msg}", end="")
        return input()
