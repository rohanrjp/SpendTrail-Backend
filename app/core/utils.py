from datetime import datetime, timezone, timedelta

def get_ist_datetime():
    utc_now = datetime.now(timezone.utc)  
    ist_offset = timedelta(hours=5, minutes=30)  
    ist_now = utc_now + ist_offset  
    return ist_now