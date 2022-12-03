#
# This file is part of realme-ota (https://github.com/R0rt1z2/realme-ota).
# Copyright (c) 2022 Roger Ortiz.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

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
