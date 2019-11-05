#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:41:39 2019

@author: sachet
"""

import pandas as pd 
import numpy as np

def preprocessing():
    """Function to return user_song_list_count which has data of all users and the count of songs the user has listened to."""
    track_metadata = pd.read_csv('/home/sachet/Artificial Intelligence/song_data.csv')
    count_play = pd.read_csv('/home/sachet/Artificial Intelligence/10000.txt', sep='\t', header=None, names=['user','song','play_count'])
    unique_track_metadata = track_metadata.groupby('song_id').max().reset_index()
    user_song_list = pd.merge(count_play, unique_track_metadata, how='left', left_on='song', right_on='song_id')
    user_song_list.rename(columns={'play_count':'listen_count'},inplace=True)
    del(user_song_list['song_id'])
    return user_song_list
    
user_song_list_count = preprocessing()

play_count = user_song_list_count[['song', 'listen_count']].groupby('song').sum().\
             sort_values(by='listen_count',ascending=False).head(5000)
song_subset = list(play_count.index[:5000])
user_subset = list(user_song_list_count.loc[user_song_list_count.song.isin(song_subset), 'user'].unique())
user_song_list_count_sub = user_song_list_count[user_song_list_count.song.isin(song_subset)]

user_id = list(user_song_list_count_sub.user)[7] #Insert user id here 

user_data = user_song_list_count_sub[user_song_list_count_sub['user'] == user_id]
user_songs = list(user_data['title'].unique())
all_songs =list(user_song_list_count_sub['title'].unique())

def get_user_items(user):
        user_data = user_song_list_count_sub[user_song_list_count_sub['user'] == user]
        user_items = list(user_data['title'].unique())
        return user_items

not_songs = [song for song in all_songs if song not in user_songs]
not_song_users=[]
for song in not_songs:
    for ind in user_song_list_count_sub.index:
        if song==user_song_list_count_sub['title'][ind]:
            if user_song_list_count_sub['user'][ind] not in not_song_users:
                not_song_users.append(user_song_list_count_sub['user'][ind])

all_users =list(user_song_list_count_sub['user'].unique())

cooccurence_matrix = np.matrix(np.zeros(shape=(len(not_song_users), len(all_users))), float)
for i in range(0,len(all_songs)):
        user_i_songs=get_user_items[all_users[i]]
        for j in range(0,len(not_song_users)):   
            user_j_songs=get_user_items[all_users[j]]
            songs_intersection=user_i_songs.intersection(user_j_songs)
            if len(songs_intersection) != 0:
                songs_union = user_i_songs.union(user_j_songs)
                cooccurence_matrix[j,i] = float(len(songs_intersection))/float(len(songs_union))
            else:
                cooccurence_matrix[j,i] = 0

song_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
song_sim_scores = np.array(song_sim_scores)[0].tolist()
sort_index = sorted(((e,i) for i,e in enumerate(list(song_sim_scores))), reverse=True)
