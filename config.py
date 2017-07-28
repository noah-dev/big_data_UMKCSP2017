#!/usr/bin/env python
import random
#This class holds the file paths and file names.
#Used by app.py
class conf_Query():
    log_print = True
    projectPath = '/home/hduser/shared_folder/Project_3_App'
    inputPath = '/input/'
    staticPath = '/static/'
    ext = '.png'

    #Query 1 filenames
    inFile1 = 't1_csv.txt'
    outFile1 = 't1'
    fig_title1 = 'Hashtag Presence vs Followers & Friends (Spark SQL & DataFrames)'
    fig_title1_scale = 'Correlation: # vs Friends + Followers'
    fig_axis1 = ["With Hashtag","Without Hashtag"]
    fig_axis1_scale = '1:Strong | 0:None | -1:Inverted'
    fig_desc1 = 'Does friend/follower correlate with hashtage usage? '+\
    'Divide tweets into two buckets based on presence or absence of hashtag.\n'+\
    'Each bucket will hold the cumulative sum of friends and followers. '+\
    'This is shown on the pie chart.\n' +\
    'A raw count is not enough to establish correlation however. '+\
    'For this, a correlation analysis is done and is shown on the bar chart'
    #Query 2 filenames
    inFile2 = 't2_csv.txt'
    outFile2 = 't2'
    fig_title2 = 'Hashtag Volume in ReTweets - (RDD Transformations)'
    fig_axis2 = ["RTs with H#", "RTs with No H#", "New tweets with H#"]
    fig_desc2 = 'How important are tweets for hashtag trending? '+\
    'A hashtag can be used in either a new tweet or in a retweet.\n'+\
    'How much hashtag volume comes from retweets compared to new tweets?'+\
    'And out of all the retweet volume, how much of it is for a hashtag?'

    #Query 3 filenames
    inFile3 = 't3_csv.txt'
    outFile3 = 't3'
    fig_title3 = 'Total Trend Volume over Time - (Spark SQL & DataFrames)'
    fig_desc3 = 'How do trends behave over time? The main plot shows ' +\
    'cumulative volume across all trends over time.\n' +\
    'In addition, the top three trends are also shown over time. The ' +\
    'top three are identified by finding cumulative volume across \n' +\
    'all time by trend. The top 3 are then plotted, showing behavior.'

    #Build input file name
    def bI(self, q):
        nameI = self.projectPath + self.inputPath + self.selectQueryName(q, 'in')
        return nameI

    #Build save file and display file names
    def bF(self, q):
        reloader = self.reloader()
        #Dispaly file just needs to include static folder
        nameDF =  self.staticPath
        nameDF += self.selectQueryName(q, 'out')
        nameDF += reloader + self.ext
        #Save file needs absolute path
        nameSF =  self.projectPath + nameDF
        return nameSF, nameDF

    #Based on q, return the appropriate file name for the query.
    #io arg is for if it is input file (data source) or output file
    def selectQueryName(self, q, io):
        if io == 'in':
            if q == 1:
                qName = self.inFile1
            elif q == 2:
                qName = self.inFile2
            elif q == 3:
                qName = self.inFile3
        elif io == 'out':
            if q == 1:
                qName = self.outFile1
            elif q == 2:
                qName = self.outFile2
            elif q == 3:
                qName = self.outFile3

        return qName

    #Haven't figured out how to disable caching- this is a workaround.
    #By changing filename every time with addition of random numbers,
    #it forces browser to reload image. Works - not very elegant though...
    def reloader(self):
        return str(random.randint(0,99999999))

    def bFA(self, q):
        if q == 1:
            return [self.fig_title1, self.fig_axis1, self.fig_title1_scale, self.fig_axis1_scale, self.fig_desc1]
            #return self.fig_title1
        elif q == 2:
            return [self.fig_title2, self.fig_axis2, self.fig_desc2]
        elif q == 3:
            return [self.fig_title3, self.fig_desc3]

    def bS(self):
        sName = self.projectPath + self.staticPath
        return sName

