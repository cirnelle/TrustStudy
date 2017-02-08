__author__ = 'yi-linghwong'

import os
import sys
import time
import re

class GetLiwcFeatures():

    def combine_timeline_tweets(self):

        lines = open(path_to_trust_links_public_nodes,'r').readlines()

        public_nodes = []

        for line in lines:
            spline = line.rstrip('\n')
            public_nodes.append(spline)


        timeline_nodes_all = []
        nodes_and_tweets = []

        print ()
        print ("Compiling nodes and their timeline tweets...")

        t_start = time.time()

        for n in range(21,41):

            print (n)

            timeline_nodes = []

            lines1 = open(path_to_timeline_tweets_files+str(n)+'.csv','r').readlines()

            for line in lines1:
                spline = line.rstrip('\n').split(',')

                if spline[0] in public_nodes:

                    if spline[0] not in timeline_nodes:
                        timeline_nodes.append(spline[0])

                    if spline[0] not in timeline_nodes_all:
                        timeline_nodes_all.append(spline[0])

                else:
                    print ("error")
                    print (spline)


            for tn in timeline_nodes:

                node = tn
                tweets = []

                if len(tweets) < 50: #take only latest n tweets

                    for line in lines1:

                        spline = line.rstrip('\n').split(',')

                        if spline[0] == tn:

                            spline[-1] = spline[-1].replace(',',' ')
                            url_removed = re.sub(r'(?:https?\://)\S+', '', spline[-1])
                            tweets.append(url_removed)

                t1 = ' '.join(tweets)

                nodes_and_tweets.append([node,t1])

        print ()
        print("Length of original public node list: ", len(public_nodes))
        print ("Length of timeline nodes: ",len(timeline_nodes_all))

        print ("Length of nodes and tweets list: ",len(nodes_and_tweets))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")

        f = open(path_to_store_node_and_tweet_ALL,'w')

        for nt in nodes_and_tweets:
            f.write(','.join(nt)+'\n')

        f.close()


    def update_trust_links(self):

        lines1 = open(path_to_trust_links_file,'r').readlines()
        lines2 = open(path_to_store_node_and_tweet_ALL,'r').readlines()

        nodes_ori = []
        trust_links_ori = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links_ori.append(spline)

            if spline[0] not in nodes_ori:
                nodes_ori.append(spline[0])


        print ("Length of original nodes: ",len(nodes_ori))

        nodes_filtered = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            if spline[0] not in nodes_filtered:
                nodes_filtered.append(spline[0])

        print ("Length of filtered nodes: ",len(nodes_filtered))

        trust_links_filtered = []

        for tl in trust_links_ori:

            if tl[0] in nodes_filtered:
                trust_links_filtered.append(tl)

        print ()
        print("Length of original trust links: ", len(trust_links_ori))
        print ("Length of filtered trust links: ",len(trust_links_filtered))

        f = open(path_to_store_filtered_trust_links_file,'w')

        for tl in trust_links_filtered:
            f.write(','.join(tl)+'\n')

        f.close()


    def get_liwc_features(self):

        lines1 = open(path_to_liwc_result_file,'r').readlines()
        lines2 = open(path_to_store_filtered_trust_links_file,'r').readlines()

        liwc_scores_dict = {}

        for line in lines1[1:]:
            spline = line.rstrip('\n').split('\t')

            liwc_scores_dict[spline[0]] = spline[2:]

        print ("Length of liwc scores dict: ",len(liwc_scores_dict))

        print ("Length of filtered trust links: ",len(lines2))

        liwc_features = []
        trust_links = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            trust_links.append(spline)

            if spline[0] in liwc_scores_dict:
                liwc_features.append(liwc_scores_dict[spline[0]])

            else:
                print ("Node not in liwc dict, exiting")
                print (spline)
                sys.exit()

        print ("Length of liwc features: ",len(liwc_features))
        #print (trust_links[:5])

        # -----------------------------
        # labelled LIWC feature #

        targets = []

        for tl in trust_links:
            targets.append(tl[2])

        if len(targets) == len(liwc_features):
            zipped = zip(liwc_features, targets)

        else:
            print("Length of target and LIWC feature lists not equal, exiting...")
            sys.exit()

        liwc_features_and_target = []

        for z in zipped:
            target_temp = []
            target_temp.append(z[1])

            z = list(z)
            z = z[0] + target_temp

            liwc_features_and_target.append(z)

        print()
        print("Length of LIWC features and target list: " + str(len(liwc_features_and_target)))

        f = open(path_to_store_labelled_liwc_features_and_target_file, 'w')

        for ft in liwc_features_and_target:
            f.write(','.join(ft) + '\n')

        f.close()





###################
# variables
###################

path_to_trust_links_public_nodes = '../output/network/nodes/1_18sep-18oct/nodes_trust_links_public.csv'
path_to_timeline_tweets_files = '../output/timeline_tweets/1_18sep-18oct/timeline/timeline_tweets_'
path_to_liwc_result_file = '../output/liwc/liwc_public_timeline_tweets.txt'
path_to_trust_links_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_new.csv'

path_to_store_node_and_tweet_ALL = '../output/timeline_tweets/1_18sep-18oct/timeline_tweets_ALL.csv' #input file for LIWC!
path_to_store_filtered_trust_links_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_filtered.csv'
path_to_store_labelled_liwc_features_and_target_file = '../output/features/by_manual_labelling/liwc/labelled_liwc.csv'


if __name__ == '__main__':

    gl = GetLiwcFeatures()

    #gl.combine_timeline_tweets()

    #gl.update_trust_links()

    gl.get_liwc_features()

