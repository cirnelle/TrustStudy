
################
# test remove completed users from user list
################

# def divide_node_list():
#
#     lines = open('../output/network/nodes_extracted.csv','r').readlines()
#
#     users_all = []
#
#     for line in lines:
#
#         spline = line.rstrip('\n')
#         users_all.append(spline)
#
#     #print (len(users_all))
#
#     n = int(len(users_all)/20) + 1
#     #print (n)
#
#     users_div_list = [users_all[i:i + n] for i in range(0, len(users_all), n)]
#
#     #print (len(users_div_list[-1]))
#
#     return users_div_list
#
# def get_following_multi(i):
#
#     users = divide_node_list()[i-1]
#
#     print (len(users))
#     #print (users)
#
#     # ------------------
#     # remove completed users from list
#
#     lines = open('../output/network/following/space_following_'+str(i)+'.csv','r').readlines()
#
#     users_completed = []
#
#     for line in lines:
#         spline = line.rstrip('\n').split(',')
#
#         if spline[0] == '0':
#             users_completed.append(spline[1])
#
#     print (len(users_completed))
#     #print (users_completed)
#
#     for uc in users_completed:
#
#         if uc in users:
#             users.remove(uc)
#
#     print (len(users))
#     #print (users)
#
# get_following_multi(1)

##################
# check for duplicates in following files
#################
#
# path_to_following_file = '../output/network/following/space_following_'
#
# for n in range(1,21):
#
#     print (n)
#
#     lines = open(path_to_following_file+str(n)+'.csv','r').readlines()
#
#     users = []
#
#     for line in lines:
#
#         spline = line.rstrip('\n').split(',')
#
#         if spline[0] == '0':
#
#             if spline[1] not in users:
#
#                 users.append(spline[1])
#
#             else:
#
#                 print (n)
#                 print (spline[1])


##################
# filter scientist @public tweets to keep only filtered nodes
##################

# import re
# import sys
#
# lines1 = open('/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv', 'r').readlines()
# lines2 = open('../output/network/nodes/nodes_filtered.csv', 'r').readlines()
#
# scientists_all = []
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#     scientists_all.append(spline[0].lower())
#
# # print (len(scientists))
#
# public = []
# scientists = []
#
# for line in lines2:
#     spline = line.rstrip('\n')
#
#     if spline.lower() not in scientists_all:
#         public.append('@'+spline.lower())
#
#     elif spline.lower() in scientists_all:
#         scientists.append(spline.lower())
#
#
# lines = open('../tweets/mentions/scientist_mention_public/DEPRECATED_scientist_@public.csv','r').readlines()
#
# print ("Length of ori tweet: "+str(len(lines)))
#
# tweets = []
#
# for line in lines:
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0].lower() in scientists:
#         tweets.append(spline)
#
# print ("Lengh of tweets after filtering scientist: "+str(len(tweets)))
#
# id_list = []
#
# final_tweets = []
#
# for t in tweets:
#
#     tweet_text = ' ' + t[-1].lower() + ' '
#
#     mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))
#
#     for ml in mention_list:
#         if ml in public:
#             if t[2] not in id_list:
#
#                 id_list.append(t[2])
#                 final_tweets.append(t)
#
#
# print ("Length of tweets after filtering public: "+str(len(final_tweets)))
#
# f = open('../tweets/mentions/scientist_mention_public/scientist_@public.csv','w')
#
# for ft in final_tweets:
#     f.write(','.join(ft)+'\n')
#
# f.close()


############
# test
############
#
# following_dict = {'u1':[[1,'s1'],[2,'u2']], 'u2':[[1,'s2'],[2,'u1']]}
#
# foll_list_final = []
#
# for key, value in following_dict.items():
#
#     key_list = []
#     value_list = []
#
#     key_list.append(key)
#
#     for v in value:
#         value_list.extend(v)
#
#     foll_list = key_list + value_list
#     foll_list_final.append(foll_list)
#
#
# print (foll_list_final)

#################
# test multithreading to get foll list
#################
#
# import multiprocessing
# from collections import defaultdict
# import sys
#
# class GetFollowing():
#
#     def divide_followings(self,n):
#
#         followings = []
#
#         lines = open('../output/network/following/space_following_' + str(n) + '.csv', 'r').readlines()
#
#         for line in lines:
#             spline = line.rstrip('\n').split(',')
#             followings.append(spline)
#
#         return followings
#
#
#     def create_following_list(self,n):
#
#         followings = self.divide_followings(n)
#
#         scientists = ['nasa','neiltyson']
#         public = ['skype','twitter','wickedkender']
#
#         following_list = []
#
#         for f in followings:
#
#             user = []
#
#             user.append(f[1].lower())
#
#             if f[0] == '0':
#                 following_list.append(['0', f[1].lower()])
#
#             if f[0] == '1':
#
#                 if f[1].lower() in scientists:
#                     scientist_followed = list(set(user).intersection(scientists))
#                     following_list.append(['1', scientist_followed[0]])
#
#                 if f[1].lower() in public:
#                     public_followed = list(set(user).intersection(public))
#                     following_list.append(['2', public_followed[0]])
#
#         following_dict = {}
#
#         flag = True  # the flag is needed to check if it is the first line of the file
#
#         for index, fl in enumerate(following_list):
#
#             if fl[0] == '0' and flag == True:  # first line of the file
#                 key = fl[1]
#                 foll_list = []
#                 flag = False
#                 continue
#
#             if fl[0] == '0' and flag == False:
#                 following_dict[key] = foll_list
#                 key = fl[1]
#                 foll_list = []
#                 continue
#
#             if fl[0] == '1' or fl[0] == '2':
#                 if index != len(following_list) - 1:
#                     foll_list.append(fl)
#
#                 if index == len(following_list) - 1:  # check if it is the last line in the file
#                     foll_list.append(fl)
#                     following_dict[key] = foll_list
#
#         # print (following_dict)
#
#         # create list with users and the public and scientist users they follow
#
#         foll_list_final = []
#
#         for key, value in following_dict.items():
#
#             key_list = []
#             value_list = []
#
#             key_list.append(key)
#
#             if value != []:
#
#                 for v in value:
#                     value_list.extend(v)
#
#                 foll_list = key_list + value_list
#                 foll_list_final.append(foll_list)
#
#         # write to file
#
#         f = open('../output/network/following/test_following_list_'+str(n)+'.csv', 'w')
#
#         for fl in foll_list_final:
#             f.write(','.join(fl) + '\n')
#
#         f.close()
#
#     def calling_function(self):
#
#         threads = 3
#
#         jobs = []
#
#         for n in range(1, threads + 1):
#             print(n)
#
#             getreplies = multiprocessing.Process(name='getfollowing_' + str(n), target=self.create_following_list, args=(n,))
#             jobs.append(getreplies)
#
#         for j in jobs:
#             print(j)
#             j.start()
#
#
#
#     def get_foll_dict(self):
#
#         following_dict = {}
#
#         for n in range(1,4):
#             lines = open('../output/network/following/test_following_list_'+str(n)+'.csv','r').readlines()
#
#             for line in lines:
#                 spline = line.rstrip('\n').split(',')
#
#                 key = spline[0]
#                 value = []
#
#                 for n in range(1,len(spline)-1,2):
#                     value.append([spline[n],spline[n+1]])
#
#                 following_dict[key] = (value)
#
#
#         print (following_dict)
#
#
#
# if __name__ == '__main__':
#
#     gf = GetFollowing()
#
#     #gf.calling_function()
#
#     gf.get_foll_dict()

################
# find missing pairs in triad file (compared to trust link file)
################

# lines1 = open('../output/trust_links/trust_links_space_strict.csv','r').readlines()
# lines2 = open('../output/network/triad/triad_space_strict.csv','r').readlines()
#
# triads = []
#
# for line in lines2:
#     spline = line.rstrip('\n').split(',')
#     triads.append([spline[0],spline[1]])
#
# print (len(triads))
#
# trust_links = []
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#     trust_links.append([spline[0],spline[1]])
#
# print (len(trust_links))
#
# not_in_trust_links = []
# temp = []
#
# for tl in trust_links:
#
#     if tl not in temp:
#         temp.append(tl)
#
#     else:
#         print (tl)


#####################
# compare two node list and filter out unique ones
#####################

# lines1 = open('test_2.csv','r').readlines()
# lines2 = open('../output/network/nodes/3_18nov-18dec/nodes_with_following.csv','r').readlines()
#
# nodes = []
#
# for line in lines1:
#     spline = line.rstrip('\n')
#     nodes.append(spline.lower())
#
# print (len(nodes))
#
# unique = []
# nodes_1 = []
#
# for line in lines2:
#     spline = line.rstrip('\n')
#
#     if spline not in nodes_1:
#         nodes_1.append(spline)
#
#     else:
#         print (spline)
#
#     if spline.lower() not in nodes:
#         unique.append(spline.lower())
#
# print (len(nodes_1))
# print (len(unique))
# print (unique)

###################
# test code to extract sublist from list
###################

# import sys
#
# l1 = ['a','b','c','d','e']
# l2 = ['a','c','b']
#
# l3 = []
#
# for index,l in enumerate(l1):
#
#     for m in l2:
#         if m == l:
#             l3.append([index,m])
#
# print (l3)
#
# max_element = max(l3, key = lambda x:x[0])
# max_index = max_element[0]
#
# print (max_index)
#
#
# sublist = l1[max_index+1:]
# print (sublist)

# ff = [[0, 'a'], [1, 'b'], [2, 'c']]
#
# zz=max([x[0] for x in ff])
#
# print (zz)

###############
# extract columns from csv file
###############

# lines = open('../tweets/mentions/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist_filtered.csv','r').readlines()
#
# tweets = []
#
# for line in lines:
#     spline = line.rstrip('\n').split(',')
#     tweets.append([spline[0],spline[-1]])
#
# print (len(tweets))
#
# f = open('../output/trust_links/by_manual_labelling/trust_links_manual.txt','w')
#
# for t in tweets:
#     f.write(','.join(t)+'\n')
#
# f.close()

