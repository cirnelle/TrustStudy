__author__ = 'yi-linghwong'

import os
import sys
import time
import multiprocessing
import re


class GetTrustLinksByMentionsFollowing():


    def get_unique_mentions(self):

        print()
        print("Getting all mentions ...")

        lines1 = open(path_to_all_mentions_file, 'r').readlines()

        mentions = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            mentions.append(spline)

        # print (mentions)
        print("Length of mention list: " + str(len(mentions)))

        print()
        print("Getting unique mentions ...")

        t_start = time.time()

        mentions_set = set(map(tuple,mentions)) # result: {[1,2], [3,4]}
        mentions_unique_tuple = list(mentions_set) # result: [(1,2), (3,4)]
        mentions_unique = [list(mu) for mu in mentions_unique_tuple] # convert list of tuples to list of list

        print("Length of complete mentions: " + str(len(mentions)))
        print("Length of unique mentions: " + str(len(mentions_unique)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        f = open(path_to_store_unique_mentions, 'w')

        for uq in mentions_unique:
            f.write(','.join(uq) + '\n')

        f.close()


    def combine_following_files(self):

        following_list = []

        for n in range(1, 21):
            lines = open(path_to_following_list_folder + str(n) + '.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')
                following_list.append(spline)

        print ("Length of combined following list: "+str(len(following_list)))

        f = open(path_to_store_combined_following_list,'w')

        for fl in following_list:
            f.write(','.join(fl)+'\n')

        f.close()


    def get_trust_links(self):

        print("Getting following dict ...")

        following_dict = {}

        for n in range(1,21):
            lines = open(path_to_following_list_folder + str(n) + '.csv', 'r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                key = spline[0]
                value = []

                for n in range(1, len(spline) - 1, 2):
                    value.append([spline[n], spline[n + 1]])

                following_dict[key] = (value)

        #print (following_dict)
        print("Length of following dict: " + str(len(following_dict)))


        print ()
        print ("Getting all mentions ...")

        lines1 = open(path_to_all_mentions_file, 'r').readlines()

        mentions = []

        for line in lines1:

            spline = line.rstrip('\n').split(',')
            mentions.append(spline)

        #print (mentions)
        print ("Length of mention list: "+str(len(mentions)))

        print ()
        print ("Getting unique mentions ...")

        t_start = time.time()

        mentions_set = set(map(tuple,mentions)) # result: {[1,2], [3,4]}
        mentions_unique_tuple = list(mentions_set) # result: [(1,2), (3,4)]
        mentions_unique = [list(mu) for mu in mentions_unique_tuple] # convert list of tuples to list of list

        print ("Length of complete mentions: "+str(len(mentions)))
        print ("Length of unique mentions: "+str(len(mentions_unique)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        print ()
        print ("Getting trust links ...")

        t_start = time.time()

        trust_links = []
        trust_yes = []
        trust_no = []
        trust_unsure = [] # only negative mentions but follows the user


        for m in mentions_unique:

            if m[0] in following_dict:

                foll_list = []

                for v in following_dict[m[0]]:

                    foll_list.append(v[1])

                    if m[1] == v[1]:

                        if m[2] == 'pos':

                            trust_links.append([m[0],m[1],'trust_yes'])
                            trust_yes.append([m[0],m[1]])

                if m[2] == 'neg':

                    if m[1] not in foll_list:

                        trust_links.append([m[0],m[1],'trust_no'])
                        trust_no.append([m[0], m[1]])

                    if m[1] in foll_list:

                        trust_unsure.append([m[0], m[1]])



        # DO NOT NEED TO check for and remove ambiguous links that exist in both yes and no list
        # because a user can't both follow AND not follow another use (we checked for both)
        # but check for duplicates (i.e. within trust_yes and trust_no)


        print ("Length of trust link YES list: "+str(len(trust_yes)))
        print ("Length of trust link NO list: "+str(len(trust_no)))
        print ("Length of trust link UNSURE list (-ve mentions but follow): "+str(len(trust_unsure)))
        print ("Length of all trust links: "+str(len(trust_links)))

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        # write to file

        f = open(path_to_store_trust_links_file,'w')

        for tl in trust_links:
            f.write(','.join(tl)+'\n')

        f.close()


    def divide_unique_mentions(self):

        lines = open(path_to_store_unique_mentions,'r').readlines()

        mentions_unique = []

        for line in lines:
            spline = line.rstrip('\n').split(',')

            mentions_unique.append(spline)

        n = int(len(mentions_unique) / 20) + 1

        divided_list = [mentions_unique[i:i+n] for i in range(0, len(mentions_unique), n)]
        #print (len(divided_list))

        return divided_list



    def get_trust_links_strict(self,i):

        ##################
        # apply stronger filter (e.g. -ve mentions more than twice)
        ##################

        #print("Getting following dict ...")

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

        lines1 = open(path_to_all_mentions_file, 'r').readlines()

        mentions = []

        for line in lines1:
            spline = line.rstrip('\n').split(',')
            mentions.append(spline)

        #print()
        #print("Getting trust links ...")

        t_start = time.time()

        mentions_unique = self.divide_unique_mentions()[i-1]

        print(len(mentions_unique))

        trust_links = []
        trust_yes = []
        trust_no = []
        trust_unsure = []  # only negative mentions but follows the user

        for m in mentions_unique:

            if m[0] in following_dict:

                foll_list = []

                for v in following_dict[m[0]]:
                    foll_list.append(v[1])

            else:
                foll_list = []

            if m[2] == 'pos':

                if mentions.count([m[0], m[1], 'pos']) >= 3:  # only assign a trust label if 3 or more +ve mentions AND follow

                    for fl in foll_list:

                        if m[1] == fl:

                            trust_links.append([m[0], m[1], 'trust_yes'])
                            trust_yes.append([m[0], m[1]])

            elif m[2] == 'neg':

                if mentions.count([m[0], m[1], 'neg']) >= 2:

                    if m[1] not in foll_list:

                        trust_links.append([m[0], m[1], 'trust_no'])
                        trust_no.append([m[0], m[1]])

                    if m[1] in foll_list:

                        trust_unsure.append([m[0], m[1]])


                #############
                # uncomment the following two lines and comment the above lines if we take only 3 -ve's as
                # sign of distrust and disregard if the user follows the mentioned user
                #############

                # if mentions.count([m[0], m[1], 'neg']) >= 2:
                #
                #     trust_links.append([m[0], m[1], 'trust_no'])

        # print("Length of trust link YES list: " + str(len(trust_yes)))
        # print("Length of trust link NO list: " + str(len(trust_no)))
        # print("Length of trust link UNSURE list (-ve mentions but follow): " + str(len(trust_unsure)))
        # print("Length of all trust links: " + str(len(trust_links)))


        t_end = time.time()
        total_time = round(((t_end - t_start) / 60), 2)
        print("Computing time was " + str(total_time) + " minutes.")

        # write to file

        f = open(path_to_store_trust_links_strict_folder+str(i)+'.csv', 'w')

        for tl in trust_links:
            f.write(','.join(tl) + '\n')

        f.close()


    def combine_trust_links_strict_files(self):

        trust_yes = []
        trust_no = []
        trust_all = []

        for n in range(1,21):

            lines = open(path_to_store_trust_links_strict_folder+str(n)+'.csv','r').readlines()

            for line in lines:
                spline = line.rstrip('\n').split(',')

                if spline not in trust_all:

                    trust_all.append(spline)

                    if spline[2] == 'trust_yes':

                        trust_yes.append(spline)

                    if spline[2] == 'trust_no':
                        trust_no.append(spline)

        print ("Length of trust yes list: "+str(len(trust_yes)))
        print ("Length of trust no list: "+str(len(trust_no)))
        print ("Length of trust list all: "+str(len(trust_all)))


        f = open(path_to_store_trust_links_strict,'w')

        for tl in trust_all:
            f.write(','.join(tl)+'\n')

        f.close()


class GetTrustLinksByTrustDictionary():


    def get_scientist_and_public_list(self):

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_additional_space_user_list, 'r').readlines()
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

            if spline[0].lower() in scientist_all:
                scientists.append(spline[0].lower())

            else:
                public.append(spline[0].lower())

        # print (scientists)
        # print (public)

        return scientists, public


    def get_trust_links_liwc(self):

    ###################
    # Use LIWC to get tweets that contain swear words, these tweets indicate distrust
    ###################

        lines1 = open(path_to_liwc_public_mention_scientist_file,'r').readlines()
        lines2 = open(path_to_liwc_scientist_mention_public_file,'r').readlines()

        tweet_and_swear_word = []

        for line in lines1[1:]:
            spline = line.rstrip('\n').split('\t')
            tweet_and_swear_word.append([spline[0].lower(),spline[-2],spline[-1]])

        for line in lines2[1:]:
            spline = line.rstrip('\n').split('\t')
            tweet_and_swear_word.append([spline[0].lower(),spline[-2],spline[-1]])

        scientists = self.get_scientist_and_public_list()[0]
        public = self.get_scientist_and_public_list()[1]

        trust_links_list = []

        trust_links_tweets = []

        for ts in tweet_and_swear_word:

            if float(ts[2]) != 0.00:

                tweet_text = ' ' + ts[1].lower() + ' '

                mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

                if ts[0] in public:

                    public_user = ts[0]

                    for ml in mention_list:
                        if ml[1:] in scientists:  # remove '@' and then check if it is a scientist

                            scientist_user = ml[1:]

                            trust_links_list.append([public_user, scientist_user, 'trust_no'])
                            trust_links_tweets.append([public_user, 'trust_no', ts[1]])

                if ts[0] in scientists:

                    scientist_user = ts[0]

                    for ml in mention_list:
                        if ml[1:] in public:  # remove '@' and then check if it is a scientist

                            public_user = ml[1:]

                            trust_links_list.append([scientist_user, public_user, 'trust_no'])
                            trust_links_tweets.append([scientist_user, 'trust_no',ts[1]])

        print ("Length of trust_no list (contains swear words) is "+str(len(trust_links_list)))
        print (len(trust_links_tweets))

        f = open(path_to_store_trust_links_all_with_tweets, 'w')

        for tt in trust_links_tweets:
            f.write(','.join(tt) + '\n')

        f.close()

        return trust_links_list


    def get_trust_links_dictionary(self):

    ###############
    # get trust links by filtering for words present in trust dictionary
    ###############

        lines1 = open(path_to_trust_dictionary,'r').readlines()
        lines2 = open(path_to_distrust_dictionary,'r').readlines()
        lines3 = open(path_to_public_mention_scientist_tweets,'r').readlines()
        lines4 = open(path_to_scientist_mention_public_tweets,'r').readlines()

        trust_word_list = []
        distrust_word_list = []

        for line in lines1:
            spline = line.rstrip('\n').rstrip(' ')
            trust_word_list.append(spline.lower())

        for line in lines2:
            spline = line.rstrip('\n').rstrip(' ')
            distrust_word_list.append(spline.lower())

        tweets_and_author =[]

        lines = lines3 + lines4

        for line in lines:
            spline = line.rstrip('\n').split(',')
            tweets_and_author.append([spline[0].lower(),spline[-1].lower()])


        #tweets_and_author = [['dunlap_obs', 'something independent green bank don\'t trust value radio observatory inaugurated - astrobiology https://t.co/ahy5xcf03m via @astrobiology']]

        tweets_trust_yes = []
        tweets_trust_no = []

        trust_links_tweets = []

        print ()
        print ("Getting trust_yes and trust_no lists (dictionary)...")

        t_start = time.time()

        for ta in tweets_and_author:

            tweet = ta[1].split()

            #----------------
            # get trust_yes tweets
            #----------------

            trust_words = []

            for tw in trust_word_list:

                pattern = '^' + tw

                for index,t in enumerate(tweet):

                    trust_word = re.findall(pattern,t)

                    if trust_word != []:

                        #print(trust_word)

                        if tweet[index-1] != 'not' and not (bool(re.search('n\'t',tweet[index-1]))): ### CHECK FOR NEGATION (e.g. "do NOT trust" or 'DON'T trust' ###

                            trust_words.append(trust_word)

            if trust_words != []:

                #print (trust_words)

                tweets_trust_yes.append([ta[0],ta[1],'trust_yes',len(trust_words)])
                trust_links_tweets.append([ta[0], 'trust_yes', ta[1]])

            #----------------
            # get trust_no_tweets
            #----------------

            distrust_words = []

            for dw in distrust_word_list:

                pattern = '^' + dw

                for index, t in enumerate(tweet):

                    distrust_word = re.findall(pattern, t)

                    if distrust_word != []:

                        # print(trust_word)

                        if tweet[index - 1] != 'not' and not (bool(re.search('n\'t', tweet[index - 1]))):  ### CHECK FOR NEGATION (e.g. "do NOT trust" or 'DON'T trust' ###

                            distrust_words.append(distrust_word)

            if distrust_words != []:

                # print (distrust_words)

                tweets_trust_no.append([ta[0], ta[1], 'trust_no', len(distrust_words)])
                trust_links_tweets.append([ta[0], 'trust_no', ta[1]])

        t_end = time.time()
        total_time = round(((t_end - t_start) / 60),2)
        print("Computing time was " + str(total_time) + " minutes.")


        print()
        print ("Length of trust_yes tweet: "+str(len(tweets_trust_yes)))
        print (tweets_trust_yes[:10])

        print("Length of trust_no tweet: " + str(len(tweets_trust_no)))
        print (tweets_trust_no[:10])

        print(len(trust_links_tweets))

        f = open(path_to_store_trust_links_all_with_tweets, 'a')

        for tt in trust_links_tweets:
            f.write(','.join(tt) + '\n')

        f.close()

        #################
        # get trust links
        #################

        scientists = self.get_scientist_and_public_list()[0]
        public = self.get_scientist_and_public_list()[1]

        print ()

        print ("Getting trust links ...")

        trust_links_list = []

        for tty in tweets_trust_yes:

            tweet_text = ' ' + tty[1] + ' '

            mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            if tty[0] in public:

                public_user = tty[0]

                for ml in mention_list:

                    if ml[1:] in scientists:  # remove '@' and then check if it is a scientist

                        scientist_user = ml[1:]

                        trust_links_list.append([public_user, scientist_user, 'trust_yes'])

            if tty[0] in scientists:

                scientist_user = tty[0]

                for ml in mention_list:

                    if ml[1:] in public:  # remove '@' and then check if it is a scientist

                        public_user = ml[1:]

                        trust_links_list.append([scientist_user, public_user, 'trust_yes'])


        for ttn in tweets_trust_no:

            tweet_text = ' ' + ttn[1] + ' '

            mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

            if ttn[0] in public:

                public_user = ttn[0]

                for ml in mention_list:

                    if ml[1:] in scientists:  # remove '@' and then check if it is a scientist

                        scientist_user = ml[1:]

                        trust_links_list.append([public_user, scientist_user, 'trust_no'])

            if ttn[0] in scientists:

                scientist_user = ttn[0]

                for ml in mention_list:

                    if ml[1:] in public:  # remove '@' and then check if it is a scientist

                        public_user = ml[1:]

                        trust_links_list.append([scientist_user, public_user, 'trust_no'])

        print ("Length of trust link: "+str(len(trust_links_list)))

        return trust_links_list


    def get_trust_links_combined(self):

        trust_links_liwc = self.get_trust_links_liwc()
        trust_links_dictionary = self.get_trust_links_dictionary()

        trust_links_all = trust_links_liwc + trust_links_dictionary

        print ()
        print ("--------------------------------")
        print ("Length of combined trust links list: "+str(len(trust_links_all)))

        #print (trust_links_all)

        #-----------------------
        # remove duplicate by aggregating their scores (e.g. 2 trust_no, 1 trust yes = trust_no; 1 trust_no, 1 trust_yes = trust_no
        #-----------------------

        #trust_links_all = [['1pherris', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_no'],['halohooper', 'nasa','trust_yes'],['halohooper', 'nasa','trust_no']]

        trust_pair_unique = []
        duplicates = []

        for tl in trust_links_all:

            first = tl[0]
            second = tl[1]

            if [first,second] not in trust_pair_unique:

                trust_pair_unique.append([first,second])

            else:

                duplicates.append([first,second])

        # subfunction to compare sublist

        def isSubList(list,sub_list):

            slice = [list[0],list[1]]

            if sub_list == slice:

                return True

            else:

                return False


        trust_links_unique = []

        for tp in trust_pair_unique:

            trust_values = []

            for tl in trust_links_all:

                if isSubList(tl,tp):

                    trust_values.append(tl[2])

            if len(trust_values) > 1:

                trust_yes_count = trust_values.count('trust_yes')
                trust_no_count = trust_values.count('trust_no')

                if trust_yes_count > trust_no_count:

                    trust_value = 'trust_yes'

                if trust_yes_count < trust_no_count:

                    trust_value = 'trust_no'

                if trust_yes_count == trust_no_count:

                    trust_value = 'trust_yes'

            elif len(trust_values) == 1:

                trust_value = trust_values[0]

            else:

                print ("error")

            trust_links_unique.append([tp[0],tp[1],trust_value])


        print ("Length of unique trust link list: "+str(len(trust_links_unique)))
        #print (trust_links_unique)
        #print (duplicates)

        f = open(path_to_store_trust_links_unique,'w')

        for tlu in trust_links_unique:

            f.write(','.join(tlu)+'\n')

        f.close()


    def get_trust_links_combined_strict(self):

        trust_links_liwc = self.get_trust_links_liwc()
        trust_links_dictionary = self.get_trust_links_dictionary()

        trust_links_all = trust_links_liwc + trust_links_dictionary

        print()
        print("--------------------------------")
        print("Length of combined trust links list: " + str(len(trust_links_all)))

        # print (trust_links_all)

        # -----------------------
        # remove duplicate by aggregating their scores (e.g. 2 trust_no, 1 trust yes = trust_no; 1 trust_no, 1 trust_yes = trust_no
        # -----------------------

        # trust_links_all = [['1pherris', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_yes'],['orbfungi', 'nasa','trust_no'],['halohooper', 'nasa','trust_yes'],['halohooper', 'nasa','trust_no']]

        trust_pair_unique = []
        duplicates = []

        for tl in trust_links_all:

            first = tl[0]
            second = tl[1]

            if [first, second] not in trust_pair_unique:

                trust_pair_unique.append([first, second])

            else:

                duplicates.append([first, second])

        # subfunction to compare sublist

        def isSubList(list, sub_list):

            slice = [list[0], list[1]]

            if sub_list == slice:

                return True

            else:

                return False

        trust_links_unique = []

        for tp in trust_pair_unique:

            trust_values = []

            for tl in trust_links_all:

                if isSubList(tl, tp):
                    trust_values.append(tl[2])

            if len(trust_values) > 1:

                trust_yes_count = trust_values.count('trust_yes')
                trust_no_count = trust_values.count('trust_no')

                if trust_yes_count > trust_no_count:
                    trust_value = 'trust_yes'

                if trust_yes_count < trust_no_count:
                    trust_value = 'trust_no'

                if trust_yes_count == trust_no_count:
                    trust_value = 'trust_yes'

            elif len(trust_values) == 1:

                trust_value = 'nil'

            else:

                print("error")

            trust_links_unique.append([tp[0], tp[1], trust_value])

        print("Length of unique trust link list: " + str(len(trust_links_unique)))
        # print (trust_links_unique)
        # print (duplicates)

        trust_links_strict = []

        for tl in trust_links_unique:

            if tl[2] != 'nil':
                trust_links_strict.append(tl)

        print ("Length of trust links strict: ",len(trust_links_strict))

        f = open(path_to_store_trust_links_unique_strict, 'w')

        for tls in trust_links_strict:
            f.write(','.join(tls) + '\n')

        f.close()

class GetTrustLinksByManualLabelling():


    def get_scientist_and_public_list(self):

        lines1 = open(path_to_seed_space_user_list, 'r').readlines()
        lines2 = open(path_to_additional_space_user_list, 'r').readlines()
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

        #print (len(scientists))
        #print (len(public))

        return scientists, public


    def get_trust_links(self):

        lines = open(path_to_manual_labelled_file,'r').readlines()

        print (len(lines))

        scientists = self.get_scientist_and_public_list()[0]
        public = self.get_scientist_and_public_list()[1]

        trust_links = []

        for line in lines:

            spline = line.rstrip('\n').split(',')

            if spline[0].lower() in public:

                public_user = spline[0].lower()

                tweet_text = ' '+ spline[-1].lower() + ' '

                mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))

                for ml in mention_list:

                    if ml[1:].lower() in scientists:

                        scientist_user = ml[1:].lower()

                        trust_links.append([public_user, scientist_user,spline[1]])

        print ("Length of trust links: ",len(trust_links))

        trust_links_unique = []
        trust_links_pair = []

        for tl in trust_links:

            if tl not in trust_links_unique:
                trust_links_unique.append(tl)

        print("Length of trust links (unique): ", len(trust_links_unique))


        for tlu in trust_links_unique:

            if [tlu[0],tlu[1]] not in trust_links_pair:
                trust_links_pair.append([tlu[0],tlu[1]])

            else:
                print ("Contradicting pairs, both trust_yes and trust_no present, exiting...")
                print (tlu)
                sys.exit()

        print ("Length of trust links (unique): ",len(trust_links_unique))

        trust_yes = []
        trust_no = []

        for tl in trust_links_unique:

            if tl[2] == 'trust_yes':
                trust_yes.append(tl)

            elif tl[2] == 'trust_no':
                trust_no.append(tl)

            else:
                print("error")
                print(tl)

        print("Length of trust_yes: ", len(trust_yes))
        print("Length of trust_no: ", len(trust_no))

        f = open(path_to_store_trust_links_unique,'w')

        for tlu in trust_links_unique:
            f.write(','.join(tlu)+'\n')

        f.close()


    def get_public_nodes(self):

        ##################
        # get the public nodes in trust links unique file in order to get their profile
        ##################

        lines = open(path_to_store_trust_links_unique,'r').readlines()

        public = self.get_scientist_and_public_list()[1]

        public_nodes = []

        for line in lines:

            spline = line.rstrip('\n').split(',')

            if spline[0] not in public_nodes:

                public_nodes.append(spline[0])

        print ("Length of public nodes: ",len(public_nodes))

        f = open(path_to_store_public_nodes_in_trust_links,'w')

        for pn in public_nodes:
            f.write(pn+'\n')

        f.close()




###################
# variables
###################

#-----------------
# by mentions and following

#path_to_all_mentions_file = 'test.txt'
# path_to_all_mentions_file = '../output/network/edges/edges_ALL_mentions.csv'
# path_to_following_list_folder = '../output/network/following/following_list_'
#
# path_to_store_unique_mentions = '../output/network/edges/edges_mentions_unique.csv'
# path_to_store_combined_following_list = '../output/network/following/following_ALL.csv'
# path_to_store_trust_links_file = '../output/trust_links/trust_links_space.csv'
# path_to_store_trust_links_strict_folder = '../output/trust_links/strict/trust_links_space_strict_'
# path_to_store_trust_links_strict = '../output/trust_links/trust_links_space_strict.csv'

#-----------------
# by trust dictionary

# path_to_liwc_public_mention_scientist_file = '../output/liwc/liwc_swear_words_public_@scientist.txt'
# path_to_liwc_scientist_mention_public_file = '../output/liwc/liwc_swear_words_scientist_@public.txt'
# path_to_seed_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
# path_to_additional_space_user_list = '../user_lists/1_18sep-18oct/user_space_additional.csv'
# path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'
# path_to_public_mention_scientist_tweets = '../tweets/mentions/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist_filtered.csv'
# path_to_scientist_mention_public_tweets = '../tweets/mentions/scientist_mention_public/1_18sep-18oct/scientist_@public.csv'
#
# path_to_trust_dictionary = '../trust_dictionary/trust_words.csv'
# path_to_distrust_dictionary = '../trust_dictionary/mistrust_words.csv'
#
# path_to_store_trust_links_all_with_tweets = '../output/trust_links/by_trust_dictionary/trust_links_with_tweets.csv'
# path_to_store_trust_links_unique = '../output/trust_links/by_trust_dictionary/trust_links_space.csv'
# path_to_store_trust_links_unique_strict = '../output/trust_links/by_trust_dictionary/strict/trust_links_space.csv'

#------------------
# by manual labelling

path_to_seed_space_user_list = '/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv'
path_to_additional_space_user_list = '../user_lists/1_18sep-18oct/user_space_additional.csv'
path_to_filtered_nodes = '../output/network/nodes/1_18sep-18oct/nodes_filtered.csv'
path_to_manual_labelled_file = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_tweets_new.csv'

path_to_store_trust_links_unique = '../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space_new.csv'
path_to_store_public_nodes_in_trust_links = '../output/network/nodes/1_18sep-18oct/nodes_trust_links_public.csv'

if __name__ == '__main__':

    #######################
    # 1. Get Trust Links by Mentions and Following edges
    #######################

    #mf = GetTrustLinksByMentionsFollowing()

    #mf.get_unique_mentions()

    #mf.divide_unique_mentions()

    #mf.combine_following_files()

    #-----------------
    # get trust links
    #-----------------

    #mf.get_trust_links()

    #-----------------
    # combine trust links strict files
    #-----------------

    #mf.combine_trust_links_strict_files()

    #-----------------
    # get trust links with stricter conditions
    #-----------------

    # threads = 20
    #
    # jobs = []
    #
    # for n in range(1, threads + 1):
    #
    #     gettrustlinks = multiprocessing.Process(name='gettrustlinks_' + str(n), target=mf.get_trust_links_strict, args=(n,))
    #     jobs.append(gettrustlinks)
    #
    # for j in jobs:
    #     print(j)
    #     j.start()


    #######################
    # 2. Get Trust Links by Trust Dictionary
    #######################

    #td = GetTrustLinksByTrustDictionary()

    #td.get_scientist_and_public_list()

    #td.get_trust_links_liwc()

    #td.get_trust_links_dictionary()

    #td.get_trust_links_combined()

    #td.get_trust_links_combined_strict()


    #######################
    # 3. Get Trust Links by Manual Labelling
    #######################

    ml = GetTrustLinksByManualLabelling()

    ml.get_trust_links()

    #ml.get_public_nodes()


