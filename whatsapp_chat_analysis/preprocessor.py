import pandas as pd
import re


def preprocess(data):
    messages = []
    for line in data.splitlines():
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2} - )([^:]*): (.*)', line)
        if match:
            date = match.group(1).strip()[:-3]
            user = match.group(2).strip()
            message = match.group(3)

            messages.append([date, user, message])

    df = pd.DataFrame(messages, columns=['date', 'user', 'message'])
    df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y, %H:%M", errors='coerce')
    df = df.dropna(subset=['date'])

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date

    df['message'] = df['message'].str.replace(r'http\S+', '', regex=True)
    df['message'] = df['message'].str.replace(r'@\w+', '', regex=True)
    df['message'] = df['message'].str.replace(r'\n', ' ', regex=True)

    return df
