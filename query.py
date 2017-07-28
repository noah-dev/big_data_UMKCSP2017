#!/usr/bin/env python
#Initalize spark context
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

#Startup spark context
spark = SparkSession.builder.appName("Project 3") .config(conf=SparkConf()).getOrCreate()
sc = spark.sparkContext #Needed for RDD (Task 2)

from numpy import *

#Called by app.py - selects and runs a query.
#q is used to decide which query to run.
#source is used to decide which input data the query should use
#returns the query result in a list
def runQuery(q, source):
    if q == 1:
        result = qSQL_t1(source)
    elif q == 2:
        result = qRDD_t2(source)
    elif q == 3:
        result = qSQL_t3(source)
    return result
#Task 1
def qSQL_t1(source):
    #Group entries by identical entries. Users that consistently do/don't use
    #hashtags will be reduced to a single, entry. Users that are not consistent
    #will be reduced to a pair of entries, for with and without hashtag.
    q_comb = "SELECT user, has_ht, friends, followers FROM t1_csv " +\
    "GROUP BY user, has_ht, friends, followers"
    #Retrive users that only consistently do/don't use hashtags.
    #Do not include users that are not consistent.
    q_user_list = "SELECT user, COUNT(*) FROM comb " +\
    "GROUP BY user HAVING COUNT(*) = 1"
    #Join users that are consistent with the rest of the data
    q_final = "SELECT user_list.user, comb.has_ht, comb.friends +" +\
    "comb.followers AS `total` FROM user_list INNER JOIN comb "+\
    "ON user_list.user = comb.user"

    q_agg_total = "SELECT has_ht, SUM(total) AS `agg_total`" +\
    " FROM final GROUP BY has_ht ORDER BY has_ht DESC"

    df_t1 = spark.read.format("csv").option('header','true').load(source)
    df_t1.createOrReplaceTempView("t1_csv")

    df_comb = spark.sql(q_comb)
    df_comb.createOrReplaceTempView("comb")

    df_user_list = spark.sql(q_user_list)
    df_user_list.createOrReplaceTempView("user_list")

    #Join unique and duplicate consistent tables
    df_final = spark.sql(q_final)
    df_final.createOrReplaceTempView("final")

    #Prepare returning results
    #Correlation Factor, Aggregated Total and Axis (Axis added by app.py)
    result = [None,None]
    final = df_final.collect()
    has_ht = []
    total = []

    for pair in final:
        has_ht.append(int(pair[0]))
        total.append(int(pair[1]))

    #correlation calculated - store in first index of entry
    result[0] = corrcoef(has_ht,total)[1,0]

    #Aggregate results
    agg_total = spark.sql(q_agg_total).collect()
    agg_total_list = []
    for pair in agg_total:
        agg_total_list.append(int(pair[1]))
    result[1] = agg_total_list

    #Return compeleted result
    return result
#Task 2
def qRDD_t2(source):
    #Load input data into an RDD
    rdd_t2_raw = sc.textFile(source)
    #Remove header, split data by comma into columns and format as pairwise
    header = rdd_t2_raw.first()
    rdd_t2_data = rdd_t2_raw.filter(lambda x: x!= header) \
                            .map(lambda x: x.split(',')) \
                            .map(lambda x: (x[0],x[1:]))

    #Split the RDD into three buckets - one with hashtags, one without.
    #The first bucket are tweets that are retweets and have a hashtag(s)
    #The second bucket are tweets that are retweets but have no hashtag(s)
    #The third bucket are tweets that are not retweets and have no hashtag(s)
    #x[0] - retweet id. x[1][0] hashtag (empty if no hashtag).
    #x[1][1] retweet hashtag (empty if no hashtag)
    rdd_t2_b1 = rdd_t2_data.filter(lambda x: x[0] != '' and x[1][1] != '')
    rdd_t2_b2 = rdd_t2_data.filter(lambda x: x[0] != '' and x[1][1] == '')
    rdd_t2_b3 = rdd_t2_data.filter(lambda x: x[0] == '' and x[1][0] != '')

    #Do not count the same retweet multiple times. Only include the one with the
    #largest rt rt count. After reducing, only retrive the rt rt count.
    rdd_t2_b1 = rdd_t2_b1.reduceByKey(lambda a, b: max(a, b)) \
                        .map(lambda x: int(x[1][2]))
    rdd_t2_b2 = rdd_t2_b2.reduceByKey(lambda a, b: max(a, b)) \
                        .map(lambda x: int(x[1][2]))

    #Reduce results to integars
    t2_b1 = rdd_t2_b1.reduce(lambda a,b: a+b)
    t2_b2 = rdd_t2_b2.reduce(lambda a,b: a+b)
    #Only need to count for new tweets - they have no retweet retweet count
    t2_b3 = rdd_t2_b3.count()
    result = [t2_b1, t2_b2, t2_b3]

    return result
#Task 3
def qSQL_t3(source):
    #Group entries by their time, and sum the volume. Use this for main plot
    q_time = "SELECT time, Sum(volume) AS `total` FROM t3_csv GROUP BY time " +\
    "ORDER BY time"
    #Identify the top three trends by cumulative volume
    q_trend = "SELECT trend, Sum(volume) AS `total` FROM t3_csv " +\
    "GROUP BY trend ORDER BY Sum(volume) DESC LIMIT 3"
    #Join the top three trends with the main table, to find volume over time
    q_trend_time = "SELECT trend.trend, t3_csv.time, t3_csv.volume " +\
    "FROM trend INNER JOIN t3_csv ON trend.trend = t3_csv.trend"

    df_t3 = spark.read.format("csv").option('header','true').load(source)
    df_t3.createOrReplaceTempView("t3_csv")

    df_time = spark.sql(q_time)
    df_time.createOrReplaceTempView("time")

    df_trend = spark.sql(q_trend)
    df_trend.createOrReplaceTempView("trend")

    df_trend_time = spark.sql(q_trend_time)
    df_trend_time.createOrReplaceTempView("df_trend_time")

    #Prepare returning results
    #Return two lists, containing the results
    #The first list is the cumulative tweet volume from the previous 24 hours
    #The second list if the tweet volume for the top three trends from
    #the previous 24 hours
    result = [None,None]
    result = [df_time.collect(),df_trend_time.collect()]
    #Return compeleted result
    return result
