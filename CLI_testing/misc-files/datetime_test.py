import datetime

#today = datetime.datetime.today()

#first = today.replace(day=1)

#prevMonth = first-datetime.timedelta(days=1)

date_string = datetime.datetime.strptime('2021-10-28', '%Y-%m-%d')

first = date_string.replace(day=1)
prevMonth = first - datetime.timedelta(days=1)

print(date_string > prevMonth)
print(date_string)
print(prevMonth)
