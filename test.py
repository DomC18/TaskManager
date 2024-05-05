from datetime import datetime, timedelta

def get_current_week_dates_formatted() -> list[str]:
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates_formatted = []

        for i in range(7):
            formatted_date = (start_of_week + timedelta(days=i)).strftime("%m/%d/%Y")
            week_dates_formatted.append(formatted_date)

        return week_dates_formatted

print(get_current_week_dates_formatted()[0][0:5] + "-" + get_current_week_dates_formatted()[-1][0:5])