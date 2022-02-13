from datetime import datetime, date, time, timedelta

def alarm_rings(start_date_str, end_date_str):
    result = []
    current_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str)
    while current_date <= end_date:
        if current_date.weekday() < 5:
            result.append(datetime(current_date.year, current_date.month, current_date.day, 7).isoformat(sep=' '))
        else:
            result.append(datetime(current_date.year, current_date.month, current_date.day, 9).isoformat(sep=' '))
        current_date += timedelta(days=1)
    return result
    