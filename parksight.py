# The supervisor's paper pad for today, typed in as a list of sessions.

from report import build_report

TODAY = "Tuesday"
SPECIAL_DAY = "Tuesday"

LEDGER = [
    {"plate": "HS12ABC", "kind": "car", "minutes": 61},
    {"plate": "VN07DEL", "kind": "van", "minutes": 30},
    {"plate": "MB33ZIP", "kind": "motorbike", "minutes": 0},
    {"plate": "CR55LNG", "kind": "car", "minutes": 300},
    {"plate": "VN21BIG", "kind": "van", "minutes": 300},
    {"plate": "CR09ODD", "kind": "car", "minutes": 45.5},
    {"plate": "CR18NEG", "kind": "car", "minutes": -10},
    {"plate": "CR40NOW", "kind": "car", "minutes": 0},
    {"plate": "MB02FST", "kind": "motorbike", "minutes": 125},
]

if __name__ == "__main__":
    for line in build_report(LEDGER, TODAY, SPECIAL_DAY):
        print(line)