# Builds the shift report as a list of text lines.

from pricing import check_session, session_fee


def split_sessions(sessions):
    """Return (valid sessions, plates of invalid sessions), keeping ledger order."""
    valid = []
    invalid_plates = []
    for session in sessions:
        try:
            check_session(session)
            valid.append(session)
        except ValueError:
            invalid_plates.append(session.get("plate", "UNKNOWN"))
    return valid, invalid_plates


def session_line(session, fee):
    return f"{session['plate']:<10}{session['kind']:<11}{session['minutes']:>5} min {fee:>8.2f}"


def build_report(sessions, today, special_day):
    valid, invalid_plates = split_sessions(sessions)
    # Price every valid session at once.
    fees = [session_fee(session, today, special_day) for session in valid]

    lines = []
    lines.append("ParkSight - High Street Garage")
    lines.append(f"Day: {today}   Special day: {special_day}")
    lines.append("-" * 38)
    for plate in invalid_plates:
        lines.append(f"Invalid session: {plate}")
    for i in range(len(valid)):
        lines.append(session_line(valid[i], fees[i]))
    lines.append("-" * 38)

    total = round(sum(fees), 2)
    still_in = len([session for session in valid if session["minutes"] == 0])
    lines.append(f"Valid sessions: {len(valid)}")
    lines.append(f"Total revenue: {total:.2f}")
    lines.append(f"Still in garage: {still_in}")
    if len(valid) == 0:
        lines.append("Average fee: No sessions")
    else:
        lines.append(f"Average fee: {total / len(valid):.2f}")
    return lines