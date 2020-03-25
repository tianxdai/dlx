import GetOldTweets3 as got
import pandas as pd
import time
from datetime import datetime, timedelta
import sys

def gettweets(ticker):
    try:
        file = open(ticker+".txt","r+")
        start_date = file.readlines()[-1].split('\t')[0].split()[0]
        file.close()
    except:
        file = open(ticker+'.txt', "w")
        file.close()
        start_date = str(datetime.today()).split()[0]
    print('Start Date:', start_date, ticker)

    i = 0
    num_tweets = 0
    file_closed = True
    while True:
        try:
            if file_closed:
                file = open(ticker+".txt", 'a+')
            since_date = str(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=i+1)).split()[0]
            until_date = str(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=i)).split()[0]
            max_date = str(datetime.today() - timedelta(days=i)).split()[0]
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch('$'+ticker+' -filter:replies') \
                                                       .setSince(since_date) \
                                                       .setUntil(until_date) \
                                                       .setMaxTweets(100)
            num = 0
            for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
                num += 1
                num_tweets += 1
                if num_tweets % 1000 == 0:
                    print('Saved', num_tweets)
                file.write(str(tweet.date) + '\t' + tweet.id + '\t' + tweet.hashtags + '\t' + tweet.username + '\t' + tweet.text.replace("\n", ' ') + '\n')
            i += 1
            print(since_date, until_date, num, ticker)
            
            if since_date == '2007-01-01':
                break
            
        except AttributeError:
            file.close()
            file_closed = True
            print('---------- Error: Attribute Error', since_date, until_date)
            i += 1
            
        except:
            file.close()
            file_closed = True
            print('Error', since_date, until_date)
            time.sleep(120)

if __name__ == "__main__":

    for ticker in sys.argv[1:]:
        gettweets(ticker)
        

