import unittest

from parksight import LEDGER, SPECIAL_DAY, TODAY
from report import build_report, split_sessions

EXPECTED_TUESDAY = [
    "ParkSight - High Street Garage",
    "Day: Tuesday   Special day: Tuesday",
    "--------------------------------------",
    "Invalid session: CR09ODD",
    "Invalid session: CR18NEG",
    "HS12ABC   car           61 min     4.00",
    "VN07DEL   van           30 min     3.50",
    "MB33ZIP   motorbike      0 min     1.00",
    "CR55LNG   car          300 min     8.50",
    "VN21BIG   van          300 min    17.50",
    "CR40NOW   car            0 min     2.00",
    "MB02FST   motorbike    125 min     3.00",
    "--------------------------------------",
    "Valid sessions: 7",
    "Total revenue: 39.50",
    "Still in garage: 2",
    "Average fee: 5.64",
]


class ReportTests(unittest.TestCase):
    def test_full_report_matches_exactly(self):
        self.assertEqual(build_report(LEDGER, TODAY, SPECIAL_DAY), EXPECTED_TUESDAY)

    def test_normal_day_charges_full_car_fee(self):
        lines = build_report(LEDGER, "Monday", "Tuesday")
        self.assertIn("CR55LNG   car          300 min    10.00", lines)
        self.assertIn("Total revenue: 41.00", lines)

    def test_invalid_sessions_do_not_stop_the_report(self):
        sessions = [
            {"plate": "BAD1", "kind": "car", "minutes": -5},
            {"plate": "GOOD1", "kind": "car", "minutes": 60},
        ]
        lines = build_report(sessions, "Monday", "Tuesday")
        self.assertIn("Invalid session: BAD1", lines)
        self.assertIn("Valid sessions: 1", lines)
        self.assertIn("Total revenue: 2.00", lines)

    def test_no_valid_sessions_says_no_sessions(self):
        sessions = [{"plate": "BAD1", "kind": "car", "minutes": 1.5}]
        lines = build_report(sessions, "Monday", "Tuesday")
        self.assertIn("Valid sessions: 0", lines)
        self.assertIn("Total revenue: 0.00", lines)
        self.assertIn("Still in garage: 0", lines)
        self.assertEqual(lines[-1], "Average fee: No sessions")

    def test_empty_ledger(self):
        lines = build_report([], "Monday", "Tuesday")
        self.assertEqual(lines[-1], "Average fee: No sessions")

    def test_split_keeps_ledger_order(self):
        valid, invalid_plates = split_sessions(LEDGER)
        self.assertEqual([s["plate"] for s in valid][:3], ["HS12ABC", "VN07DEL", "MB33ZIP"])
        self.assertEqual(invalid_plates, ["CR09ODD", "CR18NEG"])

    def test_missing_plate_is_reported_as_unknown(self):
        valid, invalid_plates = split_sessions([{"kind": "car", "minutes": -1}])
        self.assertEqual(invalid_plates, ["UNKNOWN"])


if __name__ == "__main__":
    unittest.main()