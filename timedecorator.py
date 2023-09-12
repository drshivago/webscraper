
def divider(time, amount):
    unit = time % amount
    temp_time = time - unit
    temp_time = temp_time // amount
    return (temp_time, unit)

def time(time_date):

    if time_date < 60:
        return time_date

    time_date, seconds = divider(time_date, 60)
    time_date, minutes = divider(time_date, 60)
    days, hours = divider(time_date, 24)

    return "Time elapsed:", days, "days", hours, "hours", minutes, "minutes", seconds, "seconds"

#testing
#num = 152343734
#print(time(num))
