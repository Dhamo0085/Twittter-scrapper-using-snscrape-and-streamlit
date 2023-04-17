# Twittter_scrapper-using-snscrape-and-streamlit

Interative GUI using streamlit for twitter scraping 

REQUIRED SKILLS:
1.	Python scripting
2.	MongoDB
3.	Streamlit
4.	Snscrape
5.	pandas dataframes

OVERVIEW:

I have Created a GUI using streamlit that contains the follwing  features
1. Can enter any keyword or Hashtag to be searched 
2. select the starting date 
3. select the ending date  
4. Number of tweets needs to be scrapped.

After scraping is done, it has the following options

1.	Download data as CSV
2.	Download data as JSON
3.	Upload data to DATABASE
4.	Display All the Tweets scraped
5.	All the Uploaded Collections in Database are Displayed in the left side in the sidebar

WORKING:

Step1:
Initially I collected the Keyword, Start date, End date, and Number of tweets from the user using streamlit

Step 2:
The above details are fed to TwitterSearchScraper and TwitterHashtagScraper.
A dataframe is created to store the entire scraped data
Now we can download this scraped data in the form of CSV or JSON format 

Step3:
The database connection is established using pymongo
A new collection will be created and data is uploaded into that collection  if the user wish to upload 

Step4:
A separate sidebar is created to display all the collections that are uploaded to the database, On clicking any collection, we can see the documents in that collection


TWITTER SCRAPER STREAMLIT APP WORKING DEMO VIDEO:



