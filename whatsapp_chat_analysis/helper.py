# helper.py
import pandas as pd
import re
from datetime import datetime
from textblob import TextBlob

def preprocess(data):
    messages = []
    date_format = "%d/%m/%Y, %H:%M"  # Adjust this format if your chat file format is different

    lines = data.splitlines()
    for line in lines:
        match = re.match(r'^(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}) - (.+?): (.+)', line)
        if match:
            timestamp, user, message = match.groups()
            try:
                timestamp = datetime.strptime(timestamp, date_format)
                messages.append([timestamp, user, message])
            except ValueError:
                continue
        else:
            if messages:
                messages[-1][2] += " " + line

    df = pd.DataFrame(messages, columns=["timestamp", "user", "message"])
    df['date'] = df['timestamp'].dt.date
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['month_num'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    return df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num']).count()['message'].reset_index()
    timeline['month'] = timeline.apply(lambda x: f"{x['month_num']}-{x['year']}", axis=1)
    timeline = timeline[['month', 'message']].rename(columns={"message": "message_count"})
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_data = df.groupby('date').count()['message'].reset_index()
    daily_data.columns = ['date', 'message_count']
    return daily_data

def media_analysis(df):
    media_types = ['image', 'audio', 'video', 'document']
    media_data = {media: df[df['message'].str.contains(media, case=False, na=False)] for media in media_types}
    return media_data

def emoji_analysis(df):
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\u2600-\u26FF\u2700-\u27BF\u2300-\u23FF\u2B50\u23F0\u23F3\u2648-\u2653\u1F004-\u1F0CF\u1F300-\u1F5FF\u1F680-\U0001F6FF\u1F700-\U0001F77F\u1F780-\U0001F7FF\u1F800-\U0001F8FF\u1F900-\U0001F9FF\u1FA00-\U0001FA6F\u1FA70-\U0001FAFF]')
    df['emojis'] = df['message'].apply(lambda x: emoji_pattern.findall(x))
    emoji_count = df['emojis'].apply(len).sum()
    return emoji_count, df['emojis']
