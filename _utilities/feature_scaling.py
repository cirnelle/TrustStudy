__author__ = 'yi-linghwong'

import os
import sys
import pandas as pd
import numpy as np
from sklearn import preprocessing
import random


degree_column = ['u_out_pos','u_out_neg','v_in_pos','v_in_neg','u_out','v_in','embeddedness']
triad_column = ['t1','t2','t3','t4','t5','t6','t7','t8','t9','t10','t11','t12','t13','t14','t15','t16']
target = ['class']

column_names = degree_column+triad_column+target


class FeatureScaling():


    def standardise_features(self):

        #dataset = pd.read_csv(path_to_labelled_features_file, usecols=[0,1,2,3,4,5,6,23], names=column_names) # to use only degree features
        dataset = pd.read_csv(path_to_labelled_features_file, names=column_names)

        standardised = []

        for cn in column_names[:-1]:

            dataset[cn] = dataset[cn].astype(float)

            std_scale = preprocessing.StandardScaler().fit(dataset[cn])
            data_std = std_scale.transform(dataset[cn])

            standardised.append(data_std)

            # print (data_std.mean())
            # print (data_std.std())

            # print (len(data_std))
            # print (data_std)

        print (len(standardised))

        standardised_transformed = np.array(standardised).T.tolist() # transpose list of list

        print (len(standardised_transformed))

        standardised_final = []

        for st in standardised_transformed:

            t1 = []

            for s in st:

                s = round(s, 2)
                s = str(s)
                t1.append(s)

            standardised_final.append(t1)

        # get targets

        lines = open(path_to_trust_link_file,'r').readlines()

        targets = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            targets.append([spline[-1]])

        print (len(targets))

        if len(targets) == len(standardised_final):

            zipped = zip(standardised_final,targets)

            standardised_with_target = []

            for z in zipped:
                z = list(z)
                z1 = z[0] + z[1]

                standardised_with_target.append(z1)

            f = open(path_to_store_standardised_feature_file,'w')

            for sf in standardised_with_target:
                f.write(','.join(sf)+'\n')

            f.close()

        else:

            print ("Length of target and feature lists not equal, CHECK!!")

        return standardised_with_target,targets


    def normalise_features(self):

        # minmax_scale = preprocessing.MinMaxScaler().fit(dataset[['u_out_pos']])
        # data_minmax = minmax_scale.transform(dataset[['u_out_pos']])

        # dataset = pd.read_csv(path_to_labelled_features_file, usecols=[0,1,2,3,4,5,6,23], names=column_names) # to use only degree features
        dataset = pd.read_csv(path_to_labelled_features_file, names=column_names)

        normalised = [] # normalised is another name for minmax

        for cn in column_names[:-1]:
            dataset[cn] = dataset[cn].astype(float)

            minmax_scale = preprocessing.MinMaxScaler().fit(dataset[cn])
            data_minmax = minmax_scale.transform(dataset[cn])

            normalised.append(data_minmax)

            # print (data_minmax.min())
            # print (data_minmax.max())

            # print (len(data_minmax))
            # print (data_minmax)

        print(len(normalised))

        normalised_transformed = np.array(normalised).T.tolist()  # transpose list of list

        print(len(normalised_transformed))

        normalised_final = []

        for nt in normalised_transformed:

            t1 = []

            for n in nt:
                n = round(n, 4)
                n = str(n)
                t1.append(n)

            normalised_final.append(t1)

        # get targets

        lines = open(path_to_trust_link_file, 'r').readlines()

        targets = []

        for line in lines:
            spline = line.rstrip('\n').split(',')
            targets.append([spline[-1]])

        print(len(targets))

        if len(targets) == len(normalised_final):

            zipped = zip(normalised_final,targets)

            normalised_with_target = []

            for z in zipped:
                z = list(z)
                z1 = z[0] + z[1]

                normalised_with_target.append(z1)

            f = open(path_to_store_normalised_feature_file, 'w')

            for nf in normalised_with_target:
                f.write(','.join(nf) + '\n')

            f.close()

        else:

            print("Length of target and feature lists not equal, CHECK!!")

        return normalised_with_target,targets


    def balance_class(self):

        targets = self.standardise_features()[1]

        trust_no = []
        trust_yes = []

        for t in targets:

            if t == ['trust_yes']:
                trust_yes.append(t)

            elif t == ['trust_no']:
                trust_no.append(t)

        print ()
        print ("Length of trust_yes: "+str(len(trust_yes)))
        print ("Length of trust_no: "+str(len(trust_no)))

        n = min(len(trust_yes),len(trust_no)) # previously n = len(trust_no)
        m = max(len(trust_yes),len(trust_no))  # previously m = len(trust_yes)
        index_list = list(range(0,m))

        random_index_list = random.sample(index_list,n) # list of random index for the longer list
        print (random_index_list)

        print ("Length of random index list: "+str(len(random_index_list)))
        print ()

        #-----------------
        # extract random item from standardised list of the longer list

        standardised = self.standardise_features()[0]

        trust_no_s = []
        trust_yes_s = []

        for s in standardised:
            if s[-1] == 'trust_yes':
                trust_yes_s.append(s)

            if s[-1] == 'trust_no':
                trust_no_s.append(s)

        # find out which list needs to be trimmed

        if len(trust_yes_s) > len(trust_no_s):

            to_be_sampled_s = trust_yes_s
            no_need_sampling_s = trust_no_s

            print ("Longer list to be sampled is trust_yes list.")

        if len(trust_no_s) > len(trust_yes_s):

            to_be_sampled_s = trust_no_s
            no_need_sampling_s = trust_yes_s

            print("Longer list to be sampled is trust_no list.")

        else:

            print ("Lists have equal length.")

        trust_list_sampled_s = []

        for index,tb in enumerate(to_be_sampled_s):

            if index in random_index_list:

                trust_list_sampled_s.append(tb)

        print ()
        print ("Length of sampled standardised list: "+str(len(trust_list_sampled_s)))

        standardised_balanced = trust_list_sampled_s + no_need_sampling_s
        print ("Length of standardised balanced list: "+str(len(standardised_balanced)))
        print()

        f = open(path_to_store_balance_class_standardised_feature_file,'w')

        for sb in standardised_balanced:
            f.write(','.join(sb)+'\n')

        f.close()

        # -----------------
        # extract random trust_yes from normalised list

        normalised = self.normalise_features()[0]

        trust_no_n = []
        trust_yes_n = []

        for n in normalised:
            if n[-1] == 'trust_yes':
                trust_yes_n.append(n)

            if n[-1] == 'trust_no':
                trust_no_n.append(n)

        # find out which list needs to be trimmed

        if len(trust_yes_n) > len(trust_no_n):

            to_be_sampled_n = trust_yes_n
            no_need_sampling_n = trust_no_n

            print("Longer list to be sampled is trust_yes list.")

        if len(trust_no_n) > len(trust_yes_n):

            to_be_sampled_n = trust_no_n
            no_need_sampling_n = trust_yes_n

            print("Longer list to be sampled is trust_no list.")

        else:

            print("Lists have equal length.")


        trust_list_sampled_n = []

        for index, tb in enumerate(to_be_sampled_n):

            if index in random_index_list:
                trust_list_sampled_n.append(tb)

        print()
        print("Length of sampled normalised list: " + str(len(trust_list_sampled_n)))

        normalised_balanced = trust_list_sampled_n + no_need_sampling_n
        print("Length of normalised balanced list: " + str(len(normalised_balanced)))
        print()


        f = open(path_to_store_balance_class_normalised_feature_file, 'w')

        for nb in normalised_balanced:
            f.write(','.join(nb) + '\n')

        f.close()


################
# variables
################

path_to_labelled_features_file = '../output/features/by_trust_dictionary/strict/labelled_degree_and_triad.csv'
path_to_trust_link_file = '../output/trust_links/by_trust_dictionary/strict/trust_links_space.csv'

path_to_store_standardised_feature_file = '../output/features/by_trust_dictionary/strict/std_norm/standardised_labelled_degree_triad.csv'
path_to_store_normalised_feature_file = '../output/features/by_trust_dictionary/strict/std_norm/normalised_labelled_degree_triad.csv'

path_to_store_balance_class_standardised_feature_file = '../output/features/by_trust_dictionary/strict/std_norm/balanced_std_labelled_degree_triad.csv'
path_to_store_balance_class_normalised_feature_file = '../output/features/by_trust_dictionary/strict/std_norm/balanced_norm_labelled_degree_triad.csv'


if __name__ == '__main__':

    fs = FeatureScaling()

    #fs.standardise_features()

    fs.normalise_features()

    #fs.balance_class()
