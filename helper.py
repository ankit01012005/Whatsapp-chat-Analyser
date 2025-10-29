from collections import Counter
import streamlit as st
import emoji

from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd

def fetch_stats(selected_user , df):

    if selected_user != "Overall":
       df = df[df['User'] == selected_user]
    # fetch no. of message
    number_of_messages = df.shape[0]
    # fetch no. of words in chat
    words=[]
    for message in df['Message']:
        words.extend(message.split())
    # fetch number of media files
    number_of_media_messages =  df[df["Message"] == "<Media omitted>"].shape[0]
    # fetch number of links
    list=[]
    for message in df['Message']:
        list.extend(extract.find_urls(message))

    return number_of_messages, len(words) , number_of_media_messages,len(list)

def most_busy_user(df):
    x = df["User"].value_counts().head(5)
    df = round(((df["User"].value_counts())/df.shape[0])*100, 2).reset_index().rename(columns={'index':'name',"User":"percentage"})
    return x,df

def word_cloud(df, selected_user):

    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().split())


    if selected_user != "Overall":
        df = df[df['User'] == selected_user]


    temp = df[
        (df["Message"] != "<Media omitted>")
    ]
    # Ensure no empty rows
    #temp = temp[temp["Message"].notna()]
    text = " ".join(temp["Message"].astype(str))

    if len(text.strip().split()) == 1:
        print("⚠️ No valid words found for word cloud")  # for debugging
        return None


    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white',
        stopwords=stop_words
    )
    df_wc = wc.generate(text)
    return df_wc


#most common_words

def most_common_words(selected_user,df):

    f = open("stop_hinglish.txt","r")
    stop_words = f.read()
    stop_words = stop_words.split()
    #print(stop_words)

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    temp = df[df["Message"] != "<Media omitted>"]

    print(temp)

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                #words.extend(word) why not extend why only append - with extend its showing just the charactors
    common_words = pd.DataFrame(Counter(words).most_common(20))

    return common_words

def emogi_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    emojis=[]
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    if len(emoji_df) > 0:
        return emoji_df


    else:
        list=[]
        return list
def month_year_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    timeline = df.groupby(['year', 'month']).count().reset_index()
    time=[]
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    timeline['month'] = timeline['month'].astype(pd.CategoricalDtype(categories=month_order, ordered=True))
    timeline['month'] = timeline['month'].sort_values().reset_index(drop=True)
    #st.title(type(timeline['month']))
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap



