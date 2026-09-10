import pytest
from datetime import time, datetime, date, timedelta

def check_time_conflict(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
    """Returns True if appointment A and appointment B overlap."""
    # Two intervals [start_a, end_a) and [start_b, end_b) overlap iff start_a < end_b and end_a > start_b
    return start_a < end_b and end_a > start_b

def test_overlapping_appointments():
    # Appt A: 10:00 - 10:30
    # Appt B: 10:15 - 10:45 (Overlaps!)
    assert check_time_conflict(time(10, 0), time(10, 30), time(10, 15), time(10, 45)) is True
    
    # Appt A: 10:00 - 10:30
    # Appt B: 09:45 - 10:15 (Overlaps!)
    assert check_time_conflict(time(10, 0), time(10, 30), time(9, 45), time(10, 15)) is True
    
    # Appt A: 10:00 - 11:00
    # Appt B: 10:15 - 10:45 (Inside!)
    assert check_time_conflict(time(10, 0), time(11, 0), time(10, 15), time(10, 45)) is True

def test_non_overlapping_appointments():
    # Appt A: 10:00 - 10:30
    # Appt B: 10:30 - 11:00 (Back to back - NO overlap)
    assert check_time_conflict(time(10, 0), time(10, 30), time(10, 30), time(11, 0)) is False
    
    # Appt A: 14:00 - 14:30
    # Appt B: 10:00 - 10:30 (Different times)
    assert check_time_conflict(time(14, 0), time(14, 30), time(10, 0), time(10, 30)) is False
