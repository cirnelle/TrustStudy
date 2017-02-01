__author__ = 'yi-linghwong'

import os
import sys
import networkx as nx
import time

class GetTriad():


    def get_scientist_and_public_list(self):
        ###############
        # get the list of remaining scientist and public from the node list (after getting the following for all nodes)
        # to filter out nodes whose accounts are protected/suspended/cancelled
        ###############

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

        return scientists, public


    def get_triad(self):

        lines1 = open(path_to_trust_links_file,'r').readlines()
        lines2 = open(path_to_combined_mentions_and_following_edges,'r').readlines() #includes intra-group followings

        #----------------------
        # create undirected graph of mention and following list (incl. intra group following)
        # to get list of embedded node list

        t_start = time.time()

        DG = nx.Graph()

        edges_pos = []
        edges_neg = []
        edges_all = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            edges_all.append(spline)

            if spline[2] == 'pos':
                edges_pos.append([spline[0],spline[1]])

            if spline[2] == 'neg':
                edges_neg.append([spline[0],spline[1]])

        print ("Getting unique nodes...")

        nodes_with_dup = []

        for ep in edges_pos:
            nodes_with_dup.append(ep[0])
            nodes_with_dup.append(ep[1])

        for en in edges_neg:
            nodes_with_dup.append(en[0])
            nodes_with_dup.append(en[1])

        nodes_set = set(nodes_with_dup)
        nodes = list(nodes_set)

        print ("Length of nodes is: "+str(len(nodes)))

        DG.add_edges_from(edges_pos, sign='+')
        DG.add_edges_from(edges_neg, sign='-')
        DG.add_nodes_from(nodes)


        #--------------------
        # sum up parallel edges
        # need this for getting triad: when parallel edges exist, we sum up their value so that only one edge is left

        print()
        print ("Getting unique edges ...")

        edges_all = edges_pos + edges_neg

        print ("Length of edges (incl. duplicate): "+str(len(edges_all)))

        edges_set = set(map(tuple,edges_all)) #result: {[1,2], [3,4]}
        edges_unique_tuple = list(edges_set) #result: [(1,2), (3,4)]
        edges_unique = [list(eu) for eu in edges_unique_tuple] #convert list of tuples to list of list

        print("Length of unique edges(before): " + str(len(edges_unique)))
        # print (edges_unique)

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        #--------------------------
        # UNCOMMENT THE FOLLOWING THE FIRST TIME WE WANT TO GET TRIAD FILE, IE WHEN UNIQUE EDGES FILE DOES NOT EXIST YET!

        # print ()
        # print ("Getting sum for unique edges...")
        #
        # t_start = time.time()
        #
        # edges_unique_sum = []
        # edges_unique_dict = {}
        #
        # for eu in edges_unique:
        #     count_pos = edges_pos.count(eu)
        #     count_neg = edges_neg.count(eu)
        #     count = count_pos - count_neg
        #
        #     if count > 0:
        #         edges_unique_sum.append([eu[0], eu[1], 'pos'])
        #         edges_unique_dict[eu[0], eu[1]] = 'pos'
        #
        #     if count <= 0:
        #         edges_unique_sum.append([eu[0], eu[1], 'neg'])
        #         edges_unique_dict[eu[0], eu[1]] = 'neg'
        #
        # print("Length of unique edges(after): " + str(len(edges_unique_sum)))
        # #print (edges_unique_dict)
        #
        # # write to file
        #
        # edges_unique_list = []
        #
        # for key,value in edges_unique_dict.items():
        #     key = list(key)
        #     key.append(value)
        #     edges_unique_list.append(key)
        #
        # f = open(path_to_store_unique_edges_file, 'w')
        #
        # for eu in edges_unique_list:
        #     f.write(','.join(eu)+'\n')
        #
        # f.close()
        #
        #
        # t_end = time.time()
        # total_time = round(((t_end - t_start) / 60), 2)
        # print("Computing time was " + str(total_time) + " minutes.")

        #---------------------


        lines = open (path_to_store_unique_edges_file,'r').readlines()

        edges_unique_dict = {}

        for line in lines:
            spline = line.rstrip('\n').split(',')

            key = (spline[0],spline[1])

            if key not in edges_unique_dict:

                edges_unique_dict[key] = spline[2]

            else:
                print (spline)



        print ()
        print ("Getting trust links...")

        t_start = time.time()

        trust_links = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

        print ("Length of trust links list is: "+str(len(trust_links)))

        triad_dict = {}

        for tl in trust_links:

            #print (tl)

            a_1 = a_2 = a_3 = a_4 = a_5 = a_6 = a_7 = a_8 = a_9 = a_10 = a_11 = a_12 = a_13 = a_14 = a_15 = a_16 = 0

            common_neighbours = sorted(nx.common_neighbors(DG, tl[0], tl[1]))

            if common_neighbours == []:

                triad_vector = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            else:

                for cn in common_neighbours:

                    u = tl[0]
                    v = tl[1]
                    x = cn

                    if (u, x) in edges_unique_dict:

                        if edges_unique_dict[(u, x)] == 'pos':

                            if (x, v) in edges_unique_dict:

                                if edges_unique_dict[(x, v)] == 'pos':

                                    a_1 += 1

                                if edges_unique_dict[(x, v)] == 'neg':

                                    a_2 += 1

                            if (v, x) in edges_unique_dict:

                                if edges_unique_dict[(v, x)] == 'pos':

                                    a_3 += 1

                                if edges_unique_dict[(v, x)] == 'neg':

                                    a_4 += 1

                        elif edges_unique_dict[(u, x)] == 'neg':

                            if (x, v) in edges_unique_dict:

                                if edges_unique_dict[(x, v)] == 'pos':

                                    a_5 += 1

                                if edges_unique_dict[(x, v)] == 'neg':

                                    a_6 += 1

                            if (v, x) in edges_unique_dict:

                                if edges_unique_dict[(v, x)] == 'pos':

                                    a_7 += 1

                                if edges_unique_dict[(v, x)] == 'neg':

                                    a_8 += 1

                    if (x, u) in edges_unique_dict:

                        if edges_unique_dict[(x, u)] == 'pos':

                            if (x, v) in edges_unique_dict:

                                if edges_unique_dict[(x, v)] == 'pos':

                                    a_9 += 1

                                if edges_unique_dict[(x, v)] == 'neg':

                                    a_10 += 1

                            if (v, x) in edges_unique_dict:

                                if edges_unique_dict[(v, x)] == 'pos':

                                    a_11 += 1

                                if edges_unique_dict[(v, x)] == 'neg':

                                    a_12 += 1

                        elif edges_unique_dict[(x, u)] == 'neg':

                            if (x, v) in edges_unique_dict:

                                if edges_unique_dict[(x, v)] == 'pos':

                                    a_13 += 1

                                if edges_unique_dict[(x, v)] == 'neg':

                                    a_14 += 1

                            if (v, x) in edges_unique_dict:

                                if edges_unique_dict[(v, x)] == 'pos':

                                    a_15 += 1

                                if edges_unique_dict[(v, x)] == 'neg':

                                    a_16 += 1

                triad_vector = [a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8,a_8,a_10,a_11,a_12,a_13,a_14,a_15,a_16]

            #print (triad_vector)

            triad_dict[tl[0],tl[1]] = triad_vector

        print("Length of triad dict is: "+str(len(triad_dict)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


        # write to file

        f = open(path_to_store_triad_file,'w')

        for key,value in triad_dict.items():

            key = list(key)

            value_string = []

            for v in value:
                value_string.append(str(v))

            triad_list = key + value_string

            f.write(','.join(triad_list)+'\n')

        f.close()


################
# variables
################

path_to_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'
path_to_trust_links_file = '../output/trust_links/by_trust_dictionary/strict/trust_links_space.csv'
path_to_combined_mentions_and_following_edges = '../output/network/edges/edges_ALL_mentions_following_intra_group.csv'

path_to_store_unique_edges_file = '../output/network/edges/edges_unique.csv'
path_to_store_triad_file = '../output/network/triad/by_trust_dictionary/strict/triad_space_strict.csv'


if __name__ == '__main__':

    gt = GetTriad()

    #gt.get_scientist_and_public_list()

    gt.get_triad()

