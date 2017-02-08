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

        #print (triad_features)

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

        ##################################
        # zip target and feature files together to create labelled features
        ##################################

        trust_links = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

        #-----------------------------
        # labelled degree and triad #

        targets = []

        for tl in trust_links:
            targets.append(tl[2])

        if len(targets) == len(all_features):

            zipped = zip(all_features,targets)

        else:
            print("Length of target and ALL feature lists not equal, exiting...")
            sys.exit()

        all_features_and_target = []

        for z in zipped:

            target_temp = []
            target_temp.append(z[1])

            z = list(z)
            z = z[0] + target_temp

            all_features_and_target.append(z)

        print ()
        print ("Length of ALL features and target list: "+str(len(all_features_and_target)))

        f = open(path_to_store_labelled_ALL_features_and_target_file,'w')

        for ft in all_features_and_target:
            f.write(','.join(ft)+'\n')

        f.close()

        # -----------------------------
        # labelled degree ONLY #

        targets = []

        for tl in trust_links:
            targets.append(tl[2])

        if len(targets) == len(degree_features):

            zipped = zip(degree_features, targets)

        else:
            print("Length of target and DEGREE feature lists not equal, exiting...")
            sys.exit()

        degree_features_and_target = []

        for z in zipped:
            target_temp = []
            target_temp.append(z[1])

            z = list(z)
            z = z[0] + target_temp

            degree_features_and_target.append(z)

        print ()
        print("Length of DEGREE features and target list: " + str(len(degree_features_and_target)))

        f = open(path_to_store_labelled_degree_features_and_target_file, 'w')

        for ft in degree_features_and_target:
            f.write(','.join(ft) + '\n')

        f.close()

        # -----------------------------
        # labelled triad ONLY #

        targets = []

        for tl in trust_links:
            targets.append(tl[2])

        if len(targets) == len(triad_features):

            zipped = zip(triad_features, targets)

        else:
            print("Length of target and TRIAD feature lists not equal, exiting...")
            sys.exit()

        triad_features_and_target = []

        for z in zipped:
            target_temp = []
            target_temp.append(z[1])

            z = list(z)
            z = z[0] + target_temp

            triad_features_and_target.append(z)

        print()
        print("Length of TRIAD features and target list: " + str(len(triad_features_and_target)))

        f = open(path_to_store_labelled_triad_features_and_target_file, 'w')

        for ft in triad_features_and_target:
            f.write(','.join(ft) + '\n')

        f.close()

    def filter_features(self):

        ######################
        # filter out std/norm features from left over public nodes (trust_links_filtered)
        ######################

        lines1 = open(path_to_trust_links_file,'r').readlines()
        lines2 = open(path_to_trust_links_filtered_file,'r').readlines()

        trust_links_ori = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links_ori.append(spline)

        print ("Length of trust links (original): ",len(trust_links_ori))

        trust_links_filtered = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')
            trust_links_filtered.append(spline)

        print("Length of trust links (filtered): ", len(trust_links_filtered))

        index_to_be_removed = []
        index_to_keep = []

        for index,tl in enumerate(trust_links_ori):

            if tl not in trust_links_filtered:
                index_to_be_removed.append(index)

            else:
                index_to_keep.append(index)

        print("Number of index to keep: ", len(index_to_keep))
        print ("Number of index to be removed: ",len(index_to_be_removed))

        #------------------------
        # filter std degree file

        std_degree_ori = []
        std_degree_filtered = []

        lines = open(path_to_std_labelled_degree_file,'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            std_degree_ori.append(spline)

        print()
        print ("std degree")
        print (len(std_degree_ori))

        for index,sd in enumerate(std_degree_ori):

            if index in index_to_keep:
                std_degree_filtered.append(sd)

        print (len(std_degree_filtered))

        f = open(path_to_store_filtered_std_labelled_degree_file,'w')

        for sd in std_degree_filtered:
            f.write(','.join(sd)+'\n')

        f.close()

        # ------------------------
        # filter std triad file

        std_triad_ori = []
        std_triad_filtered = []

        lines = open(path_to_std_labelled_triad_file, 'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            std_triad_ori.append(spline)

        print()
        print("std triad")
        print(len(std_triad_ori))

        for index, sd in enumerate(std_triad_ori):

            if index in index_to_keep:
                std_triad_filtered.append(sd)

        print(len(std_triad_filtered))

        f = open(path_to_store_filtered_std_labelled_triad_file, 'w')

        for sd in std_triad_filtered:
            f.write(','.join(sd) + '\n')

        f.close()

        # ------------------------
        # filter std degree triad file

        std_degree_triad_ori = []
        std_degree_triad_filtered = []

        lines = open(path_to_std_labelled_degree_triad_file, 'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            std_degree_triad_ori.append(spline)

        print()
        print("std degree triad")
        print(len(std_degree_triad_ori))

        for index, sd in enumerate(std_degree_triad_ori):

            if index in index_to_keep:
                std_degree_triad_filtered.append(sd)

        print(len(std_degree_triad_filtered))

        f = open(path_to_store_filtered_std_labelled_degree_triad_file, 'w')

        for sd in std_degree_triad_filtered:
            f.write(','.join(sd) + '\n')

        f.close()

        # ------------------------
        # filter norm degree file

        norm_degree_ori = []
        norm_degree_filtered = []

        lines = open(path_to_norm_labelled_degree_file, 'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            norm_degree_ori.append(spline)

        print()
        print("norm degree")
        print(len(norm_degree_ori))

        for index, sd in enumerate(norm_degree_ori):

            if index in index_to_keep:
                norm_degree_filtered.append(sd)

        print(len(norm_degree_filtered))

        f = open(path_to_store_filtered_norm_labelled_degree_file, 'w')

        for sd in norm_degree_filtered:
            f.write(','.join(sd) + '\n')

        f.close()

        # ------------------------
        # filter norm triad file

        norm_triad_ori = []
        norm_triad_filtered = []

        lines = open(path_to_norm_labelled_triad_file, 'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            norm_triad_ori.append(spline)

        print()
        print("norm triad")
        print(len(norm_triad_ori))

        for index, sd in enumerate(norm_triad_ori):

            if index in index_to_keep:
                norm_triad_filtered.append(sd)

        print(len(norm_triad_filtered))

        f = open(path_to_store_filtered_norm_labelled_triad_file, 'w')

        for sd in norm_triad_filtered:
            f.write(','.join(sd) + '\n')

        f.close()

        # ------------------------
        # filter std degree triad file

        norm_degree_triad_ori = []
        norm_degree_triad_filtered = []

        lines = open(path_to_norm_labelled_degree_triad_file, 'r').readlines()

        for line in lines:
            spline = line.rstrip('\n').split(',')
            norm_degree_triad_ori.append(spline)

        print()
        print("norm degree triad")
        print(len(norm_degree_triad_ori))

        for index, sd in enumerate(norm_degree_triad_ori):

            if index in index_to_keep:
                norm_degree_triad_filtered.append(sd)

        print(len(norm_degree_triad_filtered))

        f = open(path_to_store_filtered_norm_labelled_degree_triad_file, 'w')

        for sd in norm_degree_triad_filtered:
            f.write(','.join(sd) + '\n')

        f.close()



#################
# variables
#################


path_to_trust_links_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_filtered.csv' #remember to remove 'filtered' if the filtered file is not available yet!
path_to_trust_links_filtered_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_filtered.csv'

path_to_degree_file = '../output/network/degrees/1_18sep-18oct/unsigned_degree_mentions-following.csv'
path_to_degree_signed_file = '../output/network/degrees/1_18sep-18oct/signed_degree_mentions-following.csv'
path_to_embeddedness_file = '../output/network/embeddedness/by_manual_labelling/1_18sep-18oct/embeddedness_count.csv'
path_to_triad_file = '../output/network/triad/by_manual_labelling/1_18sep-18oct/triad_space.csv'

path_to_store_degree_features = '../output/features/by_manual_labelling/network/degree_features.csv'
path_to_store_triad_features = '../output/features/by_manual_labelling/network/triad_features.csv'
path_to_store_labelled_degree_features_and_target_file = '../output/features/by_manual_labelling/network/labelled_degree.csv'
path_to_store_labelled_triad_features_and_target_file = '../output/features/by_manual_labelling/network/labelled_triad.csv'
path_to_store_labelled_ALL_features_and_target_file = '../output/features/by_manual_labelling/network/labelled_degree_triad.csv'

#------------------
# for filtering std/norm labelled files

path_to_std_labelled_degree_file = '../output/features/by_manual_labelling/network/std_norm/std_labelled_degree.csv'
path_to_std_labelled_triad_file = '../output/features/by_manual_labelling/network/std_norm/std_labelled_triad.csv'
path_to_std_labelled_degree_triad_file = '../output/features/by_manual_labelling/network/std_norm/std_labelled_degree_triad.csv'
path_to_norm_labelled_degree_file = '../output/features/by_manual_labelling/network/std_norm/norm_labelled_degree.csv'
path_to_norm_labelled_triad_file = '../output/features/by_manual_labelling/network/std_norm/norm_labelled_triad.csv'
path_to_norm_labelled_degree_triad_file = '../output/features/by_manual_labelling/network/std_norm/norm_labelled_degree_triad.csv'

path_to_store_filtered_std_labelled_degree_file = '../output/features/by_manual_labelling/network/std_norm/filtered/std_labelled_degree.csv'
path_to_store_filtered_std_labelled_triad_file = '../output/features/by_manual_labelling/network/std_norm/filtered/std_labelled_triad.csv'
path_to_store_filtered_std_labelled_degree_triad_file = '../output/features/by_manual_labelling/network/std_norm/filtered/std_labelled_degree_triad.csv'
path_to_store_filtered_norm_labelled_degree_file = '../output/features/by_manual_labelling/network/std_norm/filtered/norm_labelled_degree.csv'
path_to_store_filtered_norm_labelled_triad_file = '../output/features/by_manual_labelling/network/std_norm/filtered/norm_labelled_triad.csv'
path_to_store_filtered_norm_labelled_degree_triad_file = '../output/features/by_manual_labelling/network/std_norm/filtered/norm_labelled_degree_triad.csv'


if __name__ == '__main__':

    fc = FeatureConstruction()

    #fc.create_degree_features()

    #fc.create_triad_features()

    fc.create_complete_features()

    #--------------
    # create filtered std/norm feature files (AFTER feature scaling has been done)
    # for the trust links that are left over after getting public node timeline tweets
    # NOT needed if already run embeddedness and triad script using filtered trust links!
    #--------------

    #fc.filter_features()