__author__ = 'yi-linghwong'

import os
import sys
import time

class FeatureConstruction():


    def combine_network_liwc_features(self):

        lines1 = open(path_to_network_feature_file,'r').readlines()
        lines2 = open(path_to_liwc_feature_file,'r').readlines()

        network_features = []
        network_trust_labels = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            network_features.append(spline[:-1])
            network_trust_labels.append(spline[-1])

        print ("Length of network features: ",len(network_features))
        print ("Length of network trust labels: ",len(network_trust_labels))

        liwc_features = []
        liwc_trust_labels = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')
            liwc_features.append(spline[:-1])
            liwc_trust_labels.append(spline[-1])

        print ("Length of liwc features: ",len(liwc_features))
        print("Length of liwc trust labels: ", len(liwc_trust_labels))

        if network_trust_labels == liwc_trust_labels:

            trust_labels = [[nt] for nt in network_trust_labels]

            if len(network_features) == len(liwc_features) == len(trust_labels):

                zipped = zip(network_features,liwc_features)

                features_combined = []

                for z in zipped:

                    z = list(z)
                    y = [item for sublist in z for item in sublist] #flatten the list (to make the list of list into one list)

                    features_combined.append(y)

                print ()
                print ("Length of combined feature list: ",len(features_combined))

                zipped1 = zip(features_combined,trust_labels)

                features_and_labels = []

                for z in zipped1:

                    z = list(z)
                    y = [item for sublist in z for item in sublist]  # flatten the list (to make the list of list into one list)
                    features_and_labels.append(y)

                print ("Length of combined feature and label list: ",len(features_and_labels))

                f = open(path_to_store_combined_network_liwc_features_file,'w')

                for fl in features_and_labels:
                    f.write(','.join(fl)+'\n')

                f.close()


            else:
                print ("Length of feature lists not equal, exiting...")
                sys.exit()


        else:
            print ("Trust label lists not the same, exiting...")
            sys.exit()


    def combine_network_liwc_keyword_features(self):

        lines1 = open(path_to_network_feature_file, 'r').readlines()
        lines2 = open(path_to_liwc_feature_file, 'r').readlines()
        lines3 = open(path_to_keyword_feature_file,'r').readlines()

        network_features = []
        network_trust_labels = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            network_features.append(spline[:-1])
            network_trust_labels.append(spline[-1])

        print("Length of network features: ", len(network_features))
        print("Length of network trust labels: ", len(network_trust_labels))

        liwc_features = []
        liwc_trust_labels = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')
            liwc_features.append(spline[:-1])
            liwc_trust_labels.append(spline[-1])

        print("Length of liwc features: ", len(liwc_features))
        print("Length of liwc trust labels: ", len(liwc_trust_labels))

        keyword_features = []
        keyword_trust_labels = []

        for line in lines3:
            spline = line.rstrip('\n').split(',')
            keyword_features.append(spline[:-1])
            keyword_trust_labels.append(spline[-1])

        print("Length of keyword features: ", len(keyword_features))
        print("Length of keyword trust labels: ", len(keyword_trust_labels))

        if network_trust_labels == liwc_trust_labels == keyword_trust_labels:

            trust_labels = [[nt] for nt in network_trust_labels]

            if len(network_features) == len(liwc_features) == len(keyword_features) == len(trust_labels):

                zipped = zip(network_features, liwc_features, keyword_features)

                features_combined = []

                for z in zipped:
                    z = list(z)
                    y = [item for sublist in z for item in
                         sublist]  # flatten the list (to make the list of list into one list)

                    features_combined.append(y)

                print()
                print("Length of combined feature list: ", len(features_combined))

                zipped1 = zip(features_combined, trust_labels)

                features_and_labels = []

                for z in zipped1:
                    z = list(z)
                    y = [item for sublist in z for item in
                         sublist]  # flatten the list (to make the list of list into one list)
                    features_and_labels.append(y)

                print("Length of combined feature and label list: ", len(features_and_labels))

                f = open(path_to_store_combined_network_liwc_keyword_features_file, 'w')

                for fl in features_and_labels:
                    f.write(','.join(fl) + '\n')

                f.close()


            else:
                print("Length of feature lists not equal, exiting...")
                sys.exit()


        else:
            print("Trust label lists not the same, exiting...")
            sys.exit()


    def remove_useless_features(self):

        ###################
        # after checking feature importance, this function can be used to remove insignificant features
        ##################

        #------------------
        # remove triad features t12, t13, t14, t15, t16

        lines = open(path_to_store_combined_network_liwc_keyword_features_file,'r').readlines()

        print ("Length of list (before): ",len(lines))

        updated_features = []

        for line in lines[:1]:
            spline = line.rstrip('\n').split(',')
            print ("Number of features (before): ",len(spline))


        for line in lines:
            spline = line.rstrip('\n').split(',')

            for n in range (5): # remove index 18 to 22, i.e. remove item at index 18 five times!

                spline.pop(18)

            updated_features.append(spline)

        print ()
        print ("Length of list (after): ",len(updated_features))
        print ("Number of features (after): ",len(updated_features[1]))

        f = open(path_to_store_combined_network_liwc_keyword_features_file,'w')

        for uf in updated_features:
            f.write(','.join(uf)+'\n')

        f.close()









##################
# variables
##################

path_to_network_feature_file = '../output/features/by_manual_labelling/network/std_norm/norm_labelled_degree_triad.csv'
path_to_liwc_feature_file = '../output/features/by_manual_labelling/liwc/std_norm/norm_labelled_liwc.csv'
path_to_keyword_feature_file = '../output/features/by_manual_labelling/keyword/std_norm/norm_labelled_keyword_profile_timeline.csv'

path_to_store_combined_network_liwc_features_file = '../output/features/by_manual_labelling/_combined/std_norm/norm_labelled_combined.csv'
path_to_store_combined_network_liwc_keyword_features_file = '../output/features/by_manual_labelling/_combined/std_norm/norm_labelled_combined_all.csv'


if __name__ == '__main__':

    fc = FeatureConstruction()

    #fc.combine_network_liwc_features()

    #fc.combine_network_liwc_keyword_features()

    fc.remove_useless_features()