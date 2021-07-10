from dateutil.parser import parse
import datetime
dt = parse("2021-04-12 12:00:00", fuzzy=True)

print(dt, datetime.datetime.now())