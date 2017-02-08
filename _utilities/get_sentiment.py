__author__ = 'yi-linghwong'

import os
import sys
import threading
import subprocess

class GetSentiment():

    def run_sentistrength(self):

        lines = open(path_to_raw_tweets,'r').readlines()

        tweets = []

        for line in lines:
            spline = line.rstrip('\n').split(',')

            #self.run_sentistrength((spline[-1]))

            tweets.append(spline[-1])

        print ("Length of tweet list is "+str(len(tweets)))

        f = open(path_to_store_tweets_only_file,'w')

        for t in tweets:

            f.write(t+'\n')

        f.close()

        #------------------
        # run sentistrength


        command = ["java", "-jar", "/Users/yi-linghwong/GitHub/data_files/SentiStrength/SentiStrengthCom.jar",
                   "sentidata",
                   "/Users/yi-linghwong/GitHub/data_files/SentiStrength/SentStrength_Data_December2015English/",
                   "input", path_to_store_tweets_only_file, "outputFolder", path_to_folder_to_store_sentistrength_output,
                   "sentenceCombineTot", "paragraphCombineTot", "binary", "negativeMultiplier", "0.01"] #use '1' or '1.5' for negative multiplier for p@s tweets; use '0.01' for s@s and s@p tweets

        subprocess.Popen(command)


    def create_tweet_file_with_sentiment(self):


        #lines = open(path_to_folder_to_store_sentistrength_output+'public_@scientist_filtered0_out.txt','r').readlines()
        #lines = open(path_to_folder_to_store_sentistrength_output + 'scientist_@public_ALL0_out.txt','r').readlines()#remember to change file name!
        lines = open(path_to_folder_to_store_sentistrength_output + 'scientist_@scientist_ALL0_out.txt', 'r').readlines()

        print ("Length of sentistrength output tweet list is "+str(len(lines)-1))

        sentiments = []
        senti_neg = []
        senti_pos = []

        for line in lines[1:]:

            spline = line.rstrip('\n').split('\t')

            if spline[0] == '1':
                sentiments.append('+')
                senti_pos.append('pos')

            elif spline[0] == '-1':
                sentiments.append('-')
                senti_neg.append('neg')

            else:
                print("error")

        print ("Length of positive sentiment: "+str(len(senti_pos)))
        print ("Length of negative sentiment: "+str(len(senti_neg)))

        print ("Total length is: "+str(len(sentiments)))

        #----------------------
        # update tweet file with sentiment

        lines1 = open(path_to_raw_tweets,'r').readlines()

        tweets_ori = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            tweets_ori.append(spline)


        if len(tweets_ori) == len(sentiments):

            zipped = zip(tweets_ori,sentiments)

            tweets_with_sentiment = []

            for z in zipped:
                z = list(z)

                flatten_list = [item for sublist in z for item in sublist]

                if (flatten_list[-1]) == '+':
                    flatten_list[-1] = 'pos'

                elif(flatten_list[-1]) == '-':
                    flatten_list[-1] = 'neg'

                else:
                    print ("error")

                length = len(flatten_list)

                flatten_list[length-1],flatten_list[length-2] = flatten_list[length-2],flatten_list[length-1]

                tweets_with_sentiment.append(flatten_list)


            print ("Length of tweets with sentiment is: "+str(len(tweets_with_sentiment)))

            f = open(path_to_store_raw_tweet_file_with_sentiment,'w')

            for ts in tweets_with_sentiment:
                f.write(','.join(ts)+'\n')

            f.close()

        else:
            print ("Lists length not equal, exiting...")
            sys.exit()



################
# variables
################

#path_to_raw_tweets = '../tweets/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist_filtered.csv'
#path_to_raw_tweets = '../tweets/scientist_mention_public/1_18sep-18oct/scientist_@public_ALL.csv'
path_to_raw_tweets = '../tweets/scientist_mention_scientist/1_18sep-18oct/scientist_@scientist_ALL.csv'

#path_to_store_tweets_only_file = '../output/sentistrength/source_tweet/1_18sep-18oct/public_@scientist_filtered.csv'
#path_to_store_tweets_only_file = '../output/sentistrength/source_tweet/1_18sep-18oct/scientist_@public_ALL.csv'
path_to_store_tweets_only_file = '../output/sentistrength/source_tweet/1_18sep-18oct/scientist_@scientist_ALL.csv'

path_to_folder_to_store_sentistrength_output = '../output/sentistrength/sentistrength_output/1_18sep-18oct/'

#path_to_store_raw_tweet_file_with_sentiment = '../tweets/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist_sentiment.csv'
#path_to_store_raw_tweet_file_with_sentiment = '../tweets/scientist_mention_public/1_18sep-18oct/scientist_@public_sentiment.csv'
path_to_store_raw_tweet_file_with_sentiment = '../tweets/scientist_mention_scientist/1_18sep-18oct/scientist_@scientist_sentiment.csv'


if __name__ == '__main__':

    gs = GetSentiment()

    #gs.run_sentistrength() #NOTE: for s@s and s@p tweets, run this, but then MANUALLY replace all -1 sentiment with 1!

    gs.create_tweet_file_with_sentiment() #IMPORTANT: remember to change file name in function!!
