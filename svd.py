#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:36:52 2019

@author: sachet
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import math as mt
from scipy.sparse import csc_matrix
from scipy.sparse import coo_matrix

track_metadata=pd.read_csv('/home/sachet/Artificial Intelligence/song_data.csv')
count_play = pd.read_csv('/home/sachet/Artificial Intelligence/10000.txt', sep='\t', header=None, names=['user','song','play_count'])
unique_track_metadata = track_metadata.groupby('song_id').max().reset_index()
user_song_list_count = pd.merge(count_play, unique_track_metadata, how='left', left_on='song', right_on='song_id')
user_song_list_count.rename(columns={'play_count':'listen_count'},inplace=True)
del(user_song_list_count['song_id'])

user_song_list_listen = user_song_list_count[['user','listen_count']].groupby('user').sum().reset_index()
user_song_list_listen.rename(columns={'listen_count':'total_listen_count'},inplace=True)
user_song_list_count_merged = pd.merge(user_song_list_count,user_song_list_listen)
user_song_list_count_merged['fractional_play_count'] = \
user_song_list_count_merged['listen_count']/user_song_list_count_merged['total_listen_count']

user_codes = user_song_list_count_merged.user.drop_duplicates().reset_index()
user_codes.rename(columns={'index':'user_index'}, inplace=True)
user_codes['us_index_value'] = list(user_codes.index)

song_codes = user_song_list_count_merged.song.drop_duplicates().reset_index()
song_codes.rename(columns={'index':'song_index'}, inplace=True)
song_codes['so_index_value'] = list(song_codes.index)

small_set = pd.merge(user_song_list_count_merged,song_codes,how='left')
small_set = pd.merge(small_set,user_codes,how='left')
mat_candidate = small_set[['us_index_value','so_index_value','fractional_play_count']]

data_array = mat_candidate.fractional_play_count.values
row_array = mat_candidate.us_index_value.values
col_array = mat_candidate.so_index_value.values

data_sparse = coo_matrix((data_array, (row_array, col_array)),dtype=float)
print(data_sparse)

K=50
urm = data_sparse
MAX_PID = urm.shape[1]
MAX_UID = urm.shape[0]

U, s, Vt = svds(urm, K)
dim = (len(s), len(s))
S = np.zeros(dim, dtype=np.float32)
for i in range(0, len(s)):
    S[i,i] = mt.sqrt(s[i])
U = csc_matrix(U, dtype=np.float32)
S = csc_matrix(S, dtype=np.float32)
Vt = csc_matrix(Vt, dtype=np.float32)

uTest = [4,5,6,7,8,873,23] #insert user id here
rightTerm = S*Vt 
max_recommendation = 250
estimatedRatings = np.zeros(shape=(MAX_UID, MAX_PID), dtype=np.float16)
recomendRatings = np.zeros(shape=(MAX_UID,max_recommendation ), dtype=np.float16)
for userTest in uTest:
    prod = U[userTest, :]*rightTerm
    estimatedRatings[userTest, :] = prod.todense()
    recomendRatings[userTest, :] = (-estimatedRatings[userTest, :]).argsort()[:max_recommendation]

num_recomendations = 10
uTest_recommended_items = recomendRatings
for user in uTest:
    print('-'*70)
    print("Recommendation for user id {}".format(user))
    rank_value = 1
    i = 0
    while (rank_value <  num_recomendations + 1):
        so = uTest_recommended_items[user,i:i+1][0]
        if (small_set.user[(small_set.so_index_value == so) & (small_set.us_index_value == user)].count()==0):
            song_details = small_set[(small_set.so_index_value == so)].\
            drop_duplicates('so_index_value')[['title','artist_name']]
            print("The number {} recommended song is {} BY {}".format(rank_value, list(song_details['title'])[0],list(song_details['artist_name'])[0]))
            rank_value+=1
        i += 1