from datetime import datetime, timedelta

now = datetime.now()
print( now)
print( now + timedelta(days=7))

diff = datetime(2025, 1, 10) - datetime(2025, 1, 1)
print( diff.days)