__author__ = 'yi-linghwong'

import os
import sys
from collections import defaultdict
import time


class FeatureConstruction():


    def create_degree_features(self):

        lines1 = open(path_to_trust_links_file,'r').readlines()
        lines2 = open(path_to_degree_file,'r').readlines()
        lines3 = open(path_to_degree_signed_file,'r').readlines()
        lines4 = open(path_to_embeddedness_file,'r').readlines()

        print ("Getting trust link list ...")

        trust_links = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

        print ("Length of trust links: "+str(len(trust_links)))

        print ("Getting degrees dict ...")

        degrees_dict = {}

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            if spline[0] in degrees_dict:
                degrees_dict[spline[0]].append([spline[1],spline[2]])

            else:
                degrees_dict[spline[0]] = [[spline[1], spline[2]]]

        print ("Length of degrees dict: "+str(len(degrees_dict)))

        print("Getting signed degrees dict ...")

        degrees_signed_dict = {}

        for line in lines3:
            spline = line.rstrip('\n').split(',')

            if spline[0] in degrees_signed_dict:
                degrees_signed_dict[spline[0]].append([spline[1],spline[2],spline[3]])

            else:
                degrees_signed_dict[spline[0]] = [[spline[1], spline[2], spline[3]]]

        print ("Length of signed degrees dict: "+str(len(degrees_signed_dict)))

        print("Getting embeddedness dict ...")

        embeddedness_dict = {}

        for line in lines4:
            spline = line.rstrip('\n').split(',')

            if (spline[0],spline[1]) not in embeddedness_dict:

                embeddedness_dict[spline[0],spline[1]] = spline[2]

        print ("Length of embeddedness dict: "+str(len(embeddedness_dict)))

        degree_features_list = []
        degree_features_list_nonames = []


        for tl in trust_links:

            #print (tl)

            degree_features = [str(0)]*7

            u = tl[0]
            v = tl[1]

            for du in degrees_signed_dict[u]:

                if du[0] == 'out' and du[1] == 'pos':
                    degree_features[0] = du[2]

                if du[0] == 'out' and du[1] == 'neg':
                    degree_features[1] = du[2]

            for dv in degrees_signed_dict[v]:

                if dv[0] == 'in' and dv[1] == 'pos':
                    degree_features[2] = dv[2]

                if dv[0] == 'in' and dv[1] == 'neg':
                    degree_features[3] = dv[2]

            for du in degrees_dict[u]:

                if du[0] == 'out':
                    degree_features[4] = du[1]

            for dv in degrees_dict[v]:

                if dv[0] == 'in':
                    degree_features[5] = dv[1]

            if (u,v) in embeddedness_dict:

                degree_features[6] = embeddedness_dict[(u,v)]

            elif (v,u) in embeddedness_dict:

                degree_features[6] = embeddedness_dict[(v,u)]

            #print (degree_features)

            degree_features.insert(0,tl[0])
            degree_features.insert(1,tl[1])
            degree_features_list.append(degree_features)
            degree_features_list_nonames.append(degree_features[2:])


        #print ("Length of degree feature list: "+str(len(degree_features_list_nonames)))
        #print (degree_features_list[:3])
        #print (degree_features_list_nonames[:3])

        if len(degree_features_list_nonames) != len(trust_links):
            print ()
            print ('!!!!')
            print ("LENGTHS NOT EQUAL, WARNING, PLEASE CHECK!")
            print('!!!!')
            print ()

        f = open(path_to_store_degree_features,'w')

        for df in degree_features_list:

            f.write(','.join(df)+'\n')

        f.close()

        return degree_features_list_nonames


    def create_triad_features(self):

        lines1 = open(path_to_trust_links_file,'r').readlines()
        lines2 = open(path_to_triad_file,'r').readlines()

        print ()
        print("Getting trust link list ...")

        trust_links = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

        print("Length of trust links: " + str(len(trust_links)))


        print ("Getting triads ...")

        triad_dict = {}

        for line in lines2:
            spline = line.rstrip('\n').split(',')

            triad_dict[spline[0],spline[1]] = spline[2:]

        print ("Length of triads: "+str(len(triad_dict)))
        #print (triad_dict)

        triad_features_list = []
        triad_features_list_nonames = []

        for tl in trust_links:

            key = (tl[0],tl[1])

            if key in triad_dict:

                triad_features = triad_dict[key]
                triad_features.insert(0,tl[0])
                triad_features.insert(1,tl[1])

                triad_features_list.append(triad_features)
                triad_features_list_nonames.append(triad_features[2:])

            else:
                print ('error')
                print (tl)

        #print ("Length of triad feature list: "+str(len(triad_features_list_nonames)))
        #print (triad_features_list[:3])
        #print (triad_features_list_nonames[:3])

        if len(triad_features_list_nonames) != len(trust_links):
            print ()
            print ('!!!!')
            print ("LENGTHS NOT EQUAL, WARNING, PLEASE CHECK!")
            print('!!!!')
            print ()

        # write to file

        f = open(path_to_store_triad_features,'w')

        for tf in triad_features_list:
            f.write(','.join(tf)+'\n')

        f.close()

        return triad_features_list_nonames


    def create_complete_features(self):

        degree_features = self.create_degree_features()
        triad_features = self.create_triad_features()

        print ()
        print ('-------------------------')
        print ("Length of degree_features: "+str(len(degree_features)))
        print ("Length of triad features: "+str(len(triad_features)))

        zipped = zip(degree_features,triad_features)

        all_features = []

        for z in zipped:
            z = list(z)
            z = z[0] + z[1]

            if len(z) == 23:
                all_features.append(z)

            else:
                print ("error")
                print (z)

        print ("Length of all features list: "+str(len(all_features)))

        lines = open(path_to_trust_links_file, 'r').readlines()

        trust_links = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

        targets = []

        for tl in trust_links:
            targets.append(tl[2])

        if len(targets) == len(all_features):

            zipped = zip(all_features,targets)

        else:
            print("Length of target and feature lists not equal, exiting...")
            sys.exit()

        features_and_target = []

        for z in zipped:

            target_temp = []
            target_temp.append(z[1])

            z = list(z)
            z = z[0] + target_temp

            features_and_target.append(z)

        print ("Length of features and target list: "+str(len(features_and_target)))

        f = open(path_to_store_features_and_target_file,'w')

        for ft in features_and_target:
            f.write(','.join(ft)+'\n')

        f.close()





#################
# variables
#################

path_to_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'
path_to_trust_links_file = '../output/trust_links/by_trust_dictionary/strict/trust_links_space.csv'

path_to_degree_file = '../output/network/degrees/mentions_following_degree.csv'
path_to_degree_signed_file = '../output/network/degrees/mentions_following_degree_signed.csv'
path_to_embeddedness_file = '../output/network/embeddedness/by_trust_dictionary/strict/embeddedness_count.csv'
path_to_triad_file = '../output/network/triad/by_trust_dictionary/strict/triad_space.csv'

path_to_store_degree_features = '../output/features/by_trust_dictionary/strict/degree_features.csv'
path_to_store_triad_features = '../output/features/by_trust_dictionary/strict/triad_features.csv'
path_to_store_features_and_target_file = '../output/features/by_trust_dictionary/strict/labelled_degree_and_triad.csv'



if __name__ == '__main__':

    fc = FeatureConstruction()

    #fc.create_degree_features()

    #fc.create_triad_features()

    fc.create_complete_features()