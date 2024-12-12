from datetime import datetime, timezone
import pytz

def get_ist_datetime():
    utc_now = datetime.now(timezone.utc)
    ist_tz = pytz.timezone("Asia/Kolkata")
    ist_now = utc_now.astimezone(ist_tz)
    return ist_now