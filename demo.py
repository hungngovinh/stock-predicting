
from pandas_datareader import data
import datetime
import tweepy
from textblob import TextBlob
import wikipedia
import requests
from bs4 import BeautifulSoup

# from nytimesarticle import articleAPI

from flask import Flask, abort, request, render_template
import json

app = Flask(__name__)




@app.route('/')
def foo():
    return render_template("index.html")






start=datetime.datetime(2018,1,1)
end=datetime.datetime(2018,2,1)



df=data.DataReader(name="MSTR",data_source="google",start=start,end=end)

# Dependencies
# nytAPI = articleAPI('f12a2eee165c4f6a8d8ca2f2139c9427')

r = requests.get('https://www.nytimes.com/search/microstrategy?action=click&contentCollection&region=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=collection')
c = r.content

soup = BeautifulSoup(c,"html.parser")
all = soup.find_all("h4", {"class": "Item-headline--3WqlT"})

url="https://news.google.com/news/search/section/q/microstrategy/microstrategy?hl=en-IN&gl=IN&ned=in"
code=requests.get(url)
soupGoogle=BeautifulSoup(code.content,'html.parser')
print("Latest news from GOOGLE")
allGoogle = soup.find_all("a", {"class": "nuEeue hzdq5d ME7ew"})
total_sentiment = 0
total_fact = 0
number_of_tweets = 0
for eachGoogle in allGoogle:
    analysis = TextBlob(eachGoogle.text)
    total_sentiment += analysis.polarity
    total_fact += analysis.subjectivity
    number_of_tweets += 1
    print(eachGoogle.text)


print(total_sentiment)
print(total_fact)
total_sentiment = 0
total_fact = 0
number_of_tweets = 0
# Printing out latest news from microstrategy
for each in all:
    # print(each)
    analysis = TextBlob(each.text)
    total_sentiment += analysis.polarity
    total_fact += analysis.subjectivity
    number_of_tweets += 1
    print(each.text)

print(total_sentiment/number_of_tweets)
print(total_fact/number_of_tweets)
consumer_key = '74oTXye3keiNytzD86ozj918m'
consumer_secret = 'NkLoXopmnyMWMfkHetvxByXnmG00cu6APGu8CAznC3eV9UB75h'

access_token = '948369615343837184-kpAzj3ZJ1zfRFnNmYpvewCCaU5nrr9y'
access_token_secret = 'nwBz43sweeC3Jba5woAevx9iBoC4jLGWkL9aRSfHvOy96'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
public_tweets = api.search('Microstrategy news')


total_sentiment = 0
total_fact = 0
number_of_tweets = 0
print(df)
for tweet in public_tweets:
    print(tweet)
    analysis = TextBlob(tweet.text)
    total_sentiment += analysis.polarity
    total_fact += analysis.subjectivity
    number_of_tweets += 1

print("Attitude toward the company on Social Media is: " + str((total_sentiment/number_of_tweets)))
print("Facts toward the company on Social Media is: " + str((total_fact/number_of_tweets)))

print(wikipedia.summary("Microstrategy"))

# articles = nytAPI.search(q="trump")

@app.route('/success')
def successs():
    data={
        'total_sentiment' : total_sentiment,
        'number_of_tweets' : number_of_tweets,
        'total_fact' : total_fact
    }
    return render_template('success.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# df.to_csv('out.csv')
