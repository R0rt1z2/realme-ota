import datetime

LOGGING_LEVELS = {
    0:  "U",    # Unknown (Default)
    1:  "F",    # Fatal Error
    2:  "E",    # Error
    3:  "W",    # Warning
    4:  "I",    # Info
    5:  "D",    # Debug
}

class Logger:
    def __init__(self, level):
        self.level = level if level in range(0, 6) else 4

    def log(self, buf, prio = 4):
        if prio <= self.level:
            print(f"[{datetime.datetime.now()}] {LOGGING_LEVELS.get(prio, LOGGING_LEVELS[0])}: {buf}")

    def die(self, msg, ecl):
        self.log(f"{msg}", ecl)
        exit(ecl)