#################
# REAL p@s: check for tweets in public_@scientist file that are actual p@s where scientist is from the additional scientist list
#################

# import re
# import sys
#
# lines1 = open('../tweets/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist.csv','r').readlines()
# lines2 = open('../user_lists/1_18sep-18oct/user_space_additional.csv','r').readlines()
# lines3 = open('../output/network/nodes/1_18sep-18oct/nodes_filtered.csv','r').readlines()
# lines4 = open('/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv','r').readlines()
#
# scientist_add = []
#
# for line in lines2:
#     spline = line.rstrip('\n')
#     scientist_add.append(spline.lower())
#
# print (len(scientist_add))
#
# scientist_seed = []
#
# for line in lines4:
#     spline = line.rstrip('\n').split(',')
#     scientist_seed.append(spline[0].lower())
#
# print (len(scientist_seed))
#
# scientist_all = scientist_add + scientist_seed
#
# public = []
#
# for line in lines3:
#     spline = line.rstrip('\n')
#
#     if spline.lower() not in scientist_all:
#         public.append(spline.lower())
#
# print (len(public))
#
# tweets = []
#
# for line in lines1:
#
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0].lower() in public:
#
#         tweet_text = ' ' + spline[-1].lower() + ' '
#
#         mention_list = (re.findall(r'(?:\@)\S+', tweet_text, re.I))
#
#         for ml in mention_list:
#
#             if ml[1:].lower() in scientist_add:
#
#                 tweets.append(spline)
#
# print (len(tweets))
# print (tweets[:10])


###############
# get tweets that are really tweeted by the public
###############


#
# import re
# import sys
#
# lines1 = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_ylh.txt','r').readlines()
# lines2 = open('../user_lists/1_18sep-18oct/user_space_additional.csv','r').readlines()
# lines3 = open('../output/network/nodes/1_18sep-18oct/nodes_filtered.csv','r').readlines()
# lines4 = open('/Users/yi-linghwong/GitHub/TwitterML/user_list/user_space_combine.csv','r').readlines()
#
# scientist_add = []
#
# for line in lines2:
#     spline = line.rstrip('\n')
#     scientist_add.append(spline.lower())
#
# print (len(scientist_add))
#
# scientist_seed = []
#
# for line in lines4:
#     spline = line.rstrip('\n').split(',')
#     scientist_seed.append(spline[0].lower())
#
# print (len(scientist_seed))
#
# scientist_all = scientist_add + scientist_seed
#
# public = []
#
# for line in lines3:
#     spline = line.rstrip('\n')
#
#     if spline.lower() not in scientist_all:
#         public.append(spline.lower())
#
# print (len(public))
#
# tweets = []
#
# print (len(lines1))
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0].lower() in public:
#         tweets.append(spline)
#
# print (len(tweets))
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_ylh_1.txt','w')
#
# for t in tweets:
#     f.write(','.join(t)+'\n')
#
# f.close()


##################
# get additional tweets to be labelled as trust links gold standard tweets
##################

# lines1 = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_with_tweets.txt','r').readlines()
# lines2 = open('../tweets/public_mention_scientist_extracted/1_18sep-18oct/public_@scientist_filtered.csv','r').readlines()
#
# tweets_1 = []
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#     tweets_1.append(spline[-1].lower())
#
# print (len(tweets_1))
#
# tweets_2 = []
#
# for line in lines2:
#     spline = line.rstrip('\n').split(',')
#     tweets_2.append([spline[0].lower(),spline[-1].lower()])
#
# print (len(tweets_2))
#
# tweets = []
#
# for t in tweets_2:
#     if t[-1] not in tweets_1:
#         tweets.append(t)
#
# print (len(tweets))
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_temp_4.txt','w')
#
# for t in tweets:
#     f.write(','.join(t)+'\n')
#
# f.close()

##################
# insert 'trust_yes' into trust links file
##################

# lines1 = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_tweets_no.csv','r').readlines()
#
# tweets = []
#
# print (len(lines1))
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#
#
#     if len(spline) != 2:
#         print (spline)
#
#     else:
#
#         tweets.append([spline[0],'trust_no',spline[-1]])
#
# print (len(tweets))
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_tweets_no_1.csv','w')
#
# for t in tweets:
#     f.write(','.join(t)+'\n')
#
# f.close()

#################
# get number of unique public nodes per file (to double check)
#################

# lines = open('../output/timeline_tweets/1_18sep-18oct/timeline_tweets_13.csv','r').readlines()
#
# nodes = []
#
# for line in lines:
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0] not in nodes:
#         nodes.append(spline[0])
#
# print (len(nodes))

#################
# get source tweet file for trust links, filter out existing nodes
#################

# lines1 = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/_source_tweets.txt','r').readlines()
# lines2 = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_space.csv','r').readlines()
#
# nodes_exist = []
#
# for line in lines2:
#     spline = line.rstrip('\n').split(',')
#     nodes_exist.append(spline[0])
#
# print (len(nodes_exist))
#
# tweets = []
# text_only = []
#
# print (len(lines1))
#
# for line in lines1:
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0].lower() not in nodes_exist:
#         tweets.append(spline)
#         text_only.append(spline[1])
#
# print (len(tweets))
#
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/_source_tweets.txt', 'w')
#
# for t in tweets:
#     f.write(','.join(t) + '\n')
#
# f.close()
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/_source_tweets_for_sentistrength.txt','w')
#
# for t in text_only:
#     f.write(t+'\n')
#
# f.close()

#####################
# get additional public nodes for trust links (new)
#####################

# lines = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/trust_links_tweets_new.csv','r').readlines()
#
# nodes = []
#
# for line in lines:
#
#     spline = line.rstrip('\n').split(',')
#
#     if spline[0] not in nodes:
#
#         nodes.append(spline[0])
#
# print (len(nodes))
#
# f = open('../output/trust_links/by_manual_labelling/1_18sep-18oct/nodes_new.csv','w')
#
# for n in nodes:
#     f.write(n+'\n')
#
# f.close()

######################
# testing with keyword in timeline
######################

