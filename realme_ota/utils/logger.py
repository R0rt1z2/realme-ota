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
    def __init__(self, silent = False, verbosity = 1):
        self.silent, self.verbosity = silent, verbosity

    def log(self, buf, prio = 0):
        line = buf

        if self.verbosity > 0:
            line = f"[{datetime.datetime.now()}] "
        
            if (prio := str(prio)) in LOGGING_LEVELS:
                line += f"{LOGGING_LEVELS[prio]}: "
            else:
                line += "U: "
        
            line += f"{buf}"

        if not self.silent:
            print(line)
    
    def die(self, msg, ecl):
        self.log(f"{msg}", ecl)
        exit(ecl)