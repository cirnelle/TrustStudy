__author__ = 'yi-linghwong'

import os
import sys
import networkx as nx
import time

class GetEmbeddedness():


    def get_scientist_and_public_list(self):

        ###############
        # get the list of remaining scientist and public from the node list (after getting the following for all nodes)
        # to filter out nodes whose accounts are protected/suspended/cancelled
        ###############

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_additional_space_user_list,'r').readlines()
        lines3 = open(path_to_filtered_nodes, 'r').readlines()

        scientist_seed = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')

            scientist_seed.append(spline[0].lower())

        scientist_additional = []

        for line in lines2:
            spline = line.rstrip('\n')

            scientist_additional.append(spline.lower())

        scientist_all = scientist_seed + scientist_additional

        scientists = []
        public = []

        for line in lines3:
            spline = line.rstrip('\n')

            if spline.lower() in scientist_all:
                scientists.append(spline.lower())

            else:
                public.append(spline.lower())

        print (scientists)
        print (public)

        return scientists, public


    def get_embeddedness(self):

        DG1 = nx.MultiDiGraph()  # for only following graph
        DG2 = nx.Graph() # for mention and following graph (undirected)
        DG_2 = nx.MultiDiGraph()  # FOR GEPHI: for mention and following graph

        ################
        # Get list of scientist and other public users a node (could be either scientist or public) follows
        ################

        print("Getting following dict ...")

        t_start = time.time()

        following_dict = {}

        for n in range(1, 21):
            lines = open(path_to_following_list_folder + str(n) + '.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                key = spline[0]
                value = []

                for n in range(1, len(spline) - 1, 2):
                    value.append([spline[n], spline[n + 1]])

                following_dict[key] = (value)

        print("Length of following dict: " + str(len(following_dict)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


        ###################
        # create graph for following_list_dict
        ###################

        t_start = time.time()

        lines = open(path_to_combined_mention_edges, 'r').readlines()

        edges_pos = []
        edges_neg = []

        for line in lines:
            spline = line.rstrip('\n').split(',')

            if spline[2] == 'pos':
                edges_pos.append([spline[0], spline[1]])

            if spline[2] == 'neg':
                edges_neg.append([spline[0], spline[1]])

        print()
        print("Length of positive edges (mentions): " + str(len(edges_pos)))
        print("Length of negative edges (mentions):  " + str(len(edges_neg)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        print ()
        print ("Getting nodes (mention)...")

        t_start = time.time()

        nodes_temp = []  # get number of nodes from mention graph, to be used to check with final nodes count (should be the same!)

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

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


        print ()
        print ("Getting edges (mentions+following, incl.intra-group)...")

        edges_pos_2 = []  # to store only following edges

        for key, value in following_dict.items():

            for v in value:

                edges_pos.append([key, v[1]])
                edges_pos_2.append([key, v[1]])

        #print (edges_pos_2)

        print()
        print("Length of positive edges (following, incl. intra-group): " + str(len(edges_pos_2)))

        print()
        print("Length of positive edges (mentions+following): " + str(len(edges_pos)))
        print("Length of negative edges (mentions+following):  " + str(len(edges_neg)))
        print("Length of total edges (mentions+following):  " + str(len(edges_neg) + len(edges_pos)))

        # get nodes

        print ()
        print ("Getting nodes (mention+following)...")

        t_start = time.time()

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

        print("Length of nodes (for mention+following graph): " + str(len(nodes)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        print ()
        print ("Getting nodes (following, incl. intra-group)...")

        t_start = time.time()

        nodes_1 = []  # for only following graph

        for ep in edges_pos_2:

            if ep[0] not in nodes_1:
                nodes_1.append(ep[0])

            if ep[1] not in nodes_1:
                nodes_1.append(ep[1])

        print ("Length of nodes (following, incl. intra-group): ",len(nodes_1))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        print ()
        print ("Creating GEPHI graph (following, incl. intra-group)...")

        t_start = time.time()

        DG1.add_edges_from(edges_pos_2, sign='+')
        DG1.add_nodes_from(nodes_1)

        nx.write_gexf(DG1, path_to_store_following_graph) #includes intra-public and intra-scientist group following!

        DG2.add_edges_from(edges_pos, sign='+')
        DG2.add_edges_from(edges_neg, sign='-')
        DG2.add_nodes_from(nodes)

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")


        # ----------------------
        # CREATE GEPHI GRAPH:
        # sum up signs (if > 0 then positive, if < 0 then negative) if parallel edges exist (ONLY for Gephi, as it doesn't accept parallel edges)
        # if the sum is zero, default to negative

        # print ()
        # print ("Creating GEPHI graph (mention+following, incl. intra-group)...")
        #
        # t_start = time.time()
        #
        # edges_all = edges_pos + edges_neg
        #
        # edges_set = set(map(tuple, edges_all))  # result: {[1,2], [3,4]}
        # edges_unique_tuple = list(edges_set)  # result: [(1,2), (3,4)]
        # edges_unique = [list(eu) for eu in edges_unique_tuple]  # convert list of tuples to list of list
        #
        # print()
        # print("Length of unique edges(before): " + str(len(edges_unique)))
        # # print (edges_unique)
        #
        # edges_unique_sum_pos = []
        # edges_unique_sum_neg = []
        # edges_unique_dict = {}
        #
        # for eu in edges_unique:
        #     count_pos = edges_pos.count(eu)
        #     count_neg = edges_neg.count(eu)
        #     count = count_pos - count_neg
        #
        #     if count > 0:
        #         edges_unique_sum_pos.append([eu[0], eu[1], count])
        #         edges_unique_dict[eu[0], eu[1]] = 'pos'
        #
        #     if count <= 0:
        #         edges_unique_sum_neg.append([eu[0], eu[1], count])
        #         edges_unique_dict[eu[0], eu[1]] = 'neg'
        #
        # print("Length of unique edges(after): " + str(len(edges_unique_sum_pos) + len(edges_unique_sum_neg)))
        #
        # for eup in edges_unique_sum_pos:
        #     DG_2.add_edges_from([(eup[0], eup[1])], sign='+', sentiment=eup[2])
        #
        # for eun in edges_unique_sum_neg:
        #     DG_2.add_edges_from([(eun[0], eun[1])], sign='-', sentiment=eun[2])
        #
        # nx.write_gexf(DG_2, path_to_store_combined_mention_and_following_graph)
        #
        # t_end = time.time()
        # total_time = round(((t_end - t_start) / 60), 2)
        # print("Computing time was " + str(total_time) + " minutes.")
        #
        # # write to file (so that don't have to recreate this when creating triad as it takes a freaking long time)
        #
        # edges_unique_list = []
        #
        # for key,value in edges_unique_dict.items():
        #     key = list(key)
        #     key.append(value)
        #     edges_unique_list.append(key)
        #
        # print ()
        # print ("Writing unique edges, following edges and mentions+following edges to file...")
        #
        # f = open(path_to_store_unique_edges_file, 'w')
        #
        # for eu in edges_unique_list:
        #     f.write(','.join(eu)+'\n')
        #
        # f.close()

        # -------------------------

        # write to file

        # f = open(path_to_store_following_edges, 'w')
        #
        # for ep in edges_pos_2:
        #     f.write(','.join(ep) + ',pos' + '\n')
        #
        # f.close()
        #
        # f = open(path_to_store_combined_mentions_and_following_edges, 'w')
        #
        # for ep in edges_pos:
        #     f.write(','.join(ep) + ',pos' + '\n')
        #
        # for en in edges_neg:
        #     f.write(','.join(en) + ',neg' + '\n')
        #
        # f.close()

        #------------------------
        # get common neighbours (embeddedness)

        print()
        print ('------------------------')
        print ("Getting common neighbours (embeddedness) ...")

        t_start = time.time()

        lines = open(path_to_trust_links_file,'r').readlines()

        embeddedness = []
        embedded_node_list = []


        for line in lines:
            spline = line.rstrip('\n').split(',')

            embedded_list = []

            common_neighbours = sorted(nx.common_neighbors(DG2, spline[0],spline[1]))

            embeddedness.append([spline[0],spline[1],str(len(common_neighbours))])
            embedded_list.append(spline[0])
            embedded_list.append(spline[1])

            for n in range(len(common_neighbours)):
                embedded_list.insert(n+2,common_neighbours[n])

            embedded_node_list.append(embedded_list)

        #print (embeddedness)
        #print (embedded_node_list)
        print (len(embedded_node_list))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        f = open(path_to_store_embeddedness,'w')

        for e in embeddedness:
            f.write(','.join(e)+'\n')

        f.close()

        f = open(path_to_store_embeddeded_node_list, 'w')

        for e in embedded_node_list:
            f.write(','.join(e) + '\n')

        f.close()



#################
# variables
#################

path_to_seed_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_additional_space_user_list = '../user_lists/1_18sep-18oct/user_space_additional.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'
path_to_following_list_folder = '../output/network/following/1_18sep-18oct/following_list_'
path_to_combined_mention_edges = '../output/network/edges/1_18sep-18oct/edges_ALL_mentions.csv'
path_to_trust_links_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_filtered.csv'

path_to_store_following_graph = '../output/graph_files/1_18sep-18oct/following_intra_group.gexf' #includes intra-public and intra-scientist group following!
path_to_store_combined_mention_and_following_graph = '../output/graph_files/1_18sep-18oct/ALL_mentions_following_intra_group.gexf'

path_to_store_unique_edges_file = '../output/network/edges/1_18sep-18oct/edges_unique.csv' # unique edges (when parallel edges exist we sum up their value so that one edge is left)
path_to_store_following_edges = '../output/network/edges/1_18sep-18oct/edges_following_intra_group.csv' #includes intra-public and intra-scientist group following!
path_to_store_combined_mentions_and_following_edges = '../output/network/edges/1_18sep-18oct/edges_ALL_mentions_following_intra_group.csv'

path_to_store_embeddedness = '../output/network/embeddedness/by_manual_labelling/1_18sep-18oct/embeddedness_count.csv'
path_to_store_embeddeded_node_list = '../output/network/embeddedness/by_manual_labelling/1_18sep-18oct/embeddedness_node_list.csv'



if __name__ == '__main__':

    ge = GetEmbeddedness()

    #ge.get_scientist_and_public_list()

    ge.get_embeddedness()