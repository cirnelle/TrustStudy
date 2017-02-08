__author__ = 'yi-linghwong'

import os
import sys
import re
import time


class GetKeywordFeatures():

    def get_keyword_features_profile(self):

        lines1 = open(path_to_trust_links_filtered,'r').readlines()

        trust_links = []
        public_nodes = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)

            if spline[0].lower() not in public_nodes:

                public_nodes.append(spline[0])

        print ("Length of trust links: ",len(trust_links))
        print ("Length of public nodes (unique): ",len(public_nodes))

        profiles = []
        nodes_with_empty_profile = []
        nodes_with_profiles_collected = []

        for n in range(1,7):

            lines = open(path_to_twitter_profile_folder+str(n)+'.csv','r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')
                spline[1] = spline[1].lower()
                #print (spline)

                if spline[0].lower() in public_nodes:

                    nodes_with_profiles_collected.append(spline[0].lower())

                    if spline[1] == '':
                        nodes_with_empty_profile.append(spline[0])

                    else:
                        profiles.append(spline)

        print ()
        print ("Length of nodes with profiles collected: ", len(nodes_with_profiles_collected))
        print ("Length of valid non empty profiles:      ",len(profiles))
        print ("Length of empty profiles:                ",len(nodes_with_empty_profile))

        #---------------------
        # (OPTIONAL) find nodes whose profiles were not collected (FOR CHECKING, might return zero!)

        nodes_without_profile = []

        for pn in public_nodes:

            if pn not in nodes_with_profiles_collected:

                nodes_without_profile.append(pn)

        if len(nodes_without_profile) != 0:

            print ()
            print ('!!!!!!!!!!!!!!!!!')
            print ("Length of nodes without profile: ",len(nodes_without_profile))
            print (nodes_without_profile)
            print ('!!!!!!!!!!!!!!!!!')

        #-----------------------
        # get keywords

        keywords1 = ['stem', 'education', 'teacher', 'science','space', 'astrobiology','space science','astronomy','cosmos','cosmology','astrophysics','hubble','telescope','hubble telescope']
        keywords2 = ['iss','space station','soyuz','astronaut','red planet','jupiter','spacex','rockets','rocket', 'space shuttle']
        keywords3 = ['enceladus','europa moon','saturn','uranus','titan','ganymede','planets','international space station', 'geek', 'technology','innovation']

        keywords = keywords1 + keywords2 + keywords3

        profiles_with_keyword = []
        nodes_with_keyword = []

        for p in profiles:

            profile = re.sub('[^a-zA-Z0-9-_ *]', ' ', p[1])

            for k in keywords:

                keyword = ' '+k+' '

                if keyword in profile:

                    if p[0] not in nodes_with_keyword:

                        profiles_with_keyword.append(p)
                        nodes_with_keyword.append(p[0])

        print ()
        print ("Length of profiles containing keyword: ",len(profiles_with_keyword))

        #-------------------------
        # CHECK for nodes which are in keyword_nodes but are actually trust_no
        #-------------------------

        trust_yes_nodes = []
        wrong_nodes = []

        for tl in trust_links:

            if tl[2] == 'trust_yes':
                if tl[2] not in trust_yes_nodes:
                    trust_yes_nodes.append(tl[0])

        for nk in nodes_with_keyword:
            if nk not in trust_yes_nodes:
                wrong_nodes.append(nk)

        print ()
        print ('!!!!!!!!!!!!!!!!!!!')
        print ("Length of nodes in keyword list but are trust no: ",len(nk))
        print (wrong_nodes)
        print ('!!!!!!!!!!!!!!!!!!!')


        #-------------------------
        # create feature and label

        keyword_and_label = []

        for tl in trust_links:

            if tl[0] in nodes_with_keyword:
                keyword_and_label.append(['1',tl[2]])

            else:
                keyword_and_label.append(['0',tl[2]])

        print ()
        print ("----------------------------")
        print ("Length of keyword and label: ",len(keyword_and_label))


        f = open(path_to_store_labelled_profile_keyword_feature_file,'w')

        for kl in keyword_and_label:
            f.write(','.join(kl)+'\n')

        f.close()


    def get_keyword_features_timeline(self):

        lines1 = open(path_to_trust_links_filtered,'r').readlines()

        trust_links = []
        public_nodes = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            trust_links.append(spline)
            public_nodes.append(spline[0])

        print ("Length of trust links: ",len(trust_links))
        print ("Length of nodes: ",len(trust_links))


        #-----------------------
        # get keywords

        keywords1 = ['science', 'physics', 'space', 'astrobiology', 'space science', 'astronomy', 'evidence', 'phd', 'galaxies', 'exoplanets', 'exoplanet',
                     'cosmos', 'cosmology', 'astrophysics', 'hubble', 'telescope', 'hubble telescope', 'astrophysicist', 'astrophysicists']
        keywords2 = ['iss', 'space station', 'soyuz', 'astronaut', 'astronauts', 'solar system', 'mars', 'red planet', 'jupiter', 'spacex', 'rockets',
                     'rocket', 'space shuttle']
        keywords3 = ['enceladus', 'europa moon', 'saturn', 'uranus', 'titan', 'ganymede', 'planets',
                     'international space station', 'geek', 'technology', 'innovation']

        keywords = keywords1 + keywords2 + keywords3

        timeline_nodes_all = []
        nodes_with_keyword = []
        nodes_and_keyword_count = []

        print ()
        print ("Getting keyword from timeline...")

        t_start = time.time()

        for n in range(1,41):

            print(n)

            timeline_nodes = []

            lines = open(path_to_timeline_tweets_folder + str(n)+'.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                if spline[0] in public_nodes:

                    if spline[0] not in timeline_nodes:
                        timeline_nodes.append(spline[0])

                    if spline[0] not in timeline_nodes_all:
                        timeline_nodes_all.append(spline[0])

                else:
                    print("error")
                    print(spline)

            for tn in timeline_nodes:

                node = tn
                tweet_keywords = []
                keyword_count = 0

                #print (node)

                for line in lines:

                    spline = line.rstrip('\n').split(',')

                    if spline[0] == tn:

                        t1 = spline[-1].replace(',', ' ')

                        tweet = re.sub('[^a-zA-Z0-9-_ *]', ' ', t1)
                        tweet = ' '+tweet+' '

                        #print (tweet)

                        for k in keywords:

                            keyword = ' ' + k + ' '

                            if keyword in tweet:

                                keyword_count += 1
                                tweet_keywords.append(keyword)

                                if node not in nodes_with_keyword:
                                    nodes_with_keyword.append(node)

                # if tweet_keywords != []:
                #
                #     print (tweet_keywords)

                nodes_and_keyword_count.append([node,str(keyword_count)])

        print ()
        print ("Length of nodes with keyword: ",len(nodes_with_keyword))
        print ("Length of all nodes in timeline files: ", len(timeline_nodes_all))
        print ("Length of nodes AND keyword list (should be the same as above): ",len(nodes_and_keyword_count))


        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        #print (nodes_and_keyword_count)

        nodes_and_keyword_count_dict = {}

        for nk in nodes_and_keyword_count:

            key = nk[0]
            nodes_and_keyword_count_dict[key] = nk[1]

        #-------------------------
        # create feature and label

        keyword_and_label = []

        for tl in trust_links:

            if tl[0] in nodes_and_keyword_count_dict:
                keyword_and_label.append([nodes_and_keyword_count_dict[tl[0]], tl[2]])

            else:
                keyword_and_label.append(['0', tl[2]])

        print()
        print("----------------------------")
        print("Length of keyword and label: ", len(keyword_and_label))

        f = open(path_to_store_labelled_timeline_keyword_feature_file, 'w')

        for kl in keyword_and_label:
            f.write(','.join(kl) + '\n')

        f.close()


    def combine_profile_and_timeline_keyword_features(self):

        lines1 = open(path_to_store_labelled_profile_keyword_feature_file,'r').readlines()
        lines2 = open(path_to_store_labelled_timeline_keyword_feature_file,'r').readlines()

        profile_features = []
        profile_trust_labels = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            profile_features.append(spline[0])
            profile_trust_labels.append(spline[-1])

        print("Length of profile features: ", len(profile_features))

        timeline_features = []
        timeline_trust_labels = []

        for line in lines2:
            spline = line.rstrip('\n').split(',')
            timeline_features.append(spline[0])
            timeline_trust_labels.append(spline[-1])

        print("Length of timeline features: ", len(timeline_features))

        if profile_trust_labels == timeline_trust_labels:

            trust_labels = profile_trust_labels

            zipped = zip(profile_features,timeline_features,trust_labels)

            combine_features_labels = []

            for z in zipped:

                z = list(z)
                combine_features_labels.append(z)

            print ("Length of combined features: ",len(combine_features_labels))

            f = open(path_to_store_labelled_profile_timeline_keyword_feature_file,'w')

            for cf in combine_features_labels:
                f.write(','.join(cf)+'\n')

            f.close()


        else:

            print ("Trust label lists not equal, exiting...")

            sys.exit()




################
# variables
################

path_to_trust_links_filtered = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_filtered.csv'
path_to_twitter_profile_folder = '../output/profile_description/1_18sep-18oct/profile_'
path_to_timeline_tweets_folder = '../output/timeline_tweets/1_18sep-18oct/timeline/timeline_tweets_'

path_to_store_labelled_profile_keyword_feature_file = '../output/features/by_manual_labelling/keyword/labelled_keyword_profile.csv'
path_to_store_labelled_timeline_keyword_feature_file = '../output/features/by_manual_labelling/keyword/labelled_keyword_timeline.csv'
path_to_store_labelled_profile_timeline_keyword_feature_file = '../output/features/by_manual_labelling/keyword/labelled_keyword_profile_timeline.csv'



if __name__ == '__main__':

    gk = GetKeywordFeatures()

    #gk.get_keyword_features_profile()

    #gk.get_keyword_features_timeline()

    gk.combine_profile_and_timeline_keyword_features()

