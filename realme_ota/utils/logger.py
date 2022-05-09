import datetime

LOGGING_LEVELS = {
    "-1":"U", # Unknown (Default)
    "0":"I",  # Info
    "1":"W",  # Warning
    "2":"E",  # Error
    "3":"F",  # Fatal Error
    "4":"D",  # Debug
    "5":"V",  # Verbose
}

class Logger:
    def __init__(self, silent = 0):
        self.silent = silent

    def log(self, buf, prio = 0):
        if not self.silent:
            print(f"[{datetime.datetime.now()}] {LOGGING_LEVELS.get(prio, LOGGING_LEVELS[str(prio)])}: {buf}")

    def die(self, msg, ecl):
        self.log(f"{msg}", ecl)
        exit(ecl)