#!/usr/bin/env python

from langdetect import detect #used to detect language
import string #used for string manipulation
import json #Used for loading of tweets
import sys

#input/output tweet file
str_inputFile = 'Input/trends.json'
str_outputFile = 'Output/t3_csv.txt'

#Return false if not able to cast as string
def canBeString(val):
    try:
        str(val)
        return True
    except:
        return False


#Output File. Add headers
outFile=open(str_outputFile,"a")
outFile.write('time,trend,volume\n')

#If ht is ' ', there is no hashtag
#If rt_ht and rt_rt_cnt are ' ', there is no retweet status
#If rt_ht is ' ' but rt_rt_cnt is not ' ', then there is retweet but no retweet hashtag

for line in open(str_inputFile):
    try:
        #Append each json file to the tweets list
        trendQuery = json.loads(line)
    except:
        continue #If not json, skip

    trendQueryKey = trendQuery.keys()

    #Begin writing trends to csv
    if 'details' in trendQueryKey:
        #Pull details - contains the desired attributes
        details = trendQuery['details'][0]
        #Retrive created_at - remove unnecessary characters
        created_at = details['created_at']
        created_at = created_at.replace('T',' ')
        created_at = created_at.replace('Z','')

        #Pull trends - contains names of trend and tweet volumes
        trendList = details['trends']
        for trend in trendList:
            name = trend['name']
            volume = trend['tweet_volume']
            #Check if trend name can be casted a string.
            if canBeString(name):
                #If trend volume is null, replace with empty string
                if not volume:
                    volume = ''

                #Write to output files
                outStr = created_at +',' + name + ',' + str(volume) + '\n'
                print outStr
                outFile.write(outStr)


outFile.close()
