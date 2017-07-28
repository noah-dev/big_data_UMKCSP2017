#!/usr/bin/env python

import enchant #Used to filter out non-english
import string #used for string manipulation
import json #Used for loading of tweets
import sys

#setup dictionary
en=enchant.Dict("en_US")

#input/output tweet file
str_inputFile = 'Input/inTweets_1239.json'
str_outputFile = 'Output/t1_csv.txt'

#Return false if not english or not able to cast as string
def canBeString(val):
    try:
        str(val)
        return True
    except:
        return False


#Output File. Add headers
outFile=open(str_outputFile,"a")
outFile.write('user,has_ht,followers,friends\n')

for line in open(str_inputFile):
    try:
        #Append each json file to the tweets list
        tweet = json.loads(line)
    except:
        continue #If not json, skip

    tweetKeys = tweet.keys()

    if 'user' in tweetKeys and 'entities' in tweetKeys:
        #Load user id - to prevent multiples
        user = tweet['user']['id']
        #Check hashtag
        ht=tweet['entities']['hashtags']
        #Is it empty? If so, set ht to space
        if not ht:
            has_ht = 0
        else:
            has_ht = 1

        #Load followers and friends
        followers = tweet['user']['followers_count']
        friends = tweet['user']['friends_count']

    #Do not print if a timestamp
    if not 'limit' in tweetKeys:
        outFile.write(str(user) + ',' + str(has_ht) + ',' + str(followers) + ',' + str(friends) + '\n')

outFile.close()
