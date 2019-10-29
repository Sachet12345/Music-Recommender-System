#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:54:25 2019

@author: sachet
"""

import pandas as pd 
import numpy as np

track_metadata=pd.read_csv('/home/sachet/Artificial Intelligence/song_data.csv')
count_play = pd.read_csv('/home/sachet/Artificial Intelligence/10000.txt', sep='\t', header=None, names=['user','song','play_count'])
unique_track_metadata = track_metadata.groupby('song_id').max().reset_index()
user_song_list_count = pd.merge(count_play, unique_track_metadata, how='left', left_on='song', right_on='song_id')
user_song_list_count.rename(columns={'play_count':'listen_count'},inplace=True)
del(user_song_list_count['song_id'])

#total_play_count = sum(user_song_list_count.listen_count)
#print('5,000 most popular songs represents {:3.2%} of total listen.'.format(float(play_count.sum())/total_play_count))

play_count = user_song_list_count[['song', 'listen_count']].groupby('song').sum().\
             sort_values(by='listen_count',ascending=False).head(5000)
song_subset = list(play_count.index[:5000])
user_subset = list(user_song_list_count.loc[user_song_list_count.song.isin(song_subset), 'user'].unique())
user_song_list_count_sub = user_song_list_count[user_song_list_count.song.isin(song_subset)]

user_id = list(user_song_list_count_sub.user)[7]
user_data = user_song_list_count_sub[user_song_list_count_sub['user'] == user_id]
user_songs = list(user_data['title'].unique())
all_songs =list(user_song_list_count_sub['title'].unique())

user_songs_users = []
for i in range(0, len(user_songs)):
    item_data = user_song_list_count_sub[user_song_list_count_sub['title'] == user_songs[i]]
    item_users = set(item_data['user'].unique())
    user_songs_users.append(item_users)
            
cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)
for i in range(0,len(all_songs)):
        songs_i_data = user_song_list_count_sub[user_song_list_count_sub['title'] == all_songs
        users_i = set(songs_i_data['user'].unique())
        for j in range(0,len(user_songs)):       
            users_j = user_songs_users[j]
            