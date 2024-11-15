# ChatLens.py
import streamlit as st
import pandas as pd
import helper
import matplotlib.pyplot as plt

# Background styling
st.markdown(
    """
    <style>
    .main-bg { background: linear-gradient(135deg, #1a1a1a, #333333); height: 100%; width: 100%; position: fixed; top: 0; left: 0; z-index: -1; }
    .title-text { font-size: 50px; color: white; font-family: 'Arial', sans-serif; font-weight: bold; text-align: center; margin-top: 20px; }
    .upload-box { margin-top: 10px; }
    </style>
    <div class="main-bg"></div>
    """,
    unsafe_allow_html=True
)

# Logo display
st.title("WhatsApp Chat Analysis")

# File upload
uploaded_file = st.file_uploader("Upload a chat file", type=["txt"])

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    df = helper.preprocess(data)
    st.success("Data processed successfully!")

    # Sidebar statistics
    st.sidebar.header("Statistics")
    user_list = df['user'].unique().tolist()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select user", user_list)

    # Number of messages
    num_messages = df[df['user'] == selected_user].shape[0] if selected_user != "Overall" else df.shape[0]
    st.sidebar.markdown(f"**Total Messages: {num_messages}**")

    # Monthly Timeline
    st.subheader("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    if not timeline.empty:
        fig, ax = plt.subplots()
        ax.bar(timeline['month'], timeline['message_count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    else:
        st.warning("No data available for the selected user or time period.")

    # Daily Timeline
    st.subheader("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['date'], daily_timeline['message_count'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    sentiment_score = df['sentiment'].mean()
    st.write(f"Average Sentiment Score: {sentiment_score:.2f}")

    # Emoji Analysis
    st.subheader("Emoji Analysis")
    emoji_count, emojis = helper.emoji_analysis(df)
    st.write(f"Total Emojis Used: {emoji_count}")
    st.dataframe(emojis)

    # Media Analysis
    st.subheader("Media Analysis")
    media_data = helper.media_analysis(df)
    for media, data in media_data.items():
        st.write(f"**{media.capitalize()}s shared**: {len(data)}")
        if not data.empty:
            st.dataframe(data[['date', 'user', 'message']])
        else:
            st.write("No media shared.")
