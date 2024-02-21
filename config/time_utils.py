from django.utils.timezone import now
from datetime import timedelta
import pytz

def now_minutes():
    # Get the current time
    # current_time = now().astimezone(pytz.timezone('Europe/Madrid'))  # Convert to 'Europe/Madrid' timezone
    # Round down to the nearest minute by subtracting the seconds and microseconds
    rounded_time = now().replace(second=0, microsecond=0)
    return rounded_time
