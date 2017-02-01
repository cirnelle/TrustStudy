#!/usr/local/bin/python3.4

__author__ = 'yi-linghwong'

import os
import sys
import time
import tweepy
import multiprocessing

#class GetFollowing():


def connect_to_twitter_api(i):

    ###################
    # create dict with api keys
    ###################

    lines = open(path_to_api_key_file+str(i)+'.txt', 'r').readlines()

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

    #print("Connecting to twitter API...")

    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def divide_node_list():

    lines = open(path_to_nodes_file,'r').readlines()

    users_all = []

    for line in lines:

        spline = line.rstrip('\n')
        users_all.append(spline)

    #print (len(users_all))

    n = int(len(users_all)/20) + 1
    #print (n)

    users_div_list = [users_all[i:i + n] for i in range(0, len(users_all), n)]

    #print (len(users_div_list[-1]))

    return users_div_list


def get_following_single():

    #------------------
    # connect to api's

    api = connect_to_twitter_api(4)

    # ---------------
    # get rate limit

    rate_limit = api.rate_limit_status()

    remaining = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
    reset_time = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']

    #print(remaining)

    # ---------------
    # get following

    lines = open(path_to_nodes_file, 'r').readlines()

    users = []

    for line in lines:
        spline = line.rstrip('\n')
        users.append(spline)

    # print (len(users))
    # print (users)

    retries = 5
    sleep_time = 10

    following_list = []

    users_done = []

    for u in users:

        if u not in users_done:

            t_start = time.time()

            following_list = []
            following_list.append(['0', u])

            print()
            print("-------------------------- " + u)

            time_now = time.strftime("%Y-%m-%d %H:%M")

            print("Time is: " + str(time_now))

            for n in range(retries):

                try:

                    for friend in tweepy.Cursor(api.friends, screen_name=u, count=200).items():
                        # if friend.screen_name in users:

                        # print (friend.screen_name)

                        following_list.append(['1', friend.screen_name])


                    users_done.append(u)

                    print(len(following_list))

                    t_end = time.time()
                    total_time = round(((t_end - t_start) / 60), 2)
                    print("Computing time was " + str(total_time) + " minutes.")

                    f = open(path_to_store_following_files+'0.csv', 'a')

                    for fl in following_list:
                        f.write(','.join(fl) + '\n')

                    f.close()

                    break

                except Exception as e:
                    print('Failed: ' + str(e))
                    time.sleep(sleep_time)


def get_following_multi(i):

    users = divide_node_list()[i-1]

    print (len(users))
    print (users)

    # ------------------
    # remove completed users from list
    # slice the user list from the last user on

    if os.path.isfile(path_to_store_following_files+str(i)+'.csv'):

        lines = open(path_to_store_following_files+str(i)+'.csv','r').readlines()

        users_completed = []

        for line in lines:
            spline = line.rstrip('\n').split(',')

            if spline[0] == '0':
                users_completed.append(spline[1])

        l1 = []

        for index,u in enumerate(users):

            for uc in users_completed:
                if uc == u:
                    l1.append([index,uc])

        max_element = max(l1, key=lambda x:x[0])
        max_index = max_element[0]

        users = users[max_index+1:]

        # for uc in users_completed:
        #
        #     if uc in users:
        #         users.remove(uc)

    else:

        pass

    print (len(users))
    print (users)

    # ------------------
    # connect to api's

    api = connect_to_twitter_api(i)

    # ---------------
    # get rate limit

    rate_limit = api.rate_limit_status()

    remaining = rate_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
    reset_time = rate_limit['resources']['statuses']['/statuses/user_timeline']['reset']

    #print(remaining)

    # ---------------
    # get following

    retries = 3
    sleep_time = 5

    following_list = []

    users_done = []

    for u in users:

        if u not in users_done:

            t_start = time.time()

            following_list = []
            following_list.append(['0', u])

            #print()
            #print("-------------------------- " + u)

            time_now = time.strftime("%Y-%m-%d %H:%M")

            #print("Time is: " + str(time_now))

            for n in range(retries):

                try:

                    for friend in tweepy.Cursor(api.friends, screen_name=u, count=200).items(10000):
                        # if friend.screen_name in users:

                            #print (friend.screen_name)

                        following_list.append(['1', friend.screen_name])

                    users_done.append(u)

                    #print(len(following_list))

                    t_end = time.time()
                    total_time = round(((t_end - t_start) / 60), 2)
                    #print("Computing time was " + str(total_time) + " minutes.")

                    f = open(path_to_store_following_files+str(i)+'.csv', 'a')

                    for fl in following_list:
                        f.write(','.join(fl) + '\n')

                    f.close()

                    break

                except Exception as e:

                    print('Failed: ' + str(e))

                    if str(e) == 'Twitter error response: status code = 401':
                        users_done.append(u)
                        break

                    if str(e) == 'Twitter error response: status code = 404':
                        users_done.append(u)
                        break

                    time.sleep(sleep_time)


################
# variables
################

path_to_nodes_file = '../output/network/nodes/3_18nov-18dec/nodes_without_following.csv'

# following files
path_to_store_following_files = '/Users/yi-linghwong/GitHub/_big_files/twitter/TrustStudy/3_18nov-18dec/following/space_following_'

# api keys
path_to_api_key_file = '/Users/yi-linghwong/keys/twitter_key_'



if __name__ == '__main__':


    #divide_node_list()

    #get_following_single()

    #get_following_multi()

    #--------------------
    # multiprocessing

    threads_1 = 20

    jobs = []

    for n in range(1,threads_1+1):

        print (n)

        getfoll = multiprocessing.Process(name='getfoll_'+str(n), target=get_following_multi, args=(n,))
        jobs.append(getfoll)

    for j in jobs:
        print (j)
        j.start()

    #---------------

    # threads_2 = 16
    #
    # jobs = []
    #
    # for n in range(11, threads_2 + 1):
    #     print(n)
    #
    #     getfoll = multiprocessing.Process(name='getfoll_' + str(n), target=get_following_multi, args=(n,))
    #     jobs.append(getfoll)
    #
    # for j in jobs:
    #     print(j)
    #     j.start()


