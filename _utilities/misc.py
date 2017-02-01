
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

import sys

l1 = ['a','b','c','d','e']
l2 = ['a','c','b']

l3 = []

for index,l in enumerate(l1):

    for m in l2:
        if m == l:
            l3.append([index,m])

print (l3)

max_element = max(l3, key = lambda x:x[0])
max_index = max_element[0]

print (max_index)


sublist = l1[max_index+1:]
print (sublist)

# ff = [[0, 'a'], [1, 'b'], [2, 'c']]
#
# zz=max([x[0] for x in ff])
#
# print (zz)





