import unittest

from pricing import check_session, is_special_day, session_fee, started_hours


def make(kind, minutes):
    return {"plate": "TEST1", "kind": kind, "minutes": minutes}


class StartedHoursTests(unittest.TestCase):
    def test_zero_minutes_is_one_hour(self):
        self.assertEqual(started_hours(0), 1)

    def test_exact_hour_is_not_rounded_up(self):
        self.assertEqual(started_hours(60), 1)
        self.assertEqual(started_hours(240), 4)

    def test_one_minute_over_starts_a_new_hour(self):
        self.assertEqual(started_hours(61), 2)
        self.assertEqual(started_hours(1), 1)


class FeeTests(unittest.TestCase):
    def test_examples_from_the_brief(self):
        self.assertEqual(session_fee(make("car", 61), "Monday", "Tuesday"), 4.00)
        self.assertEqual(session_fee(make("van", 30), "Monday", "Tuesday"), 3.50)
        self.assertEqual(session_fee(make("motorbike", 0), "Monday", "Tuesday"), 1.00)

    def test_long_car_on_normal_day_pays_full(self):
        self.assertEqual(session_fee(make("car", 300), "Monday", "Tuesday"), 10.00)

    def test_long_car_on_special_day_gets_15_percent_off(self):
        self.assertEqual(session_fee(make("car", 300), "Tuesday", "Tuesday"), 8.50)

    def test_special_needs_over_four_hours(self):
        # 240 minutes is exactly 4 hours, not over it.
        self.assertEqual(session_fee(make("car", 240), "Tuesday", "Tuesday"), 8.00)
        self.assertEqual(session_fee(make("car", 241), "Tuesday", "Tuesday"), 8.50)

    def test_van_gets_no_special(self):
        self.assertEqual(session_fee(make("van", 300), "Tuesday", "Tuesday"), 17.50)

    def test_discount_is_rounded_to_two_decimals(self):
        # 9 hours = 18.00, minus 15% = 15.30 (not 15.299999...)
        self.assertEqual(session_fee(make("car", 540), "Tuesday", "Tuesday"), 15.30)

    def test_special_day_ignores_case_and_spaces(self):
        self.assertTrue(is_special_day(" tuesday ", "Tuesday"))
        self.assertFalse(is_special_day("Wednesday", "Tuesday"))


class CheckSessionTests(unittest.TestCase):
    def test_valid_session_passes(self):
        check_session(make("car", 0))
        check_session(make("van", 1000))

    def test_fractional_minutes_rejected(self):
        with self.assertRaises(ValueError):
            check_session(make("car", 45.5))

    def test_negative_minutes_rejected(self):
        with self.assertRaises(ValueError):
            check_session(make("car", -10))

    def test_text_minutes_rejected(self):
        with self.assertRaises(ValueError):
            check_session(make("car", "90"))

    def test_boolean_minutes_rejected(self):
        with self.assertRaises(ValueError):
            check_session(make("car", True))

    def test_missing_minutes_rejected(self):
        with self.assertRaises(ValueError):
            check_session({"plate": "TEST1", "kind": "car"})

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):
            check_session(make("lorry", 30))


if __name__ == "__main__":
    unittest.main()