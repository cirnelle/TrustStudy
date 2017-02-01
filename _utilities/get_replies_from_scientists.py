__author__ = 'yi-linghwong'

import os
import sys
import tweepy
import time
import json
import re
import multiprocessing



def connect_to_twitter_api(i):

    ###################
    # create dict with api keys
    ###################

    lines = open(path_to_api_key_file + str(i) + '.txt', 'r').readlines()

    api_dict = {}

    for line in lines:
        spline = line.replace("\n", "").split()

        api_dict[spline[0]] = spline[1]

    apikey = api_dict["API_key"]
    apisecret = api_dict["API_secret"]

    AccessToken = api_dict["Access_token"]
    AccessTokenSecret = api_dict["Access_token_secret"]

    auth = tweepy.OAuthHandler(apikey, apisecret)
    auth.set_access_token(AccessToken, AccessTokenSecret)

    print("Connecting to twitter API...")

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def get_scientist_and_public_list():

    lines1 = open(path_to_scientist_list,'r').readlines()
    lines2 = open(path_to_filtered_node_list,'r').readlines()

    scientists_all = []

    for line in lines1:
        spline = line.rstrip('\n').split(',')
        scientists_all.append(spline[0].lower())

    #print (len(scientists))

    public = []
    scientists = []

    for line in lines2:
        spline = line.rstrip('\n')

        if spline.lower() not in scientists_all:
            public.append(spline)

        elif spline.lower() in scientists_all:
            scientists.append(spline.lower())

    #print (len(public))

    return scientists,public


def divide_scientist_list():

    #lines = open(path_to_scientist_list, 'r').readlines()
    scientists = get_scientist_and_public_list()[0]

    n = int(len(scientists) / 5) + 1
    # print (n)

    users_div_list = [scientists[i:i + n] for i in range(0, len(scientists), n)]

    print (len(users_div_list))

    # print (len(users_div_list[-1]))

    return users_div_list


def get_replies(i):

    #-------------------
    # get list of public user

    public_users = get_scientist_and_public_list()[1]

    # print (len(public_users))
    # print (public_users)

    #-------------------
    # get list of scientist

    scientists = divide_scientist_list()[i-1]

    # print (len(scientists))
    # print (scientists)

    # ------------------
    # connect to api's

    api = connect_to_twitter_api(i+28)

    retries = 5
    sleep_time = 10


    #public_users = ['yilinghwong','NASA']
    #scientists = ['concupiscentia_']

    for user in scientists:

        #print("Getting tweets for " + str(user))

        user_tweets = []

        for r in range(retries):

            try:

                rate_limit = api.rate_limit_status()

                remaining = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
                reset_time = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']

                #print(remaining)

                ##################
                # get tweets with twitter user_timeline, excluding RTs and Replies
                ##################

                tweets = tweepy.Cursor(api.user_timeline, id=user, include_rts=False, exclude_replies=False, count=200).items(
                    3200)

                for t in tweets:

                    # dumps serialises strings into JSON (which is very similar to python's dict)
                    json_str = json.dumps(t._json)

                    # loads deserialises a string and create a python dict, i.e. it parses the JSON to create a python dict
                    data = json.loads(json_str)

                    #################
                    # check if media exists, and which type
                    #################

                    if 'extended_entities' in data:

                        if 'media' in data['extended_entities']:

                            if data['extended_entities']['media'] != []:

                                length = len(data['extended_entities']['media'])

                                for n in range(length):
                                    type = data['extended_entities']['media'][n]['type']


                    elif 'entities' in data:

                        if 'urls' in data['entities']:

                            if (data['entities']['urls'] != []):

                                length = len(data['entities']['urls'])

                                for n in range(length):

                                    if (data['entities']['urls'][n]['display_url'].startswith('youtu')):
                                        type = 'video'
                                        break

                                    elif (data['entities']['urls'][n]['display_url'].startswith('vine')):
                                        type = 'video'
                                        break

                                    elif (data['entities']['urls'][n]['display_url'].startswith('amp.twimg')):
                                        type = 'video'
                                        break

                                    elif (data['entities']['urls'][n]['display_url'].startswith('snpy.tv')):
                                        type = 'video'
                                        break

                                    elif (data['entities']['urls'][n]['display_url'].startswith('vimeo')):
                                        type = 'video'
                                        break

                                    else:
                                        type = 'no_media'

                            else:
                                type = 'no_media'

                        else:
                            type = 'no_media'

                    else:
                        type = 'no_media'

                    ################
                    # append list of parameters to tweet list
                    ################

                    tweet_text = ' '+data['text'].replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(',', ' ').lower()+' '
                    #print (tweet_text)

                    mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

                    for pu in public_users:
                        public_user = '@' + (str(pu)).lower()

                        if public_user in mention_list:

                            user_tweets.append(
                                [user, data['created_at'], data['id_str'], str(data['user']['followers_count']),
                                 str(data['user']['friends_count']), str(data['retweet_count']),
                                 str(data['favorite_count']), 'has_' + type,
                                 data['text'].replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(',', ' ')])

                #################
                # write (append) data to file for each user
                #################

                f = open(path_to_folder_to_store_replies+str(i)+'.csv', 'a')

                # if file is empty create heading

                for ut in user_tweets:
                    f.write(','.join(ut) + '\n')


                break

            except Exception as e:
                print('Failed: ' + str(e))
                time.sleep(sleep_time)


def combine_tweets(self):

    lines1 = open(path_to_folder_to_store_replies + '1.csv', 'r').readlines()
    lines2 = open(path_to_folder_to_store_replies + '2.csv', 'r').readlines()
    lines3 = open(path_to_folder_to_store_replies + '3.csv', 'r').readlines()
    lines4 = open(path_to_folder_to_store_replies + '4.csv', 'r').readlines()
    lines5 = open(path_to_folder_to_store_replies + '5.csv', 'r').readlines()

    lines = lines1 + lines2 + lines3 + lines4 + lines5

    print(len(lines))

    tweets_containing_public = []
    id_list = []

    for line in lines:
        spline = line.rstrip('\n').split(',')

        if spline[2] not in id_list:
            id_list.append(spline[2])
            tweets_containing_public.append(spline)

    print(len(tweets_containing_public))

    f = open(path_to_store_combined_tweets, 'w')

    for tc in tweets_containing_public:
        f.write(','.join(tc) + '\n')

    f.close()


################
# variables
################

path_to_api_key_file = '/Users/yi-linghwong/keys/twitter_api_keys_'
path_to_scientist_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_filtered_node_list = '../output/network/nodes/nodes_filtered.csv'

path_to_folder_to_store_replies = '../tweets/mentions/scientist_mention_public/scientist_replies_'

path_to_store_combined_tweets = '../tweets/mentions/scientist_mention_public/scientist_@public.csv'


if __name__ == '__main__':

    #################
    # collect scientist tweets
    #################

    threads = 5

    jobs = []

    for n in range(1, threads + 1):

        print(n)

        getreplies = multiprocessing.Process(name='getreplies_' + str(n), target=get_replies, args=(n,))
        jobs.append(getreplies)

    for j in jobs:
        print(j)
        j.start()


    #################
    # combine tweets
    #################

    #combine_tweets()


