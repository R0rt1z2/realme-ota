import datetime

# Logging verbosity
LOGGING_LEVELS = {
    "-1":"U", # Unknown (Default)
    "0":"I",  # Info
    "1":"W",  # Warning
    "2":"E",  # Error
    "3":"F",  # Fatal Error
    "4":"D",  # Debug
    "5":"V",  # Verbose
}

def log(buf, prio = 0):
    line = buf

    if _verbosity == 1:
        line = f"[{datetime.datetime.now()}] "
    
        if (prio := str(prio)) in LOGGING_LEVELS:
            line += f"{LOGGING_LEVELS[prio]}: "
        else:
            line += "U: "
    
        line += f"{buf}"

    print(line)

def init(verbosity = 1):
    global _verbosity
    _verbosity = verbosity