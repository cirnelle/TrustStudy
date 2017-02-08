__author__ = 'yi-linghwong'

import os
import sys
import time
import tweepy
import json
import multiprocessing


def connect_to_twitter_api(i):

    lines = open(path_to_twitter_api_key+str(i)+'.txt', 'r').readlines()

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

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def divide_node_list():

    lines = open(path_to_node_list, 'r').readlines()

    node_list = []

    for line in lines:
        spline = line.rstrip('\n')
        node_list.append(spline)

    n = int(len(node_list) / 20) + 1
    # print (n)

    node_div_list = [node_list[i:i + n] for i in range(0, len(node_list), n)]

    return node_div_list


def get_timeline_tweets(i):

    api = connect_to_twitter_api(i)

    users = divide_node_list()[i-1]

    print ("Length of nodes for "+str(i)+": ",len(users))
    print (users)

    #users = ['yilinghwong']

    tweets = []

    for u in users:

        print (u)

        user_tweets = []
        description = []

        try:


            #---------------------------------
            # Uncomment the following if want to get profile description too
            #---------------------------------

            profile = api.get_user(screen_name=u)

            description.append([u, profile.description.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(',', ' ')])

            f = open(path_to_store_user_profile_description_file,'a')

            for d in description:
                f.write(','.join(d)+'\n')

            f.close()

            #----------------------------------

            tweets = tweepy.Cursor(api.user_timeline, id=u, include_rts=False, exclude_replies=True, count=200).items(3200)

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

                user_tweets.append([u, data['created_at'], data['id_str'], str(data['user']['followers_count']),
                                    str(data['user']['friends_count']), str(data['retweet_count']),
                                    str(data['favorite_count']), 'has_' + type,
                                    data['text'].replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace(',',
                                                                                                                 ' ')])


            #################
            # write (append) data to file for each user
            #################

            f = open(path_to_store_timeline_tweets+str(i+20)+'.csv', 'a')

            for ut in user_tweets:
                f.write(','.join(ut) + '\n')


        except Exception as e:

            print ("Failed: " + str(e))



##############
# variables
##############

path_to_twitter_api_key = '/Users/yi-linghwong/keys/twitter_api_'
path_to_node_list = '../output/network/nodes/1_18sep-18oct/nodes_new.csv'

path_to_store_user_profile_description_file = '../output/profile_description/1_18sep-18oct/profile_6.csv'
path_to_store_timeline_tweets = '../output/timeline_tweets/1_18sep-18oct/timeline_tweets_'


if __name__ == '__main__':

    threads_1 = 20

    jobs = []

    for n in range(1, threads_1 + 1):
        print(n)

        getfoll = multiprocessing.Process(name='gettimeline_' + str(n), target=get_timeline_tweets, args=(n,))
        jobs.append(getfoll)

    for j in jobs:
        print(j)
        j.start()