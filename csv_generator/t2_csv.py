#!/usr/bin/env python

import enchant #Used to filter out non-english
import string #used for string manipulation
import json #Used for loading of tweets
import sys

#setup dictionary
en=enchant.Dict("en_US")

#input/output tweet file
str_inputFile = 'Input/inTweets_1239.json'
str_outputFile = 'Output/t2_csv.txt'

#Return false if not english or not able to cast as string
def isValid(val):
    flag = True #Assume to be valid - see if assumption is right/wrong

    if val == '': return flag #If blank, it is valid ('' causes enchant dict to throw exception on my system)

    if not en.check(val): flag = False #Check if english

    #Below makes assumption that any string can be written to output file.
    try: str(val) #See if val can be casted as string. If so, should be able to write to file
    except: flag = False #IF cannot be casted as string, should not be able to write to file

    #If english and can be casted as string, flag should have remained unchanged as True.
    return flag


#Output File. Add headers
outFile=open(str_outputFile,"a")
outFile.write('id,ht,rt_ht,rt_rt_cnt\n')

#If ht is ' ', there is no hashtag
#If rt_ht and rt_rt_cnt are ' ', there is no retweet status
#If rt_ht is ' ' but rt_rt_cnt is not ' ', then there is retweet but no retweet hashtag

for line in open(str_inputFile):
    try:
        #Append each json file to the tweets list
        tweet = json.loads(line)
    except:
        continue #If not json, skip
    tweetKeys = tweet.keys()

    #Load hashtag
    if 'entities' in tweetKeys:
        ht=tweet['entities']['hashtags']
        #Is it empty? If so, set ht to space
        if not ht: ht = ''
        #If there is ht, load it
        else: ht = ht[0]['text']

    #Is the tweet a retweet?
    if 'retweeted_status' in tweetKeys:
        rt_ht=tweet['retweeted_status']['entities']['hashtags']
        if rt_ht: rt_ht = rt_ht[0]['text']
        else: rt_ht = ''
        rt_rt_cnt = str(tweet['retweeted_status']['retweet_count'])
        rt_id = str(tweet['retweeted_status']['id'])
    else:
        rt_ht = ''
        rt_rt_cnt = ''
        rt_id = ''

    #Do not print if a timestamp
    if not 'limit' in tweetKeys:
        if isValid(ht) and isValid(rt_ht):
            outFile.write(rt_id + ',' + ht +  ',' + rt_ht + ',' + rt_rt_cnt + '\n')


outFile.close()