class conf_TEST_Query():
    log_print = True
    projectPath = '/home/hduser/shared_folder/Project_3_App'
    inputPath = '/input/'
    staticPath = '/static/'
    ext = '.png'

    #Query 1 filenames
    inFile1 = 'test_t1.txt'
    outFile1 = 't1'
    fig_title1 = 'Hashtag Presence vs Followers & Friends (Spark SQL & DataFrames)'
    fig_title1_scale = 'Correlation: # vs Friends + Followers'
    fig_axis1 = ["With Hashtag","Without Hashtag"]
    fig_axis1_scale = '1:Strong | 0:None | -1:Inverted'
    fig_desc1 = 'Does friend/follower correlate with hashtage usage? '+\
    'Divide tweets into two buckets based on presence or absence of hashtag.\n'+\
    'Each bucket will hold the cumulative sum of friends and followers. '+\
    'This is shown on the pie chart.\n' +\
    'A raw count is not enough to establish correlation however. '+\
    'For this, a correlation analysis is done and is shown on the bar chart'
    #Query 2 filenames
    inFile2 = 'test_t2.txt'
    outFile2 = 't2'
    fig_title2 = 'Hashtag Volume in ReTweets - (RDD Transformations)'
    fig_axis2 = ["RTs with H#", "RTs with No H#", "New tweets with H#"]
    fig_desc2 = 'How important are tweets for hashtag trending? '+\
    'A hashtag can be used in either a new tweet or in a retweet.\n'+\
    'How much hashtag volume comes from retweets compared to new tweets?'+\
    'And out of all the retweet volume, how much of it is for a hashtag?'

    #Query 3 filenames
    inFile3 = 'test_t3.txt'
    outFile3 = 't3'
    fig_title3 = 'Total Trend Volume over Time - (Spark SQL & DataFrames)'
    fig_desc3 = 'How do trends behave over time? The main plot shows ' +\
    'cumulative volume across all trends over time.\n' +\
    'In addition, the top three trends are also shown over time. The ' +\
    'top three are identified by finding cumulative volume across \n' +\
    'all time by trend. The top 3 are then plotted, showing behavior.'

    #Build input file name
    def bI(self, q):
        nameI = self.projectPath + self.inputPath + self.selectQueryName(q, 'in')
        return nameI

    #Build save file and display file names
    def bF(self, q):
        reloader = self.reloader()
        #Dispaly file just needs to include static folder
        nameDF =  self.staticPath
        nameDF += self.selectQueryName(q, 'out')
        nameDF += reloader + self.ext
        #Save file needs absolute path
        nameSF =  self.projectPath + nameDF
        return nameSF, nameDF

    #Based on q, return the appropriate file name for the query.
    #io arg is for if it is input file (data source) or output file
    def selectQueryName(self, q, io):
        if io == 'in':
            if q == 1:
                qName = self.inFile1
            elif q == 2:
                qName = self.inFile2
            elif q == 3:
                qName = self.inFile3
        elif io == 'out':
            if q == 1:
                qName = self.outFile1
            elif q == 2:
                qName = self.outFile2
            elif q == 3:
                qName = self.outFile3

        return qName

    #Haven't figured out how to disable caching- this is a workaround.
    #By changing filename every time with addition of random numbers,
    #it forces browser to reload image. Works - not very elegant though...
    def reloader(self):
        return str(random.randint(0,99999999))

    def bFA(self, q):
        if q == 1:
            return [self.fig_title1, self.fig_axis1, self.fig_title1_scale, self.fig_axis1_scale, self.fig_desc1]
            #return self.fig_title1
        elif q == 2:
            return [self.fig_title2, self.fig_axis2, self.fig_desc2]
        elif q == 3:
            return [self.fig_title3, self.fig_desc3]

    def bS(self):
        sName = self.projectPath + self.staticPath
        return sName
