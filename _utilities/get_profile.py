__author__ = 'yi-linghwong'

import os
import sys
import time
import tweepy
import json

class GetProfile():

    def connect_to_twitter_api(self):

        lines = open(path_to_twitter_api_key, 'r').readlines()

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


    def get_public_node(self):

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

        # print (scientists)
        # print (public)

        return public


    def get_twitter_profile(self):

        api = self.connect_to_twitter_api()

        public_users = self.get_public_node()

        print ("Length of nodes: ",len(public_users))

        #public_users = ['yilinghwong']

        descriptions = []

        t_start = time.time()

        print ("Collecting profile descriptions...")


        for pu in public_users:

            print (pu)

            try:

                profile = api.get_user(screen_name = pu)

                descriptions.append([pu,profile.description.replace('\n', ' ').replace('\r', ' ').replace('\t',' ').replace(',', ' ')])

                if (len(descriptions) == 100:

                    pass
                    
                    # write to file
                    # descriptions = []


            except Exception as e:

                print ("Failed: " + str(e))

        #print ("Length of profile nodes: ", len(descriptions))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print ()
        print("Computing time was " + str(total_time) + " minutes.")


        f = open(path_to_store_user_profile_description_file,'w')

        for d in descriptions:
            f.write(','.join(d)+'\n')

        f.close()





##############
# variables
##############

path_to_twitter_api_key = '/Users/yi-linghwong/keys/twitter_api_keys_34.txt'
path_to_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'

path_to_store_user_profile_description_file = '../output/profile_description/profile_1_18sep-18oct.csv'


if __name__ == '__main__':

    gp = GetProfile()

    gp.get_twitter_profile()