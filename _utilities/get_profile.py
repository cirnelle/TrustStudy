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


def divide_public_node_list():

    lines1 = open(path_to_space_user_list, 'r').readlines()
    lines2 = open(path_to_filtered_nodes, 'r').readlines()

    scientist_list = []

    for line in lines1:
        spline = line.rstrip('\n').split(',')

        scientist_list.append(spline[0].lower())

    scientists = []
    public = []

    for line in lines2:
        spline = line.rstrip('\n').split(',')

        if spline[0].lower() in scientist_list:
            scientists.append(spline[0].lower())

        else:
            public.append(spline[0].lower())


    n = int(len(public) / 5) + 1
    # print (n)

    public_div_list = [public[i:i + n] for i in range(0, len(public), n)]

    return public_div_list


def get_twitter_profile(i):

    api = connect_to_twitter_api(i+33)

    public_users = divide_public_node_list()[i-1]

    print ("Length of nodes for "+str(i)+": ",len(public_users))
    print (public_users)

    #public_users = ['yilinghwong']

    descriptions = []

    for pu in public_users:

        #print (pu)

        try:

            profile = api.get_user(screen_name = pu)

            descriptions.append([pu,profile.description.replace('\n', ' ').replace('\r', ' ').replace('\t',' ').replace(',', ' ')])

            if len(descriptions) > 99:

                #print ("aha")

                f = open(path_to_store_user_profile_description_file+str(i)+'.csv','a')

                for d in descriptions:

                    f.write(','.join(d)+'\n')

                f.close()

                descriptions = []


        except Exception as e:

            print ("Failed: " + str(e))

    # need the following lines to write to file the remaining items in description list

    f = open(path_to_store_user_profile_description_file + str(i) + '.csv', 'a')

    for d in descriptions:
        f.write(','.join(d)+'\n')

    f.close()



##############
# variables
##############

path_to_twitter_api_key = '/Users/yi-linghwong/keys/twitter_api_keys_'
path_to_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'

path_to_store_user_profile_description_file = '../output/profile_description/1_18sep-18oct/filtered_nodes/profile_'


if __name__ == '__main__':

    threads_1 = 5

    jobs = []

    for n in range(1, threads_1 + 1):
        print(n)

        getfoll = multiprocessing.Process(name='getprofile_' + str(n), target=get_twitter_profile, args=(n,))
        jobs.append(getfoll)

    for j in jobs:
        print(j)
        j.start()