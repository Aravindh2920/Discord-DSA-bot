import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def get_ist_now():
    return datetime.datetime.now(IST)

def get_ist_today():
    return get_ist_now().date()

def is_before_deadline():
    """
    Returns True if current IST time is before 23:59.
    """
    now = get_ist_now()
    deadline = now.replace(hour=23, minute=59, second=0, microsecond=0)
    return now <= deadline