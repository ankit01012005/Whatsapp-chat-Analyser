import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Step 1: extract date, time, user, message directly
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s?[apAP][mM])\s*[-–]\s([^:]+):\s(.*)'
    matches = re.findall(pattern, data)

    records = []
    for date, time, user, message in matches:
        records.append({
            "Date": date,
            "Time": time.replace("\u202f", " "),
            "User": user.strip(),
            "Message": message.strip()
        })

    # Step 2: create dataframe
    df = pd.DataFrame(records)

    # Step 3: convert to proper datetime
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')
    df["Time"] = df["Time"].str.strip().apply(
        lambda x: datetime.strptime(x.replace("\u202f", " "), "%I:%M %p").time()
    )

    df["Datetime"] = df.apply(lambda r: pd.Timestamp.combine(r["Date"], r["Time"]), axis=1)
    df.drop(["Date", "Time"], axis=1, inplace=True)

    # Step 4: extract components
    df['only_date'] = df['Datetime'].dt.date
    df["year"] = df["Datetime"].dt.year
    df["month"] = df["Datetime"].dt.month_name()
    df["day"] = df["Datetime"].dt.day
    df['day_name'] = df['Datetime'].dt.day_name()
    df["hour"] = df["Datetime"].dt.hour
    df["min"] = df["Datetime"].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
