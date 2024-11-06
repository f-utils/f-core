import datetime
from . import op

def date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y %H:%M:%S')

def today():
    return datetime.date.today().strftime('%d/%m/%Y')

def now():
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

def to_hour(seconds):
    hours, remainder = op.mod(seconds, 3600)
    minutes, seconds = op.mod(remainder, 60)
    return f"{int(hours):02}h{int(minutes):02}m{int(seconds):02}s"
