HOURLY_RATES = {"car": 2.00, "van": 3.50, "motorbike": 1.00}
SPECIAL_MINUTES = 240
SPECIAL_DISCOUNT = 0.15


def check_session(session):
    """Raise ValueError if the session cannot be priced."""
    kind = session.get("kind")
    minutes = session.get("minutes")
    if kind not in HOURLY_RATES:
        raise ValueError("unknown vehicle kind")
    if type(minutes) is not int:
        raise ValueError("minutes must be a whole number")
    if minutes < 0:
        raise ValueError("minutes cannot be negative")


def started_hours(minutes):
    """Any part of an hour counts as a full hour; 0 minutes is still 1 hour."""
    hours = minutes // 60
    if minutes % 60 != 0:
        hours = hours + 1
    if hours == 0:
        hours = 1
    return hours


def is_special_day(today, special_day):
    return today.strip().lower() == special_day.strip().lower()


def session_fee(session, today, special_day):
    """Return the fee for a session that has already passed check_session."""
    kind = session["kind"]
    minutes = session["minutes"]
    fee = started_hours(minutes) * HOURLY_RATES[kind]
    if kind == "car" and minutes > SPECIAL_MINUTES and is_special_day(today, special_day):
        fee = fee * (1 - SPECIAL_DISCOUNT)
    return round(fee, 2)