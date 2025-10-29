import pandas as pd
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyser')
uploaded_file = st.sidebar.file_uploader('Upload WhatsApp Chat')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    #print(data)
    #print(type(data))
    #print(data[0])
    #fetch user
    user_list = df['User'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt..", user_list)
    # stats columns
    if st.sidebar.button("Analyse"):
        numOfMessage,words,number_of_media_messages,number_of_links = helper.fetch_stats(selected_user,df)
        st.title("Top Stats")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(numOfMessage)
        with col2:
            st.header("Words")
            st.title(words)
        with col3:
            st.header("Media Messages")
            st.title(number_of_media_messages)
        with col4:
            st.header("Number of links")
            st.title(number_of_links)
    #timeline
        st.title("Monthly Timeline")
        timeline = helper.month_year_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline["time"],timeline["Message"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

    # most active user columns
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                ax.bar(x.index,x.values,color="green")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #word cloud
        st.title("Word Cloud")
        df_wc = helper.word_cloud(df, selected_user)
        if df_wc is None:
            st.warning("Word cloud is empty or contains no valid words.")
        else:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

        #most common words
        if df_wc != None:
            st.title("Most Busy Words")
            most_common_words = helper.most_common_words(selected_user,df)
            fig,ax = plt.subplots()
            ax.barh(most_common_words[0],most_common_words[1],color="blue")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        #emogi analyses
        emoji_df = helper.emogi_helper(selected_user, df)
        if len(emoji_df) != 0:
            st.title("Emoji Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.warning("Emoji not found ")
