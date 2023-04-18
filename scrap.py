import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo
import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")  # To connect to MONGODB
mydb = client["Twitter_Database"]  # To create a DATABASE
tweets_df = pd.DataFrame() #To create an empty dataframe
dfm = pd.DataFrame()

#MENU & OPTIONS DISPLAYED
st.write("# Twitter data scraping")
option = st.selectbox('How would you like the data to be searched?',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'Example: IPL')
start = st.date_input("Select the start date", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 1000, 10)
tweets_list = []

#SCRAPING USING SNSCRAPE
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.rawContent, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.rawContent, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cant be empty')

# CONVERT TO CSV
@st.cache_data # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
     # DOWNLOAD AS CSV
    csv = convert_df(tweets_df)
    st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)

    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient ='records')
    st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

# SHOW TWEETS
if st.button('Show Tweets'):
    st.write(tweets_df)
    
# UPLOAD DATA TO DATABASE
if st.button('Upload Tweets to Database'):
 coll = word
 coll = coll.replace(' ', '_') + '_Tweets'
 mycoll = mydb[coll]
 dict = tweets_df.to_dict('records')
 if dict:
     mycoll.insert_many(dict)
     ts = datetime.time()
     mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word + str(ts)}}, upsert=False, array_filters=None)
     st.success('Successfully uploaded to database')
     st.balloons()
 else:
     st.warning('Cant upload because there are no tweets')