nodes_and_keyword_count = [['elliedvs', '1'], ['ffsgeorge', '2'], ['inthemane', '1'], ['deadlylallana', '0'], ['elliedvs', '0'], ['iamphilipjoyce', '2'], ['zagary_mejia', '0'], ['kingakalecinska', '0'], ['katiemckenzieee', '4'], ['real_bratton', '0'], ['aimee_weir14', '0'], ['carahsassidy', '0'], ['camrynnoellee', '1'], ['franciscojayda', '0'], ['imnicolleochoa', '0'], ['lexitoootle', '2'], ['_jessiiiesmith', '3'], ['savannahbeadenk', '0'], ['tompaymaloryles', '0'], ['bfswproductions', '0'], ['vokkedup', '0'], ['becca_frend', '2'], ['pater429', '0'], ['danferher', '0'], ['bigdawgdavies', '3'], ['kaylawaterss', '0'], ['paigey_espe', '1'], ['_alyhernandez', '0'], ['jesselias05', '0'], ['kaleciaf', '0'], ['sloanealexander', '1'], ['aleks_burkus', '0'], ['groovyat', '1'], ['catherine_ava', '1'], ['eimearwinterss', '0'], ['sheepman_xd', '1'], ['chinesesmile105', '1'], ['johnthegypsy', '2'], ['skubusteve', '4'], ['ayekatyy', '10'], ['centristnet', '3'], ['rosieislameee', '2'], ['jameson_guidry', '2'], ['cammstride', '3'], ['ursiclapp', '3'], ['bobbygergus', '0'], ['xsunnyolivia', '1'], ['phoebe_curtis1', '2'], ['phillytheboss', '1'], ['boho1899', '0'], ['tr1n4b34n', '0'], ['eeekks', '4'], ['kalish_man', '4'], ['dskisoccer17', '1'], ['aoife_doherty1', '0'], ['officialmarklaw', '0'], ['doctorchipotle', '1'], ['mr_ityc', '1'], ['_samhepworth', '5'], ['attackonbriana', '2'], ['jesiliczner', '19'], ['_matthewcooper_', '1'], ['endo_chank', '6'], ['maisaakhn', '0'], ['tripdeuceuno', '0'], ['johncashtro', '6'], ['fvckedyourhoe', '1'], ['blonde_sun_doll', '0'], ['__alegra_', '4'], ['michellerds_', '1'], ['jessylang10', '0'], ['talktothaliah', '0'], ['emily__eddy', '2'], ['holyhojbjerg', '2'], ['annajkozak', '2'], ['savvyridenour', '1'], ['boywonerelroy1', '0'], ['muddyvegas_', '1'], ['sarahsokay', '1'], ['saintified_', '0'], ['mckailie', '0'], ['morganavickery', '4'], ['only__yess', '0'], ['waynecheong', '16'], ['currentnews_en', '35'], ['worldnewsj', '21'], ['jolandagreve', '14'], ['avary_gunsallus', '0'], ['kiii555', '1'], ['tauva101', '4'], ['putaceloso', '0'], ['yeahimatree', '0'], ['katieeemaeee__', '1'], ['roarkfineart', '1'], ['isaacmarron', '5'], ['borjardriguez', '1'], ['robbiereckd', '1'], ['alexandra_7', '3'], ['latvianvideoslv', '0'], ['shimmermcpe', '0'], ['uncalming', '3'], ['anas_is_in', '2'], ['mahnxr', '3'], ['itschrispine', '0'], ['davidplatten', '3'], ['sararamirez', '6'], ['tobinmd1964', '1'], ['idolisedun', '0'], ['zuluagamariana1', '1'], ['ritsybits', '0'], ['b2daitch', '2'], ['amidignan', '8'], ['samrobinson97', '0'], ['beckyhxmmo', '0'], ['cody_gary', '1'], ['kid604', '80'], ['kevyngessner', '3'], ['princessduck', '2'], ['heathhamb', '1'], ['fr33_w0rld', '1'], ['keaganmilitante', '18'], ['emmav_og', '7'], ['wetigersss', '0'], ['mollykthomas', '6'], ['richardtdevane2', '4'], ['thunderyoyster', '2'], ['zoeeefish', '1'], ['darkpreacher99', '1'], ['diordadd', '0'], ['twatterfull', '27'], ['mae_oxo', '0'], ['_sarahreeves', '0'], ['ambiibambi24', '2'], ['503carlo', '0'], ['rileyhogue', '1'], ['rosebrown1616', '0'], ['tizzivee', '6'], ['shelbseliz', '0'], ['mcgeezyfbaby', '2'], ['angiep1994', '3'], ['tippotate', '4'], ['ramsettpark', '2'], ['kaddess_', '1'], ['ashlynhojsak', '1'], ['nettanini', '1'], ['gimmiethestick', '24'], ['jessicanatiel', '0'], ['sammruger', '0'], ['rissriss__', '1'], ['calibitcoin', '2'], ['oceaniaknows', '0'], ['thatspacelava', '1'], ['tanja_girl', '0'], ['sumthingmessy', '0'], ['ultijaebum', '2'], ['carolynmcfish1', '8'], ['adhdengineer', '0'], ['abbaadamufan', '8'], ['l0ttyy', '2'], ['grace_rhiannon', '1'], ['goin5hole', '9'], ['nancycollister1', '2'], ['astrobotslut', '46'], ['davetonner', '0'], ['jonny_chaos', '10'], ['heatherwassing', '4'], ['rupertmissickjr', '2778'], ['jpetme', '0'], ['marriottlibrary', '13'], ['christophergfx', '3'], ['chloemageex', '1'], ['mode23', '8'], ['jooordanstevens', '1'], ['joydrizzy', '1'], ['unchxrmed', '1'], ['grt8ness2017', '4'], ['paupausaints', '0'], ['3carryonitems', '10'], ['sarahxsmo', '3'], ['leaving_notice', '2'], ['the__bear__jew', '0'], ['destrhope', '0'], ['jay_fezz', '6'], ['marshalljm', '2'], ['korillz', '0'], ['manuki16', '11'], ['trophysws', '0'], ['queenscorpion9', '0'], ['mariah_lee98', '0'], ['silviamelange', '0'], ['yaneri11', '4'], ['bookkworm', '11'], ['emilytimmsss', '1'], ['shylasarabando', '1'], ['sarahetsy', '0'], ['matterssomehow', '14'], ['aliasbluebird', '0'], ['fiyaakiyaa', '2'], ['mrjamesnoble', '26'], ['snake354', '0'], ['majesticwizardy', '0'], ['mykingtetsu', '0'], ['alhimself', '19'], ['hunt_chance', '2'], ['ellie_robs13', '4'], ['stevesveale', '1'], ['ricardoortiz50', '4'], ['buddrud', '2'], ['k_luhhhx', '0'], ['ivhunsinger', '0'], ['hippiebookkeep', '2'], ['stevesgoddard', '61'], ['joshwillgray', '0'], ['lizdotfern', '7'], ['brendandegnan', '2'], ['georgewalterxx', '0'], ['andrewmyrvold', '0'], ['ameliaaakayy', '1'], ['adiehowarthh', '1'], ['shansdoe', '0'], ['helene0709', '0'], ['hlawless_x', '0'], ['stephiegilley', '2'], ['keira_scahill', '0'], ['riezaapr', '9'], ['tconspiracyguys', '4'], ['rexriot215', '19'], ['thefatgirlslife', '0'], ['emocirclejerk', '7'], ['manzanitafire', '20'], ['dadamthegreat', '3'], ['jennieknapper', '0'], ['lawr_and_syl', '0'], ['codyjayp', '0'], ['heathenasu', '0'], ['tywahu', '1'], ['morgancummmins', '1'], ['e_dyc', '1'], ['babyidiotjerk', '7'], ['temporarypony', '0'], ['novarff', '5'], ['skinnypimp_', '1'], ['guiltyjoseph', '1'], ['kaitlinbruce23', '0'], ['freyugh', '3'], ['danaelizabeth69', '0'], ['alexxx_0817', '1'], ['diventareadesso', '14'], ['peggyschxyler', '2'], ['brookemcgarvin', '8'], ['_charlottee_s', '0'], ['uranussideways', '1'], ['fulmetaltiger57', '2'], ['mbsevans', '0'], ['rimmediou', '3'], ['margofaulkner', '14'], ['frazzledjazz', '1'], ['savageprinc3ss', '2'], ['dammndolan', '6'], ['sara_hammonds', '2'], ['wentzofficial', '2'], ['in4ab8tin', '0'], ['_xogoddess_', '2'], ['nataliemfarias', '0'], ['headass_tx', '0'], ['bouquetofskulls', '3'], ['mgliksmanmdphd', '33'], ['spacekid51', '0'], ['wtfjessielynn', '2'], ['emilliaa', '2'], ['seidyxm', '0'], ['laurennschh', '2'], ['emmaboppidybop', '0'], ['c_anthony191', '0'], ['abigailhartxo', '2'], ['givingtree223', '1'], ['freefallfx', '1'], ['alexcorp_', '6'], ['starzara3', '0'], ['shizayaz', '0'], ['yungwjll', '0'], ['pajtasg', '2'], ['socali_km', '0'], ['cheyenne_nale', '0'], ['idioticmidget', '0'], ['comicsdougout', '0'], ['mercuraz', '2'], ['grahamt11', '2'], ['kingtomlnson', '0'], ['fayebuckley9', '2'], ['dinoplop', '2'], ['alexjrhodes', '4'], ['claudiafabeni', '6'], ['yellowfinesse', '3'], ['rowan_frey', '0'], ['leah_ferg12', '2'], ['_derping_irwin_', '0'], ['siighko', '3'], ['kas_1979', '4'], ['arisaarelainen', '13'], ['joshcldr', '1'], ['willowfthes', '0'], ['russplfc', '2'], ['forevansakes', '0'], ['nenanextdoor', '0'], ['santiagoalba_', '2'], ['ikelliegold', '0'], ['ccharliebee', '1'], ['cinnamonbyte', '0'], ['effinglibrarian', '22'], ['jonnniiirenee', '0'], ['alexisfaltz', '0'], ['pabloncej', '6'], ['markese_j', '1'], ['jacobvalencia21', '0'], ['clairepees_', '0'], ['williamlads', '5'], ['triwzard', '2'], ['waluigidabest', '1'], ['babybob2121', '2'], ['dereksweetwater', '1'], ['adrienbenson', '4'], ['mtppocahotass', '5'], ['yolousup', '0'], ['nelldollbell', '1'], ['name47z', '0'], ['spookyrituals', '2'], ['inbredhybrid', '0'], ['juststaninhope', '1'], ['sleepythejoker', '1'], ['keishwer', '1'], ['aaronflynn96', '2'], ['pablodiablo94', '1'], ['jacobthomas3_', '0'], ['misselliegray', '1'], ['loopjohnb', '2'], ['thereehlthing', '0'], ['whoisnickchaff', '1'], ['airellababyy', '5'], ['stonyindacut', '1'], ['nicksearlegeo8', '5'], ['_money19', '0'], ['jaaaafeel', '4'], ['thotheancient', '1'], ['trulyxbeauty', '1'], ['n8than5', '0'], ['_alexandra666', '2'], ['ohsnapitzarlene', '0'], ['merchew', '0'], ['juicyjaceyy', '2'], ['camillealthen', '0'], ['ufo_slut', '0'], ['fresh_615', '1'], ['nataliekate33', '2'], ['thereal2red', '4'], ['itscurtmcgurt', '1'], ['omixey', '0'], ['ry_best', '0'], ['dizzeeclizzy', '0'], ['eyeopen81359400', '0'], ['delanee_skye', '0'], ['thevictorianyc', '0'], ['macepts', '0'], ['teeeemz', '0'], ['queenn', '0'], ['triidant', '0'], ['gardenofganja', '1'], ['bzoda15', '1'], ['austinsizzles', '1'], ['sinners966', '27'], ['hsmitty3', '0'], ['heavymimilover', '1'], ['tevgvn', '4'], ['lightbrand33', '1'], ['indyg8s', '0'], ['nicoleej0hnson', '7'], ['toraxsmpl', '1'], ['g_eorg_i', '1'], ['tarakiyee', '10'], ['jordan_jjj', '0'], ['justmejustina', '1'], ['oliviapiro', '9'], ['realdavidshelly', '1'], ['kybunks', '4'], ['icosmos10', '1'], ['maddierach', '9'], ['cam_abhab', '3'], ['jaymoreee', '2'], ['mas0nnnn', '2'], ['ozcastillo31', '1'], ['ehrenkassam', '2'], ['akadarkskinpapi', '0'], ['trashstiel', '1'], ['marioc7_', '0'], ['johnnysenpapi', '1'], ['kids_again', '0'], ['vleon16', '1'], ['hnkthln', '4'], ['universe_joey', '4'], ['wallbreaker1818', '0'], ['astralnautbsamp', '1'], ['serenitycortez_', '0'], ['brian_flack', '1'], ['calvincooly', '0'], ['trenationnn', '1'], ['tchav17', '0'], ['thenamebeaugie', '0'], ['smuttydolan', '0'], ['insane_wallace', '1'], ['zakcircuits', '3'], ['nancyyttran', '4'], ['kenzie2289', '0'], ['jdiamondisme', '4'], ['harkynkunmy', '0'], ['trevormoran', '2'], ['sburns0406', '0'], ['oralwithricky', '0'], ['tylerr2rs', '3'], ['boobearcaylen', '5'], ['tylerscactuss', '1'], ['mango_gab', '0'], ['shinyyjacks', '0'], ['alexandrapetlov', '1'], ['moran_slayer', '0'], ['lalawlorff', '0'], ['mxlory', '1'], ['jblover12223', '0'], ['gregermeisterrr', '0'], ['mintsivan', '1'], ['natalybtw', '1'], ['caitiemary02', '1'], ['belovedgraceffa', '0'], ['sleepykitty_', '0'], ['harleiarenn', '5'], ['savagedarkskin7', '0'], ['slyshotty', '0'], ['_sarahfay_', '0'], ['pfleming13', '0'], ['bri_jolie', '2'], ['themoderncage', '1'], ['francklegunner', '1'], ['bogchon', '3'], ['perrinbrunet', '5'], ['k_wright6', '2'], ['evelyn_evans21', '0'], ['readandjeep', '4'], ['rvrb_', '0'], ['derp696', '3'], ['luke_hemmburger', '2'], ['sequoiasss', '0'], ['greedygray', '1'], ['caitlynsmith24', '1'], ['chelsiewithac', '0'], ['100s_of_fandoms', '0'], ['oreaux_', '4'], ['hallie_page', '0'], ['niceguy504', '11'], ['cubillo_', '0'], ['jessegilbert', '1'], ['rosslyndmc', '0'], ['mintchmla', '1'], ['labhaoiselesiog', '1'], ['yungsquidkid', '1'], ['bentley_holley', '0'], ['br00kearnold', '0'], ['carringtoncash', '2'], ['alexischewy', '5'], ['try_and_guess', '0'], ['dakotaswan7', '1'], ['lifesamitch97', '1'], ['angeloboggiox', '1'], ['radcouch', '0'], ['brooklyn_bug', '4'], ['apexidee', '0'], ['dollasforpoetry', '3'], ['giselle_nieblas', '1'], ['cameronng24', '3'], ['angelmastr', '0'], ['maxontweet', '9'], ['tluckeroth', '3'], ['heally_', '1'], ['thisisbrookeb', '3'], ['catandthemoon92', '0'], ['oddunicornio04', '0'], ['kazadilla', '0'], ['theorangeorphan', '2'], ['nina_aversa', '1'], ['c_o_t_u_e', '10'], ['ohhh_neptune', '0'], ['lrfbaratz', '0'], ['messywriter_', '1'], ['iam_vanwild3r', '0'], ['gigi_3723', '0'], ['falsebaidwin', '1'], ['biancaaddison', '0'], ['juklinn', '6'], ['ace_is_dead', '0'], ['jj_pardini', '0'], ['sammydodgerocks', '8'], ['lordlin_', '2'], ['laughat_mylife', '0'], ['saintskeleton', '2'], ['shivermydear', '0'], ['chuckyoutwo', '0'], ['janisse_chris', '1'], ['raecanty', '1'], ['lizcudi', '1'], ['sonatinahaze', '5'], ['sunnyybunny', '10'], ['champthisguyls', '2'], ['rachel_steichen', '1'], ['antiezelle', '9'], ['reckless_renzo', '0'], ['rufiosonfire', '5'], ['simplesed', '4'], ['elihudsvn', '0'], ['einnxre', '5'], ['nemo42_za', '1'], ['banditsboy1130', '0'], ['madibetty', '1'], ['aestheticangel_', '0'], ['kawaikacti', '0'], ['sieeked', '0'], ['karkinpus13', '0'], ['marziemfer', '3'], ['imyourmanwhore', '0'], ['jtrochezzz2', '3'], ['wewantprenups', '1'], ['haleycurrie', '0'], ['tombutts', '24'], ['lindsdistefano', '1'], ['djsmoothnuts', '1'], ['mayanash17', '1'], ['_aubsnic', '0'], ['unklebing', '3'], ['daniellekrivex', '0'], ['arobertson28', '5'], ['messissav', '1'], ['morganlindaj', '2'], ['satiricalmuse', '3'], ['tulsipatel_', '0'], ['juliasmith1121', '1'], ['daiaigoat', '0'], ['mariahmcds7', '1'], ['ttlydolans', '0'], ['daujahboo1', '10'], ['blueavebabe', '0'], ['genereuse2015', '0'], ['teamsuper_nz', '0'], ['monkeymafia1668', '6'], ['onlinetyier', '1'], ['renad_a_a', '0'], ['cutetotheheart', '1'], ['weiryn', '2'], ['riverajaime', '0'], ['ohmycelestie', '0'], ['ynh___', '0'], ['tattoodillon', '1'], ['herbalyfe', '2'], ['haaaaileyyy', '1'], ['bocaniam', '0'], ['daslaz', '0'], ['uitjiminie', '5'], ['brenanasplit', '1'], ['jchavez_', '8'], ['nonchalantguy_', '0'], ['latino_lion52', '0'], ['crowbarpwr', '0'], ['willweil', '7'], ['graciosaaa_', '1'], ['zoerab1', '2'], ['moneymach_', '0'], ['pistol_p3ter', '0'], ['ruchifruitwala', '1'], ['__cocoooo', '7'], ['mephype93', '9'], ['cod2legendbeast', '0'], ['sinisterservant', '3'], ['joetheatheist', '6'], ['elisabethtooker', '1'], ['njhlads', '0'], ['lillyszquad', '1'], ['trappedinchaos', '0'], ['anum_bagel', '1'], ['dm_ra3', '0'], ['stonecold_jet', '0'], ['kevinbethune', '33'], ['iamkingwize', '11'], ['fuckuli', '1'], ['typical_but_odd', '0'], ['rosethorp', '0'], ['maryheston', '8'], ['darthkarennn', '0'], ['vobinraldez', '4'], ['haydenscroggins', '6'], ['gawbymoon', '4'], ['elrisitasforte', '0'], ['el_cristiano5', '3'], ['jr_4four', '0'], ['ruggrossorlando', '0'], ['the_codeine_kid', '3'], ['sheyleneh', '10'], ['p_dasher', '2'], ['mmboltz', '2'], ['ham_man13', '0'], ['cursingpolice', '13'], ['stolen_affinity', '0'], ['neboheightsmom', '0'], ['lloydlyndsay', '0'], ['adigamotv', '2'], ['itsnovap', '1'], ['micapughhhh_', '0'], ['jp_landolfi', '0'], ['_ianfrancis', '1'], ['itskingkumar', '0'], ['kashiakatelenn', '2'], ['harrykinga', '0'], ['katnisseverweed', '0'], ['high_life_joe', '4'], ['_aaaaaari', '5'], ['kveeezy', '0'], ['alivommaro', '0'], ['gazared305', '5'], ['jimmywanner', '0'], ['emily_malkowski', '1'], ['iamcarolinaking', '9'], ['elenaduong', '0'], ['_sknydanny', '0'], ['kuson_2_14', '0'], ['msdj72', '2'], ['broke_beautiful', '6'], ['radzz999', '0'], ['ultmarktuna', '0'], ['orianacrosales', '2'], ['janalfunstyyry', '0'], ['elkayy13', '1'], ['stephlovaaa_', '3'], ['drtydza', '0'], ['thelunarfather', '10'], ['compazavala', '0'], ['caiticam', '5'], ['richierich3rd', '1'], ['anaaep', '3'], ['articlemkultra', '0'], ['nm_c07', '2'], ['franzbeaponce', '0'], ['redmetcalfe', '0'], ['beccaarana', '0'], ['travelnlivelife', '0'], ['ctkennedy25', '0'], ['mel_kittykatt', '0'], ['boubounokefalos', '0'], ['geckorhombus', '0'], ['katechadwick5', '0'], ['superemmachan', '0'], ['notorioushjb', '0'], ['themarckoguy', '2'], ['belladestiny99', '1'], ['afr0jill', '0'], ['amber_ward_', '0'], ['freebyrd55', '0'], ['themostmitsos', '7'], ['blaiseceegee', '7'], ['imcoopershields', '2'], ['mrgnmcnl_', '1'], ['larkin10louise', '0'], ['turing_police', '4'], ['hamiltonbreakme', '0'], ['jonginng', '1'], ['ayesh_sk', '0'], ['oliviavavin', '5'], ['commanderxlexa', '1'], ['ohhnico_', '0'], ['thedylanparker', '4'], ['nadzran_hafiy13', '9'], ['jerrmeehan', '1'], ['ischern', '2'], ['riceboyrey', '1'], ['khephrithoth', '0'], ['evazquez8520', '0'], ['jessicamarzipan', '5'], ['melanin_made', '0'], ['ang_romano', '2'], ['tobiovevo', '0'], ['tim_radio', '0'], ['writerkarlaf', '1'], ['paigeshoe13', '2'], ['reneewebs', '34'], ['despanno', '4'], ['noriaz91', '2'], ['smenor', '6'], ['millafecke', '0'], ['madkbrew', '4'], ['_aroomba', '2'], ['kellylord1569', '0'], ['mcbrizzle_', '3'], ['pytbby', '0'], ['kry5t41', '1'], ['francessldb', '0'], ['annasather', '6'], ['theoooooooooo', '0'], ['katewetherlock', '8'], ['jessieeeeb_', '0'], ['tj_xm', '0'], ['martian_garden', '6'], ['wintxersoldier', '1'], ['d_teck', '4'], ['johnnypappas', '395'], ['k_kkadie_bugg', '1'], ['ninadubzzz', '2'], ['dylanacop', '2'], ['nickosjtm', '0'], ['pigeonpriest', '2'], ['ihatethemedia', '8'], ['jackh_official', '5'], ['handofbarnes', '1'], ['jragga', '2'], ['wayfarersprayer', '4'], ['baileyskinner1', '0'], ['norrrr_', '2'], ['okingkong1', '2'], ['youngjedifresh', '3'], ['thatbitchkonrad', '0'], ['samhenryjohnson', '3'], ['j_dragonkin', '2'], ['utah_getme_2', '4'], ['squints92', '4'], ['hailbuddha', '0'], ['jrbeardcrew', '5'], ['glowprincxss', '2'], ['pinoe77', '4'], ['moving20', '7'], ['kaptainkramer23', '2'], ['leblancstartup', '0'], ['brittanymacdon', '0'], ['dank_mit', '1'], ['br3annak', '0'], ['broadstreetbosh', '0'], ['laurenaharder', '1'], ['johnajaoude', '0'], ['skyla_rose_32', '1'], ['treelijahblvd', '0'], ['jaybeedubbau', '2'], ['armando22leosun', '0'], ['heysarahxox', '3'], ['haileyrade', '10'], ['mobydick1738', '2'], ['ibtehalhussein', '2'], ['myahtbh', '1'], ['carmennli', '3'], ['miss_euphoric88', '2'], ['charliepoet', '18'], ['9_scorp', '3'], ['aureajenelle', '0'], ['__dessxo', '0'], ['jakegunst', '17'], ['marie__cutie', '17'], ['cheyforbes', '2'], ['dmufc58', '15'], ['bruinsscience', '6'], ['jgarcein', '0'], ['not_coyotic', '13'], ['alyssa_kubiak', '0'], ['willoftheatheis', '0'], ['gaikwadvishalr', '0'], ['zelfthezolf', '0'], ['fuzepsd', '0'], ['cawwwtney', '0'], ['tivikareed', '1'], ['submarinorojo', '0'], ['erma_geddon', '2'], ['feddjord', '0'], ['spinnerbuckle', '0'], ['artgarfunkle', '0'], ['misterburk3', '1'], ['sparks30303', '3'], ['78d185fdc3bd4c1', '0'], ['gomhar', '6'], ['jamila_v', '39'], ['illus10nz', '0'], ['carolcotb', '0'], ['_kiebooms', '0'], ['keatonrey', '8'], ['raz_ma_tazzzz', '1'], ['embraceape', '32'], ['eloanmusk', '1'], ['coryrichards83', '0'], ['azerrah', '5'], ['bibicheret', '1'], ['cessnadriver172', '0'], ['chrisisnorml', '6'], ['quastar2011', '29'], ['sagesera', '3'], ['casxvii', '1'], ['uf0freak', '0'], ['bga19h', '7'], ['arielofficial', '2'], ['mischiefmags', '7'], ['almaasoglu', '3'], ['laurrmoran', '1'], ['blurukus', '2'], ['jadalynp', '0'], ['macksboo', '0'], ['sequoiathetree', '1'], ['blondecrkhead', '6'], ['itsdisko', '1'], ['kayenne22', '2'], ['texas_kayak', '0'], ['nondairygary', '0'], ['camjam_andjelly', '0'], ['msmollybnorth', '2'], ['lent_ava', '0'], ['temperance206', '1'], ['fandomsandhoran', '0'], ['garrywhoever', '4'], ['old_ag_91', '1'], ['nikollets', '3'], ['_david_harden_', '4'], ['majorluzer', '0'], ['brookecarneyyy', '0'], ['_m0ha', '0'], ['artislove', '1'], ['caliibeau', '0'], ['shot1of1whiskey', '1'], ['giasoriano_', '0'], ['andrewinaustin', '1'], ['ptabbiner', '7'], ['txkahashi', '0'], ['revertart', '0'], ['sarah_byham', '1'], ['tallbarry', '3'], ['sydneyvvvv', '0'], ['fancyshitbro', '1'], ['antoniskazou', '2'], ['nickjdenton', '0'], ['_emily_0331', '0'], ['pcs1776', '8'], ['caitlinkurvink', '0'], ['tlsmith625', '0'], ['ghosttgalaxy', '5'], ['coltinayres', '2'], ['prblematicpeach', '3'], ['uslawreview', '27'], ['brianrrs37', '3'], ['yosari_', '0'], ['mrmagonegro', '0'], ['wafflekingdavy', '3'], ['harvest_wind', '4'], ['flatearthcity', '6'], ['yigitispir', '1'], ['idfcmoran', '1'], ['andypalooza', '1'], ['robbycruz7', '0'], ['toffeealmondd', '1'], ['pod_panik', '1'], ['peruwiadomo', '0'], ['chillvibes_420', '1'], ['waleedlabhi', '2'], ['deefa45', '8'], ['non_believer001', '0'], ['jkildren625', '0'], ['poppylee53152', '6'], ['_thatniggacarl', '5'], ['trinakshyk', '10'], ['firewake32', '1'], ['portland_ghosts', '18'], ['cjkdwl', '2'], ['nothingsirius', '42'], ['marsweep', '13'], ['songz_ofmylife', '0'], ['ameri_grl', '0'], ['flatearthjason', '13'], ['scienceiswrong', '2'], ['donaldroche2', '13'], ['derekkleslie', '1'], ['realheine', '3'], ['klugectr', '141'], ['orrchidrain', '0'], ['mehrharris', '0'], ['jamiepart2', '1'], ['rodrigonunescal', '2'], ['geodedicated', '12'], ['esba1ley', '25'], ['xxjaycfreshxx', '3'], ['maradacy', '2'], ['itstylernicole', '0'], ['jeremybresley', '17'], ['livinapril7', '2'], ['attackontyson', '2'], ['sbarsh', '50'], ['barshbits', '33'], ['sinfuic', '2'], ['keremgogus', '7'], ['keke_fan_', '3'], ['scrapmetalrobot', '3'], ['mattcusson', '2'], ['goodyawards', '21'], ['neilhollywood', '8'], ['buffer', '1'], ['dun3buggi3', '39'], ['lovelyfunmom27', '1'], ['leesallyman', '7'], ['mujosey', '5'], ['jameszanardo', '23'], ['maddysettel', '6'], ['nutmegamillion', '1'], ['mattcorlett01', '3'], ['thegrannyhere', '0'], ['tc__joseph', '12'], ['teencher', '5'], ['uscdigital', '57'], ['theecobeat', '27'], ['hesupplanted', '0'], ['sannsibble', '19'], ['b0yle', '137'], ['lumabargo', '10'], ['jorgego98249461', '0'], ['woodsdiscovery', '8'], ['jon_vas2877', '2'], ['upportunityu', '94'], ['stratocumulus', '259'], ['rmgluck2017', '1'], ['adpcnet', '102'], ['kinglutherv', '1'], ['prezcannady', '9'], ['xploredeepspace', '595'], ['therealkyler_a', '0'], ['aguscipolicy', '398'], ['spaceartsae', '51'], ['nasa_sti', '46'], ['sengarypeters', '90'], ['lzcata', '2'], ['lilya_333', '3'], ['spacebrendan', '141'], ['boweswg', '6'], ['kiraonclimate', '18'], ['thecircuitmovie', '6'], ['dale_the_cooper', '157'], ['ripmyyoutth', '1'], ['sabriel_', '9'], ['broadsidebd', '6'], ['fednewsradio', '52'], ['aasandesign', '6'], ['mackbradley', '88'], ['drgitpaws', '0'], ['datawolf4005', '9'], ['freelancephilos', '21'], ['kool_duderex', '9'], ['janetepetro1', '7'], ['ken_yager', '4'], ['secondmuse', '118'], ['worldofscitech', '60'], ['martensjd', '7'], ['revamariepeter2', '0'], ['rcamp004', '19'], ['toddicus', '36'], ['petitpipo', '1'], ['gassygiant', '1'], ['swellbritta', '12'], ['jorgemurray98', '0'], ['orlandopride', '9'], ['bobbiebees', '0'], ['nova_r7', '3'], ['entrylevelrebel', '16'], ['georgeshornack', '3'], ['newscred', '0'], ['executivegov', '131'], ['mt_consult', '128'], ['egyptiankarim', '0'], ['daniel_thecuban', '2'], ['ewein2412', '1'], ['romansgirl2073', '0'], ['bzbx', '39'], ['itis4tom', '25'], ['newswhip', '19'], ['absolut_zer0', '5'], ['ramani_iyer', '47'], ['youssef_nfissi', '0'], ['gary_indiana', '0'], ['zajaczkowski', '65'], ['dailystarnews', '20'], ['joerymi', '6'], ['vbpaul88', '3'], ['newsfromspace', '402'], ['spacejournalism', '130'], ['boyerchristie', '2'], ['chia_jeslyn', '3'], ['timmermansr', '465'], ['kernelcob', '0'], ['albertalbs', '5'], ['mabsj2', '26'], ['rathertiresome', '4'], ['replaurahalld19', '17'], ['ju5t_v151t1ng', '226'], ['gutmicrobiomef', '0'], ['perolikeee_', '1'], ['nanowiz05', '5'], ['eplawiuk', '25'], ['stevekaliski', '10'], ['aagie', '88'], ['donnarapha', '2'], ['halleatonix', '5'], ['ucfh', '3'], ['vtwebdesign', '0'], ['muhiburshourov', '0'], ['michdsan14', '7'], ['ctdengineering', '6'], ['alienbeagle', '2'], ['adamjacobspdx', '1'], ['drewneisser', '6'], ['wjhuie', '58'], ['maggiemurphey', '2'], ['emceeslim', '4'], ['artofastronomy', '178'], ['ascendedmal', '5'], ['miabryce', '16'], ['katrobison', '70'], ['explorersinst', '29'], ['jonathanknowles', '224'], ['law4usc', '0'], ['tomholtzpaleo', '78'], ['rorystoves', '8'], ['gabbybirkman', '88'], ['mad_science_guy', '21'], ['ninazamparis', '2'], ['nfigueroajr', '210'], ['rappolee', '37'], ['ticsdaily', '6'], ['alimearza', '26'], ['mosestamakloe', '22'], ['twittermoments', '25'], ['smoothestknight', '23'], ['engryourworld', '30'], ['chomifelicidade', '0'], ['issyhjg', '0'], ['psproduct', '3'], ['dragonbox', '3'], ['kevinmlevy', '7'], ['malligoose', '6'], ['zacharycohn', '5'], ['scot_nature_boy', '26'], ['robrekemeyer', '0'], ['jannabernice', '4'], ['oconnorcolette', '0'], ['davidhu72182968', '0'], ['watertrends', '20'], ['mesraiders', '2'], ['florencedrakton', '1'], ['lastmanonmoon', '379'], ['lamboholic1', '0'], ['shelbyburon', '6'], ['jneal518_neal', '1'], ['19921974', '0'], ['sundhaug92', '7'], ['kimcungtv', '13'], ['alymurray', '1'], ['john1966olsen', '0'], ['thephoenixflare', '15'], ['tiikgarza', '4'], ['danpx2', '293'], ['unclejoe1116', '20'], ['toddharrisondc', '65'], ['trendrewards1', '19'], ['quixoticnance', '5'], ['scrubshine', '21'], ['aplusplus', '12'], ['sliztheboss', '4'], ['lucidfly', '12'], ['simoneroliver', '58'], ['judywang_', '12'], ['petercheong10', '13'], ['barry_corley', '17'], ['rohanpinto', '43'], ['radioxeu', '35'], ['navig_us', '5'], ['nayhamanzoor', '0'], ['annined', '13'], ['annie2488', '4'], ['oracle', '104'], ['marilinpeters', '1'], ['deplorable_ed', '0'], ['cptplanespotter', '0'], ['ghdatstate', '1'], ['bigelowlab', '30'], ['adambadger', '15'], ['cinnamonlester_', '0'], ['vic_alonsoperez', '7'], ['polyman71', '1'], ['curtnickisch', '23'], ['jessicacadams', '2'], ['tamu', '41'], ['djwarrenyoung', '8'], ['pradigy', '9'], ['now__space', '107'], ['_absterrr', '2'], ['aristofanea', '0'], ['maurice_edmonds', '0'], ['lora7777', '52'], ['astro_physical_', '20'], ['cenecmalaga', '13'], ['artsandlectures', '18'], ['jeffdeherdt', '4'], ['commandermla', '265'], ['dilicorne', '1'], ['rullys', '2'], ['craftlass', '92'], ['rosanne_sacto', '4'], ['mck_s6', '0'], ['cornerhub', '23'], ['sarah_begum', '6'], ['rhettwilliam', '0'], ['blackphysicists', '465'], ['jaybirdone', '5'], ['jorgeglz00', '1'], ['vicentvicedo', '0'], ['urmainegirl', '1'], ['raakwork', '21'], ['cynwyd5thgrade', '8'], ['questfloorcare', '4'], ['comfort_y', '8'], ['1_gflame', '66'], ['cosmos4u', '111'], ['olegreg42', '3'], ['sthilairelab', '10'], ['wakeyamindupej', '14'], ['mommage8386', '7'], ['nyambose3', '0'], ['defenseintel', '34'], ['rihadan', '2'], ['fbi', '13'], ['iitmweb', '5'], ['trixywh', '0'], ['bamit_das', '16'], ['robre62', '8'], ['peerthru', '13'], ['musicaltrees', '0'], ['fadilhamman', '7'], ['rtslabs', '36'], ['baronboehm', '3'], ['mcadookelly', '6'], ['debwhite', '3'], ['brotherbat', '0'], ['gammacounter', '3'], ['varon_carol', '0'], ['imnazim', '1'], ['isaacgaye', '5'], ['whyilikescience', '197'], ['stemedu_johnson', '0'], ['usembassysweden', '35'], ['birdseye1', '0'], ['letiziacaruso', '34'], ['sisteragenda', '17'], ['chrislucard', '137'], ['epicroxy', '0'], ['plabbe1', '0'], ['etphonegemini', '56'], ['physorg_com', '109'], ['tanyamariev', '1'], ['aldoadastra', '3'], ['californiakara', '9'], ['peterfortna', '9'], ['caseydreier', '133'], ['fyiscipolicy', '61'], ['stiltonninja', '12'], ['maximaxoo', '170'], ['marty_bolton', '8'], ['wieilc', '110'], ['grizzleytrubble', '1'], ['davelavery', '122'], ['ashekulhuq', '323'], ['adrianginger', '0'], ['skyatnightmag', '409'], ['irialouise', '3'], ['neurosocialself', '46'], ['dmvanderhoof', '9'], ['mayramontrose', '34'], ['thinkin_ape', '0'], ['helloclodagh', '18'], ['spacecasper', '865'], ['awb_org', '226'], ['onesynam', '1'], ['andjtjoeng', '1'], ['marksan04731571', '0'], ['housescience', '222'], ['shawnleenerts', '0'], ['doctorbrijpatel', '3'], ['jbprime', '148'], ['cmcelraft', '0'], ['edierodriguez', '0'], ['crgonzalez', '5'], ['artshumana', '37'], ['genefangirl', '2'], ['13blackangel13', '1'], ['eeg_uae', '14'], ['shuttlealmanac', '53'], ['charisgroup', '3'], ['janineingram7', '5'], ['lindyloo1979', '0'], ['rasamataz_lv', '1'], ['trinity_u', '15'], ['zezeswanson', '0'], ['realkyleolbert', '11'], ['ouphyssci', '27'], ['aircraftnerds', '0'], ['jonathanlhall', '19'], ['svathome', '4'], ['storybywill', '24'], ['glytchtech', '2'], ['changeequation', '272'], ['p5umno', '4'], ['glennostrosky', '0'], ['gracetiscareno', '3'], ['stormseeker79', '1'], ['hivezine_', '6'], ['cntroversyincda', '10'], ['spacecoral', '8'], ['joesibanez', '2'], ['claudiaalvaran2', '2'], ['gomez4224', '5'], ['keystounlocking', '5'], ['pillownaut', '51'], ['kurafire', '4'], ['maximodalmau', '7'], ['smittydarling', '5'], ['pc0101', '3'], ['usembislamabad', '12'], ['drunken_neo', '9'], ['bricknix', '3'], ['hocochamber', '12'], ['wmckimney', '0'], ['its_en_not_on', '2'], ['masoomjethwa', '1'], ['draken50', '2'], ['0x4e0x650x6f', '5'], ['sydneysneckka', '0'], ['smoothcat', '9'], ['usgao', '61'], ['fueladdicts', '17'], ['kiss999', '2'], ['power965', '0'], ['johnsanders0', '0'], ['javifenoy', '7'], ['chughtaienge813', '3'], ['heyarnoldc', '3'], ['hpstan', '0'], ['lauriecantillo', '213'], ['xeni', '3'], ['mikenasatir', '1'], ['robertjshoupe', '1'], ['meddevcentre', '86'], ['darkparadise0m', '0'], ['annmaura', '4'], ['storyblockmedia', '6'], ['americorps', '3'], ['avramovk', '0'], ['discoveryhour', '1465'], ['phibetakappa', '228'], ['ufnations', '86'], ['usveteransmag', '4'], ['mindy777', '0'], ['jmuplanetarium', '288'], ['atm_husband', '1'], ['robinhicks_', '22'], ['roysimangunsong', '3'], ['maggiecort', '0'], ['astrotek', '329'], ['mermaidcarnell', '5'], ['edbailey1957', '8'], ['vabeachteach', '31'], ['minorleaguesman', '2'], ['shravansaxena', '12'], ['usambindia', '69'], ['tracy_karin', '22'], ['spaceleclerc', '99'], ['obastronomy', '211'], ['sylvia_opella', '0'], ['lmb_spa', '1'], ['eternal_voyager', '4'], ['micha_louis', '1'], ['heriabusufyan92', '5'], ['udaykarve', '1'], ['daaronherman', '1'], ['bis_spaceflight', '57'], ['lislelibrary', '30'], ['tylerfeague', '4'], ['edmatters', '25'], ['dtlafave', '0'], ['misspattyx', '5'], ['engineeringcom', '108'], ['educateeng', '22'], ['stampydragon', '18'], ['the_real_isamar', '0'], ['imam_a_siddique', '1'], ['ageekmom', '97'], ['exeteruninews', '4'], ['gabeberto57', '1'], ['licholding', '2'], ['happynestmegi', '16'], ['dannytheinfidel', '0'], ['misterhw', '3'], ['feonixforever', '0'], ['comicbooknerd23', '2'], ['nehayadav2058', '0'], ['spacecenterhou', '272'], ['rinchenmtp', '11'], ['nicharsh', '10'], ['nickfalacci', '3'], ['prishkachu', '10'], ['rieinspire', '6'], ['ilovemarsfans', '32'], ['eusapient', '4'], ['lorimoreno', '18'], ['oetkb2', '2'], ['v_septembre', '1'], ['selvynk', '0'], ['therealdjflux', '124'], ['ouachitaways', '0'], ['iss_casis', '465'], ['lomhow1234', '3'], ['brooklynweaver', '1'], ['reinepsy', '0'], ['27chips', '2'], ['posco69', '3'], ['dreducacion', '0'], ['jenoconnell', '4'], ['astromicerule', '65'], ['donalddjl', '0'], ['squasherg', '0'], ['tentivetodetail', '7'], ['mattpegram', '4'], ['callyra', '0'], ['edisonawards', '226'], ['coloradonewsccm', '7'], ['mighty_humanzee', '45'], ['nasakepler', '511'], ['dara2c', '0'], ['jeffdsalisbury', '6'], ['holygoat_420', '0'], ['r_sharrock', '19'], ['skankbones', '1'], ['studiokca', '4'], ['lsullivan', '219'], ['sp_johnsullivan', '5'], ['raverfrom95', '0'], ['saber_smith', '3'], ['epbock', '12'], ['koz_99', '2'], ['surfsidesams', '3'], ['orbitalatk', '289'], ['jstephengagnon', '29'], ['restlessone14', '8'], ['aims600doc', '3'], ['nasa360', '292'], ['cheriedlyon1', '5'], ['needimages', '0'], ['whybankcollapse', '1'], ['lwaltzing', '0'], ['duckhunter9090', '0'], ['h_t_adams', '0'], ['lilcuriouscatt', '0'], ['sanchiaalasia', '4'], ['tlaustin', '14'], ['smartvedha', '0'], ['slyfoxninja', '5'], ['heywerner59', '21'], ['allisonkkelly', '150'], ['uglyfossils', '4'], ['rajkvx', '2'], ['eclark1946', '0'], ['jennikeleher1', '0'], ['isaacvollmer', '0'], ['nmarascio', '25'], ['cindyrourke23', '1'], ['oo2112', '0'], ['bryanbriggs6', '0'], ['gracieruiz', '3'], ['jgoku18', '0'], ['easysun_power', '39'], ['mrsgyde', '1'], ['spaceflightins', '250'], ['miss_space_geek', '13'], ['uppitynycupcake', '2'], ['addisonryan', '0'], ['scaley_jencen', '4'], ['t_dubs82', '0'], ['ruthspiro', '12'], ['to_the_breach', '20'], ['redidbull', '0'], ['skiestercfi', '1'], ['kneazleknickers', '7'], ['livn2lo19', '0'], ['psutympany', '3'], ['jess_walker', '2'], ['kuppachiravi', '3'], ['mamtajain4215', '0'], ['patf758', '0'], ['jaisinghessar', '0'], ['x_gillian_x', '0'], ['applixir', '3'], ['denkbots', '13'], ['anjalikolachala', '1'], ['skywatchapps', '177'], ['king_rkin279', '0'], ['oubey', '640'], ['tsgz7zv3ydwqted', '22'], ['djfrankieee', '26'], ['matthewnorris82', '0'], ['belinsan61', '0'], ['meiklewilliam', '11'], ['dunlapcj', '13'], ['huile_de_olive', '4'], ['maskinjunior', '1'], ['cinberas', '4'], ['jrmsaunders', '9'], ['rachreneebell', '4'], ['discoverdonovan', '5'], ['raminsubzero', '10'], ['lotusg13', '0'], ['thegatecast', '2'], ['krystalondesign', '19'], ['michelelauriat', '2'], ['adrianf1erros', '0'], ['agiantjenna', '2'], ['disruptive55', '162'], ['immortalmirco', '2'], ['rtdasilva3', '2'], ['rgesthuizen', '106'], ['dayne_cov', '1'], ['leerum6', '0'], ['mr_james_c', '2'], ['miss_lewis5', '2'], ['ajpearson23', '9'], ['tinapanossian', '12'], ['nancyfordephoto', '8'], ['beardedsavagenh', '0'], ['beegejohnson', '31'], ['eringreeson', '63'], ['astrophiz', '286'], ['bhgross144', '139'], ['randy00312', '0'], ['astronobeads', '9'], ['smithsk', '735'], ['frankowluke', '1'], ['theiet', '62'], ['slaydott', '1'], ['fcojlg', '0'], ['ldaycalico', '5'], ['giftofwealth', '0'], ['jamesgis', '17'], ['907natalie', '2'], ['melissa_shelley', '6'], ['andrej_gross', '15'], ['jcbreckjac', '0'], ['kamla_sharbear', '13'], ['calminc', '3'], ['irondog55', '0'], ['jaggeroriginal', '3'], ['margeaux_fr', '1'], ['xadellebellex', '3'], ['_herbbaker', '88'], ['robinwhitsell', '119'], ['just1fix2004', '17'], ['stwilfridsmaths', '2'], ['uolnewscentre', '138'], ['uniofleicester', '51'], ['plasmarmuse', '91'], ['rjmlaird', '127'], ['chrisfflyer', '15'], ['clcwju', '11'], ['antarikshghosh1', '0'], ['consultseuss', '34'], ['thechaosclangfa', '13'], ['shasani61', '11'], ['theobproject', '91'], ['smoroi', '0'], ['fionaaldridge', '9'], ['fallenstar_ana', '0'], ['bigdaddypete', '20'], ['ukspaceacademy', '190'], ['lancecaraccioli', '3'], ['carbon_flight', '58'], ['capitalemnews', '4'], ['jean_labbe', '7'], ['kulganofcrydee', '7'], ['davidsornberger', '60'], ['rocketmanjrs', '3'], ['robamorg', '16'], ['astroperseo', '68'], ['jgrplanets', '95'], ['hmns', '138'], ['kevindavis338', '74'], ['4girlcrew', '0'], ['allstuffspace', '21'], ['richwajda', '3'], ['taustation', '186'], ['fizzbulous', '13'], ['mmmukalla', '0'], ['creepertrent115', '8'], ['scottpiano1', '2'], ['windsormorning', '16'], ['craignorriscbc', '12'], ['morningnorth', '15'], ['im_ebg', '51'], ['mrmonster911', '92'], ['rory_mg', '43'], ['emspeck', '198'], ['joseph_eilert', '7'], ['classic_thuli', '1'], ['vaidabhishek', '3'], ['orbital_decay', '102'], ['zachadams74', '2'], ['tallandtrue', '24'], ['anime_fan77', '7'], ['flndr6', '20'], ['rotosequence', '20'], ['doughensel', '9'], ['transcendtales', '29'], ['masanorimusic', '6'], ['spacedlaw', '2'], ['tskynet', '8'], ['algi80', '12'], ['philae_ptolemy', '4'], ['vincenzoloscalz', '54'], ['mnmlbit', '44'], ['askewmind', '16'], ['bp_hutch', '61'], ['splinister', '15'], ['i_we_gaia', '29'], ['loubrutus', '9'], ['mattkronner', '0'], ['thev1nce', '1'], ['dwenius', '3'], ['thatawesometerr', '6'], ['grilled_onion', '0'], ['ocultado', '3'], ['bernhard_weyhe', '9'], ['jeanneb1962', '1'], ['fragraptor', '5'], ['dunn_pa', '0'], ['ryanmerkley', '45'], ['robcwolfe', '1'], ['paxxman', '2'], ['jeev12194', '0'], ['lord_bung', '5'], ['sinkoj', '29'], ['ronbaalke', '213'], ['giannipetitti', '2'], ['kssecrets', '1'], ['vyomnaut', '0'], ['only1marcia', '1'], ['jon__hoff', '0'], ['sergey_reznik', '0'], ['jjuday', '4'], ['writertracy', '15'], ['mhs_science', '303'], ['jovanbkt', '59'], ['ploberman', '62'], ['ieeeorg', '178'], ['uoyastrosoc', '17'], ['wingdcanada', '38'], ['scienceatwingd', '21'], ['guerillascience', '138'], ['hal9000and1', '6'], ['princecyboi', '11'], ['stuartaken', '5'], ['paul_hayslip', '2'], ['f_rodriguezjr', '0'], ['asimpleresponse', '20'], ['onreact_com', '20'], ['cosmocrops', '66'], ['trassens', '68'], ['acecentric', '358'], ['astrobiologytop', '333'], ['ecroydon', '0'], ['esfs_canada', '60'], ['chrisdmarshall', '120'], ['biophyskrys', '22'], ['mew19forever', '2'], ['gograzi', '1'], ['meister_art', '0'], ['expresstechie', '116'], ['chic4change', '12'], ['flos_ad_mare', '1'], ['interplanetypod', '381'], ['cselas', '0'], ['pollick_chris', '0'], ['hellobezlo', '18'], ['harrisonfinnian', '33'], ['dstephen132', '0'], ['kartikparija', '68'], ['nasahistory', '703'], ['pemcoworldair', '9'], ['fertaddei', '0'], ['peoplewcooljobs', '5'], ['piotr_wiorek', '0'], ['cary_northrop', '2'], ['kirstinmcewan', '26'], ['handsanfeet', '2'], ['umakantgohatre', '4'], ['asnell620', '5'], ['aviationheritag', '14'], ['stevespaleta', '10'], ['davidlxho', '102'], ['exor_dg', '0'], ['tcmindy', '188'], ['deepakrajgor', '26'], ['ijaz7425', '0'], ['kuldeep89815740', '0'], ['catphrodite', '5'], ['fadumzz', '3'], ['davidbsweather', '7'], ['gobusurv', '1'], ['ayeiibor', '3'], ['rubennews', '28'], ['bunting29', '0'], ['spacemonkeyluvn', '7'], ['renecc', '2'], ['pamfloresmusic', '0'], ['parkerhuse', '0'], ['wms00bowvgy3efx', '0'], ['kenleypdx', '0'], ['akhil_am_', '1'], ['space_wombat', '10'], ['zaynsmjolnir', '8'], ['ddmarketingtalk', '0'], ['mallory_mack', '1'], ['pamelacayne', '4'], ['voidsebastian', '6'], ['cosmiccuttlefsh', '4'], ['charlesgare40', '50'], ['garrixhuman', '94'], ['victoria_ramen', '36'], ['steveyeasting', '0'], ['omandoriginal', '0'], ['nerdforaliving', '5'], ['leahazucenas', '1'], ['yoda', '6'], ['gabrielpbruce', '0'], ['mimi_ohare', '0'], ['josiecreates', '7'], ['jennclitler', '1'], ['janetbooklady', '0'], ['alexteha', '0'], ['bobsfeedback', '0'], ['richard_bruschi', '47'], ['munglooh', '0'], ['cvdevkatesakal', '0'], ['ogharit', '1'], ['traidmark', '95'], ['natashacormac', '1'], ['apeximagingmike', '4'], ['taylormmeredith', '1'], ['docnotdoctor', '7'], ['markpaintt', '0'], ['astroguyz', '414'], ['miss_bored_alot', '6'], ['saxopolis', '3'], ['magicsanchez4', '10'], ['egeline1958', '14'], ['ianakki07', '0'], ['rockandjoel', '6'], ['manthonybrowne', '4'], ['jonoabroad', '3'], ['kennymcpirate', '2'], ['marietherrien45', '0'], ['issaboveyou', '0'], ['bwgibbo333', '0'], ['gimamedjian', '0'], ['crkarla', '143'], ['algotechnews', '569'], ['carlaxys5', '2'], ['jamesmoore_org', '40'], ['kkidsny', '27'], ['spooninspace', '10'], ['engphoto', '3'], ['mrm0726', '70'], ['ks_edmktg', '26'], ['hammersuit', '1'], ['sarahcamille95', '0'], ['hackerspacela', '67'], ['lotg60', '9'], ['dslsynth', '1'], ['bosrealteolaiga', '5'], ['ujs6591', '9'], ['thebutcher_st', '0'], ['tomtom28115', '29'], ['funkygreencomet', '10'], ['morningexp', '15'], ['youkenn_doit', '3'], ['longquint', '14'], ['science_hooker', '179'], ['amylia80', '0'], ['heinrichalberts', '8'], ['alexbiebricher', '2483'], ['spac307cowboy', '13'], ['aschwortz', '30'], ['anissagoesrawr', '5'], ['thesoulfulemu', '7'], ['lilygwenya', '1'], ['ffff2003cn20051', '0'], ['korsasap', '236'], ['ripudaman_usha', '112'], ['adrianw_w', '5'], ['alastairkingon', '1'], ['brooklyncybele', '2'], ['lenalazyeye', '1'], ['aicsinspace', '218'], ['allensaakyan', '15'], ['elizejackson', '4'], ['traumajunkie17', '16'], ['fwd79', '11'], ['efayeme', '5'], ['krrrod24', '1'], ['teachkidsnews', '74'], ['_andrewgregg', '6'], ['ericbaize', '21'], ['pyrotasticuk', '3'], ['libertyscictr', '88'], ['sabareeshpa', '0'], ['casualelephant', '1'], ['whatdamath', '666'], ['alicia_j_burke', '1'], ['___missfisher', '3'], ['richworkzone', '7'], ['hermann250', '0'], ['madik', '3'], ['mal7798', '14'], ['marsroverdriver', '47'], ['profmike_m', '10'], ['nebogipfelwho', '2'], ['msangelapacheco', '2'], ['laurabaxter3', '2'], ['kierandean', '0'], ['meg_eastwood', '12'], ['chaosaholic', '3'], ['californiiya', '1'], ['c_holce', '2'], ['dionadrienne24', '0'], ['realindytaiis24', '0'], ['mechtwintailed', '1'], ['jethrotoll', '0'], ['danieljoneslee1', '0'], ['captamerica1787', '0'], ['paul_kidk9299', '0'], ['yohangerm', '1'], ['ashpeeweezy', '17'], ['_paigemaddy', '8'], ['cyberen', '4'], ['lifebypierre', '0'], ['stellarplanet', '502'], ['spaceagenda', '628'], ['brainmaker', '377'], ['gpknopp', '6'], ['iteratedmnifold', '3'], ['marsanalogues', '25'], ['livingarchitect', '67'], ['jpmajor', '205'], ['nccomfort', '97'], ['greenstemsuoy', '15'], ['astronomymike', '147'], ['erthscicarleton', '9'], ['humanoidhistory', '1618'], ['ststherapies', '0'], ['poison_iveen', '2'], ['djcalla7', '0'], ['faithelarue', '1'], ['daryariz', '1'], ['thefuckfather', '1'], ['kelseyevans1411', '1'], ['kaethe_butcher', '1'], ['grimmly_icarus', '0'], ['realesttruthsof', '1'], ['yel_sales', '0'], ['jaquelineza14', '1'], ['nectvr', '1'], ['traphikpromo', '1'], ['oliviaspyra', '1'], ['tomgranzzz', '0'], ['therealqaisar', '0'], ['matttyy_x', '0'], ['sacc_daddy', '5'], ['shanaduchin', '1'], ['mischaparry', '3'], ['thedarkestsq', '2'], ['larrry_', '1'], ['theillestone_', '0'], ['kerouazy', '4'], ['michinojosa', '3'], ['gq_ds', '2'], ['chalexiss', '0'], ['devlishboy10', '1'], ['mberwebb', '2'], ['suckmy_wayne', '0'], ['psdifabio', '6'], ['bmas925yeah12', '0'], ['f000lsg0ld', '5'], ['shelbz_1997', '2'], ['megsbella', '3'], ['sadiyayoung', '3'], ['rosieshamoon', '3'], ['g333jordan', '11'], ['mikey_shai', '2'], ['oceonwalker', '1'], ['vivianacalianno', '0'], ['pyq87', '2'], ['spkrshutup', '0'], ['thatoneoffig', '0'], ['camillezy', '2'], ['nikki_muffin', '1'], ['joseuzi_32', '0'], ['kdaileydose', '1'], ['youngkainno', '0'], ['410383n719505w', '15'], ['kokoalak0900', '0'], ['handynsac', '0'], ['samskit82', '0'], ['fcallian', '0'], ['coolblkguy', '4'], ['glamretweet', '0'], ['haydenmrut', '0'], ['kaidaddy219', '2'], ['stackshabazz', '1'], ['donsean_', '3'], ['semendemon25', '0'], ['c_cakau', '22'], ['emilymaine_', '0'], ['boristhespiderr', '1'], ['mrmarshallman3', '0'], ['ajtweetss', '2'], ['updatenewslive', '35'], ['_elholmes', '3'], ['imperatortruth', '18'], ['_patrek_', '0'], ['greennnelly', '2'], ['briannacostaa', '0'], ['insidertruelife', '0'], ['khvdimbaye', '4'], ['adit_prada', '0'], ['beachy_jack', '3'], ['k9rotts', '6'], ['shoutingvoids', '11'], ['victor17115660', '0'], ['nicolesteenrod', '1'], ['beneluxufo', '0'], ['wozzels', '0'], ['jasoncrg', '16'], ['mur06067673', '0'], ['popelawson2011', '2'], ['megvivacious', '2'], ['vipasha1999', '0'], ['19jpullen68', '0'], ['kamakapahinui', '0'], ['sunsetsari', '1'], ['dclintf', '1'], ['yogabbygabbax', '0'], ['jaimecook13', '2'], ['7_samgrande_7', '0'], ['eliz_gaskins', '0'], ['urbanblisslife', '10'], ['jessevlogs123', '0'], ['jamia_rain', '8'], ['alxxa966', '3'], ['logesteele', '3'], ['thischickgigi', '5'], ['ipressthis', '59'], ['dale_katy', '1'], ['zclaor', '0'], ['callummiley74', '0'], ['zzahraalqahtani', '0'], ['simplyalyss', '2'], ['simplycinfulxxx', '1'], ['kkksavannah', '0'], ['jmswsr', '3'], ['realninolord', '3'], ['suit_kase_', '0'], ['shae_best_', '0'], ['carlaandrade_', '1'], ['savionwright', '0'], ['kiera_5sos', '0'], ['shankhunt69', '0'], ['themadhatter355', '2'], ['midnight__music', '0'], ['obeys_creek', '1'], ['christineeekim', '0'], ['brittfink', '2'], ['rothtravo', '1'], ['lstoff2', '2'], ['rolljleah', '0'], ['alienboy708', '9'], ['peterfelth', '6'], ['dtreco13', '0'], ['amir_hali', '14'], ['jlgnava', '60'], ['auntiejamamab', '4'], ['rcgoodman02', '1'], ['ruperthucks', '1'], ['kompananzi', '7'], ['eyeswide2see', '0'], ['nomorelobbiest', '5'], ['internatlgmr1', '0'], ['lniggeling1', '0'], ['chadoakhill', '3'], ['tjalmere', '0'], ['kevinni75074015', '8'], ['regalinterloper', '0'], ['ilooktwice', '0'], ['_monkey_boy_', '3'], ['killjoy044', '0'], ['ireland_rhain', '0'], ['robbofoz', '0'], ['jennae16_', '2'], ['violet1962', '2'], ['meagswins', '1'], ['delozier_m', '5'], ['_e0ll4a_', '0'], ['infotechnologi', '4'], ['juanp12_227', '1'], ['gl3a99', '0'], ['bikinatroll', '33'], ['jamariqui2', '0'], ['lazer789', '5'], ['maskulin4_life', '0'], ['misserdoodles', '0'], ['red4eva71', '7'], ['actionb0ss', '0'], ['neerovra', '0'], ['devnull23', '19'], ['surgpathatlas', '8'], ['whorerfilms', '0'], ['golddraco_13', '0'], ['bizzyblazinbudz', '4'], ['arc_nu', '2'], ['jeaighwalker', '1'], ['mentestropeada', '1'], ['conorivera', '0'], ['yaboijose_', '0'], ['nebiund', '3'], ['dahk_holliday', '2'], ['hashtag1o1', '1'], ['thelordnoel', '1'], ['mr_5h33pd06', '8'], ['tallamotorsport', '0'], ['ironmanindiandr', '4'], ['rahulsangwan111', '0'], ['garbtweeter', '1'], ['d_nicee11', '2'], ['iseedjustice', '1'], ['kampotyler', '0'], ['markgarrington', '0'], ['sawdust1620', '2'], ['darealassassin', '0'], ['tarawasjesus', '2'], ['ay_strike', '0']]

# print (len(tweets))
#
# temp = []
#
# for t in tweets:
#
#     if t[0] not in temp:
#         temp.append(t[0])
#
# print (len(temp))

nodes_and_keyword_count_dict = {}

for nk in nodes_and_keyword_count:
    key = nk[0]
    nodes_and_keyword_count_dict[key] = nk[1]

print (nodes_and_keyword_count_dict)

trust_links = [['elliedvs','nasa','trust_yes'],['elliedvs','nasa','trust_no'],['ffsgeorge','nasa','trust_yes']]

keyword_and_label = []

for tl in trust_links:

    if tl[0] in nodes_and_keyword_count_dict:
        keyword_and_label.append([nodes_and_keyword_count_dict[tl[0]], tl[2]])

    else:
        keyword_and_label.append(['0', tl[2]])

print (keyword_and_label)