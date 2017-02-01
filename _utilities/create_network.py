__author__ = 'yi-linghwong'

import os
import sys
import tweepy
import networkx as nx
import subprocess
import time
import re
from collections import defaultdict
import multiprocessing
from itertools import groupby


#-----------------
# get Twitter API keys


class CreateTwitterNetwork():

    def __init__(self):

        print ("Welcome")


    def get_tweets_mentioning_scientists(self):

        lines1_1 = open(path_to_raw_unique_tweets_file,'r').readlines()
        lines1_2 = open(path_to_raw_unique_tweets_file_1, 'r').readlines()

        lines1 = lines1_1 + lines1_2

        #lines1 = open(path_to_raw_unique_tweets_file, 'r').readlines()
        lines2 = open(path_to_seed_space_user_list,'r').readlines()

        space_users = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            space_users.append(spline[0])

        print ("Length of scientist list is "+str(len(space_users)))

        tweets_containing_scientist = []
        id_list = []

        print ("Getting tweets with @scientist mentions ...")

        t_start = time.time()

        for line in lines1:
            spline = line.rstrip('\n').split(',')

            tweet_text = ' ' + spline[-1].lower() + ' '

            mention_list =  (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            for su in space_users:
                space_user = '@' + (str(su)).lower()

                if space_user in mention_list:

                    if spline[2] not in id_list:

                        id_list.append(spline[2])

                        tweets_containing_scientist.append(spline)

            ##############
            # ALTERNATIVE (slower)
            ##############

            # for su in space_users:
            #
            #     space_user = ' @' + (str(su)).lower() + ' '
            #
            #     if space_user in str(tweet_text):
            #
            #         tweets_containing_scientist.append(spline)

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        print ()
        print ("Length of raw tweet list is "+str(len(lines1)))
        print ("Length of tweet containing scientist is "+str(len(tweets_containing_scientist)))

        f = open(path_to_store_tweets_with_scientist_mention,'w')

        for tc in tweets_containing_scientist:
            f.write(','.join(tc)+'\n')

        f.close()


    def get_unique_nodes(self):

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_store_tweets_with_scientist_mention, 'r').readlines()

        scientist_list = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            scientist_list.append(spline[0])

        nodes = []

        for line in lines2:

            spline = line.rstrip('\n').split(',')
            tweet_text = ' ' + spline[-1].lower() + ' '

            mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            for sl in scientist_list:
                space_user = '@' + (str(sl)).lower()

                if space_user in mention_list:

                    if spline[0].lower() not in nodes:

                        nodes.append(spline[0].lower())

                    if sl.lower() not in nodes:

                        nodes.append(sl.lower())

        print ("Length of extracted nodes is "+str(len(nodes)))

        f = open(path_to_store_nodes, 'w')

        for n in nodes:
            f.write(n + '\n')

        f.close()


    def get_nodes_without_following(self):

        ################
        # filter out nodes that so far do not have their following list extracted yet
        # so that we don't have to extract their following again as it takes a lot of time
        ################

        lines1 = open(path_to_store_nodes,'r').readlines()
        lines2 = open('../output/network/nodes/1_18sep-18oct/nodes_filtered.csv','r').readlines()

        nodes_with_following = [] # nodes whose following list has already been extracted

        for line in lines2:
            spline = line.rstrip('\n')
            nodes_with_following.append(spline)

        print ("Length of nodes with following list extracted: "+str(len(nodes_with_following)))

        nodes_without_following = []
        duplicates = [] # nodes present in both lists, so their following list do not need to be extracted anymore

        for line in lines1:
            spline = line.rstrip('\n')

            if spline.lower() not in nodes_with_following:
                nodes_without_following.append(spline)

            else:
                duplicates.append(spline.lower())

        print ("Length of nodes without following list: "+str(len(nodes_without_following)))
        print ("Length of duplicated nodes: "+str(len(duplicates)))
        #print (duplicates[:10])

        f = open(path_to_store_nodes_without_following,'w')

        for nw in nodes_without_following:
            f.write(nw+'\n')

        f.close()

        f = open(path_to_store_nodes_with_following,'w')

        for d in duplicates:
            f.write(d+'\n')

        f.close()


    def get_following_list_for_duplicated_nodes(self):

        ##################
        # extract the following list for the duplicated nodes
        ##################

        lines = open(path_to_store_nodes_with_following,'r').readlines()

        nodes_with_following = []

        t_start = time.time()

        for line in lines:
            spline = line.rstrip('\n')
            nodes_with_following.append(spline)

        print ("Length of duplicated nodes: "+str(len(nodes_with_following)))

        #-----------------------
        # get a list of lists with node as first item and following as the next items
        # i.e. [[nasa, abc, def],[esa, ghi]]

        pairs = [] # want to get pairs = [[0,'nasa'],[1,'abc'],[1,'def'],[0,'esa'],[1,'ghi']]

        nodes = []

        for n in range(1,21):

            print (n)

            lines = open('/Users/yi-linghwong/GitHub/_big_files/twitter/TrustStudy/1_18sep-18oct/following/space_following_'+str(n)+'.csv','r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')
                l = [int(spline[0]),spline[1]]
                pairs.append(l) # pairs = [[0,'nasa'],[1,'abc'],[1,'def'],[0,'esa'],[1,'ghi']]

        print ()
        print ("Length of whole following list for oct-nov nodes: "+str(len(pairs)))

        #pairs = [[0,'ab'],[1,'cd'],[1,'ef'],[0,'gh'],[1,'ij'],[0,'kl'],[0,'etc'],[1,'mn'],[1,'op'],[1,'qr']]

        following_list = [] # want result to be [[nasa, abc, def],[esa, ghi]], i.e. first element of each list is the node
        temp = []
        checker = 0

        for item in pairs:

            if item[0] == checker:

                if checker == 1:
                    checker = item[0]
                    temp.append(item[1])

                elif checker == 0:
                    if temp == []:
                        checker = item[0]
                        temp.append(item[1])

                    else:
                        checker = item[0]
                        following_list.append(temp)
                        temp = []
                        temp.append(item[1])

            elif item[0] > checker:
                checker = item[0]
                temp.append(item[1])

            else:
                following_list.append(temp)
                checker = 0
                temp = []
                temp.append(item[1])

        following_list.append(temp) # so that the last node (and its following) in the list will be appended too

        print (len(following_list))


        #---------------
        # get the following list of the nodes that are in the duplicated list

        #nodes_with_following = ['ab','kl']

        following = []
        dup = []

        for fl in following_list:

            if fl[0].lower() in nodes_with_following:

                following.append(['0',fl[0]])
                dup.append(fl[0])

                for f in fl[1:]:

                    following.append(['1',f])

        print("Length of duplicated nodes: ",len(dup))
        print ("Length of following list for duplicated nodes: "+str(len(following)))

        f = open(path_to_following_list_folder+'21.csv','w')

        for fo in following:

            f.write(','.join(fo)+'\n')

        f.close()

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


    def get_filtered_nodes(self):

        ###############
        # get the list of remaining scientist and public from the node list (after getting the following for all nodes)
        # to filter out nodes whose accounts are protected/suspended/cancelled
        ###############

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_store_nodes, 'r').readlines()

        valid_nodes = []

        print ("Getting valid nodes ...")

        for n in range(1, 21):


            lines = open('/Users/yi-linghwong/GitHub/_big_files/twitter/TrustStudy/1_18sep-18oct/following/space_following_'+ str(n) + '.csv', 'r').readlines()
            #lines = open(path_to_following_list_folder + str(n) + '.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                if spline[0] == '0':
                    valid_nodes.append(spline[1].lower())

        print ()
        print ("Number of original nodes is "+str(len(lines2)))
        print("Number of filtered nodes is " + str(len(valid_nodes)))
        print ()

        scientists = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')

            if spline[0].lower() in valid_nodes:  # filter out nodes that we cannot get following for

                scientists.append(spline[0].lower())

        # print(len(scientists))

        print (scientists)

        public = []

        for line in lines2:
            spline = line.rstrip('\n')

            if spline.lower() not in scientists:

                if spline.lower() in valid_nodes:  # filter out nodes that we cannot get following for

                    public.append(spline.lower())

        # print(len(public))

        print ("Length of filtered scientist list is: "+str(len(scientists)))
        print ("Length of filtered public list is "+str(len(public)))

        f = open(path_to_store_filtered_nodes, 'w')

        for s in scientists:
            f.write(s + '\n')

        for p in public:
            f.write(p + '\n')

        f.close()


    def filter_out_scientists_from_public_list(self):

        ###############
        # filter out additional scientist from node list based on their profile description
        ###############

        lines = open(path_to_profile_description_file,'r').readlines()




    path_to_store_seed_and_additional_space_user_list


    def get_scientist_and_public_list(self):

        ###############
        # get the list of remaining scientist and public from the node list (after getting the following for all nodes)
        # to filter out nodes whose accounts are protected/suspended/cancelled
        ###############

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_store_filtered_nodes, 'r').readlines()

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

        #print ("Length of scientist list is: "+str(len(scientists)))
        #print ("Length of public list is: "+str(len(public)))


        return scientists, public


    def extract_tweets_for_filtered_nodes(self):

        ####################
        # extract public @scientist tweets from raw tweet file for filtered nodes
        ####################

        lines1 = open(path_to_store_tweets_with_scientist_mention,'r').readlines()

        print("Length of tweets before filtering: " + str(len(lines1)))

        public = self.get_scientist_and_public_list()[1]

        filtered_tweets = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')

            if spline[0].lower() in public:
                filtered_tweets.append(spline)

        print ("Length of tweets after filtering: "+str(len(filtered_tweets)))

        f = open(path_to_store_tweets_with_scientist_mention_filtered,'w')

        for ft in filtered_tweets:

            f.write(','.join(ft)+'\n')

        f.close()


    def create_network_mentions(self):

        DG1 = nx.MultiDiGraph() # public mention scientist
        DG2 = nx.MultiDiGraph()  # scientist mention public
        DG3 = nx.MultiDiGraph() # combined mentions

        DG_1 = nx.MultiDiGraph() # FOR GEPHI: public mention scientist
        DG_2 = nx.MultiDiGraph()  # FOR GEPHI: scientist mention public
        DG_3 = nx.MultiDiGraph() # FOR GEPHI: combined mentions

        #####################
        # get nodes and edges for public mentions of scientists
        #####################

        lines = open(path_to_public_mention_scientist_tweets_with_sentiment,'r').readlines()

        scientists = self.get_scientist_and_public_list()[0]

        scientist_list = []

        for s in scientists:
            scientist_list.append('@'+s.lower())

        #print (scientist_list)

        edges_pos = []
        edges_neg = []
        nodes = []
        user_all = [] #not all tweets contain mention of a scientist, some lines are truncated or are RT, but we want to keep a list of all users

        print ("Creating edges and nodes (public mention scientist)...")

        t_start = time.time()

        for line in lines:

            spline = line.rstrip('\n').split(',')
            tweet_text = ' '+spline[-1].lower()+' '

            user_all.append(spline[0])

            mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            for ml in mention_list:

                if ml in scientist_list:
                    public_user = spline[0].lower()
                    scientist = ml.replace('@','')

                    if spline[0].lower() not in nodes:
                        nodes.append(spline[0].lower())

                    if scientist.lower() not in nodes:
                        nodes.append(scientist.lower())

                    # get sentiment to get sign of edges

                    if spline[-2] == 'pos':

                        edges_pos.append([public_user,scientist])

                    elif spline[-2] == 'neg':

                        edges_neg.append([public_user,scientist])

                    else:
                        print ("error")


        print ("Number of positive tweets (public @scientist): "+str(len(edges_pos)))
        print ("Number of negative tweets (public @scientist): "+str(len(edges_neg)))
        print("Number of total edges (public @scientist): " + str(len(edges_pos+edges_neg)))
        print ("Number of nodes: "+str(len(nodes)))
        print("Number of total user: "+str(len(user_all)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        DG1.add_edges_from(edges_pos,sign='+')
        DG1.add_edges_from(edges_neg,sign='-')
        DG1.add_nodes_from(nodes)

        # ----------------------
        # CREATE GEPHI GRAPH:
        # sum up signs (if > 0 then positive, if < 0 then negative) if parallel edges exist (ONLY for Gephi, as it doesn't accept parallel edges)
        # if the sum is zero, default to negative

        print ()
        print ("Creating GEPHI graph 1 (public @scientist)...")

        t_start = time.time()

        edges_all = edges_pos + edges_neg

        edges_set = set(map(tuple, edges_all))  # result: {[1,2], [3,4]}
        edges_unique_tuple = list(edges_set)  # result: [(1,2), (3,4)]
        edges_unique = [list(eu) for eu in edges_unique_tuple]  # convert list of tuples to list of list


        # print(len(edges_unique))
        # print (edges_unique)

        edges_unique_sum_pos = []
        edges_unique_sum_neg = []

        for eu in edges_unique:
            count_pos = edges_pos.count(eu)
            count_neg = edges_neg.count(eu)
            count = count_pos - count_neg

            if count > 0:
                edges_unique_sum_pos.append([eu[0], eu[1], count])

            if count <= 0:
                edges_unique_sum_neg.append([eu[0], eu[1], count])

        #print(len(edges_unique_sum_pos) + len(edges_unique_sum_neg))

        for eup in edges_unique_sum_pos:
            DG_1.add_edges_from([(eup[0], eup[1])], sign='+', sentiment=eup[2])

        for eun in edges_unique_sum_neg:
            DG_1.add_edges_from([(eun[0], eun[1])], sign='-', sentiment=eun[2])

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        nx.write_gexf(DG_1, path_to_store_public_mention_scientist_graph)

        #------------------------

        # write to file

        f = open(path_to_store_public_mention_scientist_edges, 'w')

        for ep in edges_pos:
            f.write(','.join(ep)+',pos'+'\n')

        for en in edges_neg:
            f.write(','.join(en) + ',neg' + '\n')

        f.close()

        #####################
        # get nodes and edges for scientist mentions of public
        #####################

        print ()
        print ('----------------------------')

        lines1 = open(path_to_scientist_mention_public_tweets_with_sentiment, 'r').readlines()

        public = self.get_scientist_and_public_list()[1]

        public_list = []

        for p in public:
            public_list.append('@'+p.lower())


        print("Creating edges and nodes (scientist mention public)...")

        edges_pos_1 = []
        edges_neg_1 = []


        t_start = time.time()

        for line in lines1:

            spline = line.rstrip('\n').split(',')
            tweet_text = ' ' + spline[-1].lower() + ' '

            mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            for ml in mention_list:

                if ml in public_list:
                    scientist_user = spline[0].lower()
                    public_person = ml.replace('@','')

                    if spline[0].lower() not in nodes:
                        print ("check")
                        print (spline[0])
                        nodes.append(spline[0].lower())

                    if public_person.lower() not in nodes:
                        print ("check2")
                        print (public_person)
                        nodes.append(public_person.lower())

                    # get sentiment to get sign of edges

                    if spline[-2] == 'pos':

                        edges_pos.append([scientist_user, public_person])
                        edges_pos_1.append([scientist_user, public_person])

                    elif spline[-2] == 'neg':

                        edges_neg.append([scientist_user, public_person])
                        edges_neg_1.append([scientist_user, public_person])

                    else:
                        print("error")


        print("Number of positive tweets (scientist @public): " + str(len(edges_pos_1)))
        print("Number of negative tweets (scientist @public): " + str(len(edges_neg_1)))
        print("Number of total edges (scientist @public): " + str(len(edges_pos_1 + edges_neg_1)))
        print("Number of nodes: " + str(len(nodes)))


        print ()
        print("Number of COMBINED positive tweets: " + str(len(edges_pos)))
        print("Number of COMBINED negative tweets: " + str(len(edges_neg)))
        print("Number of COMBINED edges: " + str(len(edges_pos + edges_neg)))
        print("Number of nodes: " + str(len(nodes)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        # write scientist mention public graph

        DG2.add_edges_from(edges_pos_1, sign='+')
        DG2.add_edges_from(edges_neg_1, sign='-')
        DG2.add_nodes_from(nodes)

        DG3.add_edges_from(edges_pos, sign='+')
        DG3.add_edges_from(edges_neg, sign='-')
        DG3.add_nodes_from(nodes)


        # ----------------------
        # CREATE GEPHI GRAPH:
        # sum up signs (if > 0 then positive, if < 0 then negative) if parallel edges exist (ONLY for Gephi, as it doesn't accept parallel edges)
        # if the sum is zero, default to negative

        # ---------------- scientist mention public graph ---------------- #

        print ()
        print("Creating GEPHI graph 2 (scientist @public) ...")

        t_start = time.time()

        edges_all_1 = edges_pos_1 + edges_neg_1

        edges_set_1 = set(map(tuple, edges_all_1))  # result: {[1,2], [3,4]}
        edges_unique_tuple_1 = list(edges_set_1)  # result: [(1,2), (3,4)]
        edges_unique_1 = [list(eu) for eu in edges_unique_tuple_1]  # convert list of tuples to list of list

        # print(len(edges_unique_1))
        # print (edges_unique_1)

        edges_unique_sum_pos = []
        edges_unique_sum_neg = []

        for eu in edges_unique_1:
            count_pos = edges_pos_1.count(eu)
            count_neg = edges_neg_1.count(eu)
            count = count_pos - count_neg

            if count > 0:
                edges_unique_sum_pos.append([eu[0], eu[1], count])

            if count <= 0:
                edges_unique_sum_neg.append([eu[0], eu[1], count])

        #print(len(edges_unique_sum_pos) + len(edges_unique_sum_neg))

        for eup in edges_unique_sum_pos:
            DG_2.add_edges_from([(eup[0], eup[1])], sign='+', sentiment=eup[2])

        for eun in edges_unique_sum_neg:
            DG_2.add_edges_from([(eun[0], eun[1])], sign='-', sentiment=eun[2])

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        nx.write_gexf(DG_2, path_to_store_scientist_mention_public_graph)

        # ------------ ALL mentions ----------- #

        print ()
        print("Creating GEPHI graph 3 (all mentions)...")

        t_start = time.time()

        edges_all = edges_pos + edges_neg

        edges_set = set(map(tuple, edges_all))  # result: {[1,2], [3,4]}
        edges_unique_tuple = list(edges_set)  # result: [(1,2), (3,4)]
        edges_unique = [list(eu) for eu in edges_unique_tuple]  # convert list of tuples to list of list

        # print(len(edges_unique))
        # print (edges_unique)

        edges_unique_sum_pos = []
        edges_unique_sum_neg = []

        for eu in edges_unique:
            count_pos = edges_pos.count(eu)
            count_neg = edges_neg.count(eu)
            count = count_pos - count_neg

            if count > 0:
                edges_unique_sum_pos.append([eu[0], eu[1], count])

            if count <= 0:
                edges_unique_sum_neg.append([eu[0], eu[1], count])

        #print(len(edges_unique_sum_pos) + len(edges_unique_sum_neg))

        for eup in edges_unique_sum_pos:
            DG_3.add_edges_from([(eup[0], eup[1])], sign='+', sentiment=eup[2])

        for eun in edges_unique_sum_neg:
            DG_3.add_edges_from([(eun[0], eun[1])], sign='-', sentiment=eun[2])


        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        nx.write_gexf(DG_3, path_to_store_combined_mention_graph)

        # ------------------------


        f = open(path_to_store_scientist_mention_public_edges, 'w')

        for ep in edges_pos_1:
            f.write(','.join(ep) + ',pos' + '\n')

        for en in edges_neg_1:
            f.write(','.join(en) + ',neg' + '\n')

        f.close()


        f = open(path_to_store_combined_mention_edges, 'w')

        for ep in edges_pos:
            f.write(','.join(ep) + ',pos' + '\n')

        for en in edges_neg:
            f.write(','.join(en) + ',neg' + '\n')

        f.close()

        #----------------
        # get in and out degrees

        print ()
        print ("Getting in and out degrees...")

        mentions_degree = [] # total in and out degrees for every node

        for id in list(DG3.in_degree_iter(nodes)):

            id = list(id)

            mentions_degree.append([id[0],'in',str(id[1])])

        for id in list(DG3.out_degree_iter(nodes)):

            id = list(id)

            mentions_degree.append([id[0],'out',str(id[1])])

        print ("Length of in and out degrees list: "+str(len(mentions_degree)))

        f = open(path_to_store_combined_mention_in_out_degrees,'w')

        for md in mentions_degree:
            f.write(','.join(md)+'\n')

        f.close()

        #----------------
        # get common neighbours (embeddedness)
        #
        # print ()
        # print ("Getting common neighbours (embeddedness)...")
        #
        # DG_3a = nx.Graph() # common neighbour function only works with undirected graphs
        #
        # DG_3a.add_edges_from(edges_pos, sign='+')
        # DG_3a.add_edges_from(edges_neg, sign='-')
        # DG_3a.add_nodes_from(nodes)
        #
        # print (sorted(nx.common_neighbors(DG_3a,'cosmocrops','nasa')))

#-----------------------------------------------------------
#
# CREATE FOLLOWING NETWORK
#
#-----------------------------------------------------------


    def create_following_list(self, n):

        scientists = self.get_scientist_and_public_list()[0]
        public = self.get_scientist_and_public_list()[1]

        print("Getting following list for list " + str(n) + " ...")

        lines = open(path_to_following_list_folder + str(n) + '.csv', 'r').readlines()

        followings = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            followings.append(spline)

        following_list = []

        for f in followings:

            user = []

            user.append(f[1].lower())

            if f[0] == '0':
                following_list.append(['0', f[1].lower()])

            if f[0] == '1':

                if f[1].lower() in scientists:
                    scientist_followed = list(set(user).intersection(scientists))
                    following_list.append(['1', scientist_followed[0]])

                if f[1].lower() in public:
                    public_followed = list(set(user).intersection(public))
                    following_list.append(['2', public_followed[0]])

        following_dict = {}

        flag = True  # the flag is needed to check if it is the first line of the file

        for index, fl in enumerate(following_list):

            if fl[0] == '0' and flag == True:  # first line of the file
                key = fl[1]
                foll_list = []
                flag = False
                continue

            if fl[0] == '0' and flag == False:
                following_dict[key] = foll_list
                key = fl[1]
                foll_list = []
                continue

            if fl[0] == '1' or fl[0] == '2':
                if index != len(following_list) - 1:
                    foll_list.append(fl)

                if index == len(following_list) - 1:  # check if it is the last line in the file
                    foll_list.append(fl)
                    following_dict[key] = foll_list

        # print (following_dict)

        # create list with users and the public and scientist users they follow

        foll_list_final = []

        for key, value in following_dict.items():

            key_list = []
            value_list = []

            key_list.append(key)

            if value != []:

                for v in value:
                    value_list.extend(v)

                foll_list = key_list + value_list
                foll_list_final.append(foll_list)

        # write to file

        f = open(path_to_store_following_list + str(n) + '.csv', 'w')

        for fl in foll_list_final:
            f.write(','.join(fl) + '\n')

        f.close()


    def start_get_foll_multiprocess(self):

        threads = 20

        jobs = []

        for n in range(1, threads + 1):
            getreplies = multiprocessing.Process(name='getfollowing_' + str(n), target=self.create_following_list, args=(n,))
            jobs.append(getreplies)

        for j in jobs:
            print(j)
            j.start()


    def create_network_following(self):

        DG4 = nx.MultiDiGraph() # for only following graph
        DG5 = nx.MultiDiGraph() # for combined mention and following graph
        DG_5 = nx.MultiDiGraph() # for Gephi: combined mention and following

        print ("Getting following dict ...")

        t_start = time.time()

        following_dict = {}

        for n in range(1, 21):
            lines = open('../output/network/following/following_list_' + str(n) + '.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                key = spline[0]
                value = []

                for n in range(1, len(spline) - 1, 2):
                    value.append([spline[n], spline[n + 1]])

                following_dict[key] = (value)

        print("Length of following dict: "+str(len(following_dict)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        ################
        # Get list of scientist and other public users a node (could be either scientist or public) follows
        # uncomment for NON-multithreading way
        ################

        # scientists = self.get_scientist_and_public_list()[0]
        # public = self.get_scientist_and_public_list()[1]
        #
        # followings = []
        #
        # for n in range(1,21):
        #
        #     lines = open(path_to_following_list_folder+str(n)+'.csv', 'r').readlines()
        #
        #     for line in lines:
        #         spline = line.rstrip('\n').split(',')
        #         followings.append(spline)
        #
        # print ("Length of following list is "+str(len(followings)))

        # ---------------
        # create following list in the format [[0,user1],[1,scientist1],[2,user2],[0,user2],[1,scientist1],[2,user1]]

        # print ()
        # print ('---------------------------')
        # print ("Creating following list for each user ...")
        #
        # t_start = time.time()
        #
        # following_list = []
        #
        # for f in followings:
        #
        #     user = []
        #
        #     user.append(f[1].lower())
        #
        #     if f[0] == '0':
        #         following_list.append(['0', f[1].lower()])
        #
        #     if f[0] == '1':
        #
        #         if f[1].lower() in scientists:
        #             scientist_followed = list(set(user).intersection(scientists))
        #             following_list.append(['1', scientist_followed[0]])
        #
        #         if f[1].lower() in public:
        #             public_followed = list(set(user).intersection(public))
        #             following_list.append(['2', public_followed[0]])
        #
        # #print (following_list)
        #
        # # --------------
        # # create a dictionary in the format: { user1:[[1,scientist1],[2,user2]], user2:[[1,scientist1],[2,user1]]...}
        #
        # print ("Creating following dict ...")
        #
        # following_dict = {}
        #
        # flag = True  # the flag is needed to check if it is the first line of the file
        #
        # for index, fl in enumerate(following_list):
        #
        #     if fl[0] == '0' and flag == True:  # first line of the file
        #         key = fl[1]
        #         foll_list = []
        #         flag = False
        #         continue
        #
        #     if fl[0] == '0' and flag == False:
        #         following_dict[key] = foll_list
        #         key = fl[1]
        #         foll_list = []
        #         continue
        #
        #     if fl[0] == '1' or fl[0] == '2':
        #         if index != len(following_list) - 1:
        #             foll_list.append(fl)
        #
        #         if index == len(following_list) - 1:  # check if it is the last line in the file
        #             foll_list.append(fl)
        #             following_dict[key] = foll_list

        # t_end = time.time()
        # total_time = round(((t_end - t_start) / 60), 2)
        # print("Computing time was " + str(total_time) + " minutes.")

        #print (following_dict)

        # create list with users and the public and scientist users they follow

        # foll_list_final = []
        #
        # for key, value in following_dict.items():
        #
        #     key_list = []
        #     value_list = []
        #
        #     key_list.append(key)
        #
        #     if value != []:
        #
        #         for v in value:
        #             value_list.extend(v)
        #
        #         foll_list = key_list + value_list
        #         foll_list_final.append(foll_list)
        #
        #
        # # write to file
        #
        # f = open(path_to_store_following_list,'w')
        #
        # for fl in foll_list_final:
        #     f.write(','.join(fl)+'\n')
        #
        # f.close()

        ###################
        # create graph for following_list_dict
        ###################

        lines = open(path_to_store_combined_mention_edges,'r').readlines()

        edges_pos = []
        edges_neg = []

        for line in lines:
            spline = line.rstrip('\n').split(',')

            if spline[2] == 'pos':
                edges_pos.append([spline[0],spline[1]])

            if spline[2] == 'neg':
                edges_neg.append([spline[0],spline[1]])


        print ()
        print("Length of positive edges (mentions): " + str(len(edges_pos)))
        print("Length of negative edges (mentions):  " + str(len(edges_neg)))

        nodes_temp = [] # get number of nodes from mention graph, to be used to check with final nodes count (should be the same!)

        for ep in edges_pos:

            if ep[0] not in nodes_temp:
                nodes_temp.append(ep[0])

            if ep[1] not in nodes_temp:
                nodes_temp.append(ep[1])

        for en in edges_neg:

            if en[0] not in nodes_temp:
                nodes_temp.append(en[0])

            if en[1] not in nodes_temp:
                nodes_temp.append(en[1])

        print("Length of nodes (from mention graph): " + str(len(nodes_temp)))

        scientists = self.get_scientist_and_public_list()[0]
        public = self.get_scientist_and_public_list()[1]

        edges_pos_2 = [] # to store only following edges

        for key,value in following_dict.items():

            if key in scientists:

                for v in value:

                    if v[0] == '2':
                        edges_pos.append([key,v[1]])
                        edges_pos_2.append([key,v[1]])

            if key in public:

                for v in value:

                    if v[0] == '1':
                        edges_pos.append([key,v[1]])
                        edges_pos_2.append([key,v[1]])

        print ()
        print("Length of positive edges (following): " + str(len(edges_pos_2)))

        print ()
        print("Length of positive edges (mentions+following): " + str(len(edges_pos)))
        print("Length of negative edges (mentions+following):  " + str(len(edges_neg)))
        print("Length of total edges (mentions+following):  " + str(len(edges_neg) + len(edges_pos)))

        # get nodes

        nodes = []

        for ep in edges_pos:

            if ep[0] not in nodes:
                nodes.append(ep[0])

            if ep[1] not in nodes:
                nodes.append(ep[1])

        for en in edges_neg:

            if en[0] not in nodes:
                nodes.append(en[0])

            if en[1] not in nodes:
                nodes.append(en[1])

        print ("Length of nodes (for mention+following graph): "+str(len(nodes)))
        #print (nodes)

        nodes_1 = [] # for only following graph

        for ep in edges_pos_2:

            if ep[0] not in nodes_1:
                nodes_1.append(ep[0])

            if ep[1] not in nodes_1:
                nodes_1.append(ep[1])

        DG4.add_edges_from(edges_pos_2, sign='+')
        DG4.add_nodes_from(nodes_1)

        nx.write_gexf(DG4, path_to_store_following_graph)

        DG5.add_edges_from(edges_pos, sign='+')
        DG5.add_edges_from(edges_neg, sign='-')
        DG5.add_nodes_from(nodes)

        # -------------------------

        # write to file

        f = open(path_to_store_following_edges, 'w')

        for ep in edges_pos_2:
            f.write(','.join(ep) + ',pos' + '\n')

        f.close()

        f = open(path_to_store_combined_mentions_and_following_edges, 'w')

        for ep in edges_pos:
            f.write(','.join(ep) + ',pos' + '\n')

        for en in edges_neg:
            f.write(','.join(en) + ',neg' + '\n')

        f.close()

        # ----------------------
        # CREATE GEPHI GRAPH:
        # sum up signs (if > 0 then positive, if < 0 then negative) if parallel edges exist (ONLY for Gephi, as it doesn't accept parallel edges)
        # if the sum is zero, default to negative

        print ()
        print ("Creating GEPHI graph (mentions+following) ...")

        t_start = time.time()

        edges_all = edges_pos + edges_neg

        edges_set = set(map(tuple, edges_all))  # result: {[1,2], [3,4]}
        edges_unique_tuple = list(edges_set)  # result: [(1,2), (3,4)]
        edges_unique = [list(eu) for eu in edges_unique_tuple]  # convert list of tuples to list of list


        print ()
        print ("Length of unique edges(before): "+str(len(edges_unique)))
        #print (edges_unique)

        edges_unique_sum_pos = []
        edges_unique_sum_neg = []

        for eu in edges_unique:
            count_pos = edges_pos.count(eu)
            count_neg = edges_neg.count(eu)
            count = count_pos - count_neg

            if count > 0:
                edges_unique_sum_pos.append([eu[0],eu[1],count])

            if count <= 0:
                edges_unique_sum_neg.append([eu[0],eu[1],count])

        print ("Length of unique edges(after): "+str(len(edges_unique_sum_pos)+len(edges_unique_sum_neg)))

        for eup in edges_unique_sum_pos:
            DG_5.add_edges_from([(eup[0],eup[1])], sign='+', sentiment=eup[2])

        for eun in edges_unique_sum_neg:
            DG_5.add_edges_from([(eun[0], eun[1])], sign='-', sentiment=eun[2])

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


        nx.write_gexf(DG_5, path_to_store_combined_mention_and_following_graph)

        # ----------------
        # get in and out degrees

        print()
        print("Getting in and out degrees...")

        mentions_degree = []  # total in and out degrees for every node

        for id in list(DG5.in_degree_iter(nodes)):
            id = list(id)

            mentions_degree.append([id[0], 'in', str(id[1])])

        for id in list(DG5.out_degree_iter(nodes)):
            id = list(id)

            mentions_degree.append([id[0], 'out', str(id[1])])

        print("Length of in and out degrees list: " + str(len(mentions_degree)))

        f = open(path_to_store_combined_mention_following_in_out_degrees, 'w')

        for md in mentions_degree:
            f.write(','.join(md) + '\n')

        f.close()

        # ---------------------
        # get common neighbours (embeddedness)
        #
        # print()
        # print("Getting common neighbours (embeddedness)...")
        #
        # DG_5a = nx.Graph()  # common neighbour function only works with undirected graphs
        #
        # DG_5a.add_edges_from(edges_pos, sign='+')
        # DG_5a.add_edges_from(edges_neg, sign='-')
        # DG_5a.add_nodes_from(nodes)
        #
        # print(sorted(nx.common_neighbors(DG_5a, 'cosmocrops', 'nasa')))


    def get_signed_in_out_degrees(self):

        # get filtered nodes

        lines = open(path_to_store_filtered_nodes,'r').readlines()

        nodes = []

        for line in lines:
            spline = line.rstrip('\n')
            nodes.append(spline)

        print ("Length of nodes is "+str(len(nodes)))

        #################
        # get signed in/out degrees for mentions graph
        #################

        lines = open(path_to_store_combined_mention_edges,'r').readlines()

        all_degrees = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            all_degrees.append(spline)

        print ()
        print ("Getting signed degree for mention graph ...")


        t_start = time.time()

        in_out_degree_signed = []

        for n in nodes:

            indegree_pos_count = 0
            indegree_neg_count = 0
            outdegree_pos_count = 0
            outdegree_neg_count = 0

            for ad in all_degrees:

                if ad[0] == n:

                    if ad[2] == 'pos':

                        outdegree_pos_count+=1

                    if ad[2] == 'neg':

                        outdegree_neg_count+=1

                if ad[1] == n:

                    if ad[2] == 'pos':

                        indegree_pos_count+=1

                    if ad[2] == 'neg':

                        indegree_neg_count+=1

            in_out_degree_signed.append([n,'in','pos',str(indegree_pos_count)])
            in_out_degree_signed.append([n,'in','neg',str(indegree_neg_count)])
            in_out_degree_signed.append([n, 'out', 'pos', str(outdegree_pos_count)])
            in_out_degree_signed.append([n, 'out', 'neg', str(outdegree_neg_count)])

        print ("Length of signed in/out degree list is: "+str(len(in_out_degree_signed))) #should be 4 times length of nodes!
        print ()

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        f = open(path_to_store_signed_combined_mention_in_out_degrees,'w')

        for iod in in_out_degree_signed:
            f.write(','.join(iod)+'\n')

        f.close()


        #################
        # get signed in/out degrees for mentions and following graph
        #################

        lines = open(path_to_store_combined_mentions_and_following_edges, 'r').readlines()

        all_degrees = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            all_degrees.append(spline)

        print ()
        print ('-------------------------')
        print ("Getting signed degree for mention and following graph ...")

        t_start = time.time()

        in_out_degree_signed = []

        for n in nodes:

            indegree_pos_count = 0
            indegree_neg_count = 0
            outdegree_pos_count = 0
            outdegree_neg_count = 0

            for ad in all_degrees:

                if ad[0] == n:

                    if ad[2] == 'pos':
                        outdegree_pos_count += 1

                    if ad[2] == 'neg':
                        outdegree_neg_count += 1

                if ad[1] == n:

                    if ad[2] == 'pos':
                        indegree_pos_count += 1

                    if ad[2] == 'neg':
                        indegree_neg_count += 1

            in_out_degree_signed.append([n, 'in', 'pos', str(indegree_pos_count)])
            in_out_degree_signed.append([n, 'in', 'neg', str(indegree_neg_count)])
            in_out_degree_signed.append([n, 'out', 'pos', str(outdegree_pos_count)])
            in_out_degree_signed.append([n, 'out', 'neg', str(outdegree_neg_count)])

        print("Length of signed in/out degree list is: " + str(len(in_out_degree_signed)))  # should be 4 times length of nodes!
        print()

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        f = open(path_to_store_signed_combined_mention_following_in_out_degrees, 'w')

        for iod in in_out_degree_signed:
            f.write(','.join(iod) + '\n')

        f.close()





##################
# variables
##################

#path_to_raw_unique_tweets_file = 'test.txt'
path_to_raw_unique_tweets_file = '/Users/yi-linghwong/Box Sync/unique_tweets/space/3_raw_tweets_18nov-18dec_1.csv'
path_to_raw_unique_tweets_file_1 = '/Users/yi-linghwong/Box Sync/unique_tweets/space/3_raw_tweets_18nov-18dec_2.csv'
path_to_seed_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_following_list_folder = '/Users/yi-linghwong/GitHub/_big_files/twitter/TrustStudy/3_18nov-18dec/following/space_following_'
path_to_profile_description_file = '../output/profile_description/profile_1_18sep-18oct.csv'

path_to_public_mention_scientist_tweets_with_sentiment = '../tweets/mentions/public_mention_scientist_extracted/public_@scientist_sentiment.csv'
path_to_scientist_mention_public_tweets_with_sentiment = '../tweets/mentions/scientist_mention_public/scientist_@public_sentiment.csv'

# storing

path_to_store_tweets_with_scientist_mention = '../tweets/mentions/public_mention_scientist_extracted/3_18nov-18dec/public_@scientist.csv' #tweets extracted from unique tweets corpus that contain mention of scientists
path_to_store_tweets_with_scientist_mention_filtered = '../tweets/mentions/public_mention_scientist_extracted/public_@scientist_filtered.csv'

path_to_store_nodes = '../output/network/nodes/3_18nov-18dec/nodes_extracted.csv'
path_to_store_nodes_without_following = '../output/network/nodes/3_18nov-18dec/nodes_without_following.csv'
path_to_store_nodes_with_following = '../output/network/nodes/3_18nov-18dec/nodes_with_following.csv'
path_to_store_filtered_nodes = '../output/network/nodes/nodes_filtered.csv'

path_to_store_seed_and_additional_space_user_list = '../user_lists/user_space_updated.csv'

path_to_store_following_list = '../output/network/following/following_list_' # users and the scientist and public users they follow

path_to_store_public_mention_scientist_graph = '../output/graph_files/public_@scientist_extracted.gexf'
path_to_store_scientist_mention_public_graph = '../output/graph_files/scientist_@public.gexf'
path_to_store_combined_mention_graph = '../output/graph_files/ALL_mentions.gexf'
path_to_store_following_graph = '../output/graph_files/following.gexf'
path_to_store_combined_mention_and_following_graph = '../output/graph_files/ALL_mentions_following.gexf'

path_to_store_public_mention_scientist_edges = '../output/network/edges/edges_public_@scientist.csv'
path_to_store_scientist_mention_public_edges = '../output/network/edges/edges_scientist_@public.csv'
path_to_store_combined_mention_edges = '../output/network/edges/edges_ALL_mentions.csv'
path_to_store_following_edges = '../output/network/edges/edges_following.csv'
path_to_store_combined_mentions_and_following_edges = '../output/network/edges/edges_ALL_mentions_following.csv'

path_to_store_combined_mention_in_out_degrees = '../output/network/degrees/mentions_degree.csv'
path_to_store_combined_mention_following_in_out_degrees = '../output/network/degrees/mentions_following_degree.csv'
path_to_store_signed_combined_mention_in_out_degrees = '../output/network/degrees/mentions_degree_signed.csv'
path_to_store_signed_combined_mention_following_in_out_degrees = '../output/network/degrees/mentions_following_degree_signed.csv'


if __name__ == '__main__':

    cn =  CreateTwitterNetwork()

    ##################
    # 1. extract tweets from public that contain scientist mention (in unique tweet list)
    ##################

    #cn.get_tweets_mentioning_scientists()

    ##################
    # 2. get all nodes (unique entries)
    ##################

    #cn.get_unique_nodes()

    ##################
    # 3. get user profile description
    ##################

    #run get_profile.py

    ##################
    # 4. get following for all nodes
    ##################

    # 1. (OPTIONAL) get only nodes that so far have not had their following list extracted, i.e. (uncomment next line)

    #cn.get_nodes_without_following()

    # 2. (OPTIONAL) extract the following list for the duplicated nodes, i.e. (uncomment next line)

    cn.get_following_list_for_duplicated_nodes()

    # 3. run get_following.py

    ##################
    # 5. filter out nodes whose accounts are protected, suspended or cancelled (return filtered scientists and public list)
    ##################

    #cn.get_filtered_nodes()

    ##################
    # 6. extract tweets from master tweet file for remaining nodes
    ##################

    #cn.extract_tweets_for_filtered_nodes()

    ##################
    # 7. get sentiment of filtered public @scientist tweets
    ##################

    # run get_sentiment.py

    ##################
    # 8. get replies to public from scientist timeline (for filtered nodes!)
    ##################

    # run get_replies_from_scientists.py

    ##################
    # 9. get sentiment for scientist @public tweets
    ##################

    # run get_sentiment.py

    ##################
    # 10. create network for mentions (and in/out degrees)
    ##################

    #cn.create_network_mentions()

    ##################
    # 11. start multiprocessing to get following dict
    ##################

    #cn.start_get_foll_multiprocess()

    ##################
    # 12. create network for following (and in/out degrees)
    ##################

    #cn.create_network_following()

    ##################
    # 13. get signed in/out degrees
    ##################

    #cn.get_signed_in_out_degrees()