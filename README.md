# TimeTracker
Fast and intuitive time tracker.

### installation
```bash
git clone https://github.com/marcelm9/TimeTracker.git
cd TimeTracker
pip install .
```

### commands
```bash
# list available commands
python -m TimeTracker help

# create new tracker
python -m TimeTracker new <name>

# spend time
python -m TimeTracker spend <name> <time-input>

# show total time spent on one tracker
python -m TimeTracker total <name>

# show details for tracker
python -m TimeTracker details <name>

# delete tracker
python -m TimeTracker delete <name>

# list all trackers
python -m TimeTracker list
```

### examples
```bash
# create new tracker
python -m TimeTracker new task1

# spend time on it
python -m TimeTracker spend task1 1h30m

# spend more time on it
python -m TimeTracker spend task1 5m

# show total time spent
python -m TimeTracker total task1 # -> 1h 35m
```

```bash
# create new trackers
python -m TimeTracker new task1-subtask1
python -m TimeTracker new task1-subtask2

# spend time on each
python -m TimeTracker spend task1-subtask1 1h
python -m TimeTracker spend task1-subtask2 30m

# show total for any trackers starting with 'task1'
python -m TimeTracker total task1. # -> 1h 30m
```