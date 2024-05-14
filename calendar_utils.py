import datetime, calendar
from datetime import datetime, timedelta

months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
# holidays = ["2023-01-26", "2023-03-07", "2023-08-15", "2023-09-19", "2023-10-02", "2023-10-24", "2023-11-14", "2023-11-27", "2023-12-25"]
holidays = [
    "2023-01-26",
    "2023-03-07",
    "2023-03-30",
    "2023-04-04",
    "2023-04-07",
    "2023-04-14",
    "2023-05-01",
    "2023-06-29",
    "2023-08-15",
    "2023-09-19",
    "2023-10-02",
    "2023-10-24",
    "2023-11-14",
    "2023-11-27",
    "2023-12-25",
    "2024-01-22",
    "2024-01-26"
]

def get_all_thursdays_of_current_month():
    today = datetime.date.today()
    weekly_thursday = []

    for week in calendar.monthcalendar(today.year, today.month):
        if week[3] != 0:
            weekly_thursday.append(week[3])
    return weekly_thursday



def is_working_day(date):
    # Check if the date is not a Saturday or Sunday and not in the list of holidays
    return date.weekday() < 5 and date.strftime("%Y-%m-%d") not in holidays

def find_nth_last_working_day(n):
    today = datetime.today()
    working_day_count = 1
    current_date = today

    # If today is Saturday or Sunday, adjust current_date to last Friday
    if current_date.weekday() >= 5:
        current_date -= timedelta(days=current_date.weekday() - 4)

    if current_date.strftime("%Y-%m-%d") in holidays:
        working_day_count = 0

    while working_day_count < n:
        current_date -= timedelta(days=1)
        if is_working_day(current_date):
            working_day_count += 1

    return current_date.strftime("%Y-%m-%d")


# n = 25
# result = find_nth_last_working_day(n, holidays)
# print(f"The {n}th last working day from today is {result}")


def calculate_intervals(t):
    current_time = datetime.now().time()
    start_time = datetime.strptime("09:15:00", "%H:%M:%S").time()
    end_time = datetime.strptime("15:30:00", "%H:%M:%S").time()
    if current_time >= end_time:
        current_time = end_time

    time_difference_seconds = (datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), start_time)).total_seconds()
    time_difference_mins = time_difference_seconds/60

    if time_difference_mins % t == 0:
        return int(time_difference_mins/t)

    return int(time_difference_mins/t + 1)

def no_of_intervals_in_one_day(t):
    start_time = datetime.strptime("09:15:00", "%H:%M:%S").time()
    end_time = datetime.strptime("15:30:00", "%H:%M:%S").time()
    time_difference_seconds = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds()
    time_difference_mins = time_difference_seconds/60
    if time_difference_mins % t == 0:
        return int(time_difference_mins/t)

    return int(time_difference_mins/t + 1)


def no_of_days_to_go_back(period, interval):
    today_intervals = calculate_intervals(int(interval))
    if period > today_intervals:
        period -= today_intervals
    intervals_in_one_day = no_of_intervals_in_one_day(int(interval))

    if period % intervals_in_one_day == 0:
        return int(period/intervals_in_one_day)

    return int(period/intervals_in_one_day + 1)


def get_anchor_date(period, interval):
    if interval == "D":
        return find_nth_last_working_day(period)
    # elif interval == "W":
    #
    else:
        return find_nth_last_working_day(no_of_days_to_go_back(period, interval))

def get_anchor_date_for_ma(period, interval):
    if interval == "D":
        period = round(period * 4.61)
        return find_nth_last_working_day(period)
    # elif interval == "W":
    #
    else:
        return find_nth_last_working_day(no_of_days_to_go_back(period, interval))


#
# interval = 5
# result = calculate_intervals(interval)
# print(f"The number of {interval}-minute intervals since 9:15 am is {result}")

def get_start_of_week(date):
    days_to_monday = date.weekday()
    start_of_week = date - timedelta(days=days_to_monday)
    return start_of_week.strftime("%Y-%m-%d")

def get_today_in_yyyy_mm_dd():
    return datetime.today().strftime("%Y-%m-%d")


def get_last_working_day(start_date=datetime.today()):
    while not is_working_day(start_date):
        start_date = start_date - timedelta(days=1)

    # print(start_date.strftime("%Y-%m-%d"))
    return start_date.strftime("%Y-%m-%d")

def convert_date_string_to_standard_format(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')

def get_one_year_ago():
    # Get today's date
    today = datetime.today()

    # Calculate the date one year ago
    one_year_ago = today.replace(year=today.year - 1)

    # Format the date in 'yyyy-mm-dd' format
    one_year_ago_formatted = one_year_ago.strftime('%Y-%m-%d')

    return one_year_ago_formatted

# print(get_last_working_day())
# today = datetime.strptime("2023-09-03", "%Y-%m-%d")
# start_of_week = get_start_of_week(today)
#
# print(f"The start of the week for {today.strftime('%Y-%m-%d')} is {start_of_week}")