#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:54:25 2019

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

#total_play_count = sum(user_song_list_count.listen_count)
#print('5,000 most popular songs represents {:3.2%} of total listen.'.format(float(play_count.sum())/total_play_count))

play_count = user_song_list_count[['song', 'listen_count']].groupby('song').sum().\
             sort_values(by='listen_count',ascending=False).head(5000)
song_subset = list(play_count.index[:5000])
user_subset = list(user_song_list_count.loc[user_song_list_count.song.isin(song_subset), 'user'].unique())
user_song_list_count_sub = user_song_list_count[user_song_list_count.song.isin(song_subset)]

user_id = list(user_song_list_count_sub.user)[7] #Insert user id here 

user_data = user_song_list_count_sub[user_song_list_count_sub['user'] == user_id]
user_songs = list(user_data['title'].unique())
all_songs =list(user_song_list_count_sub['title'].unique())

user_songs_users = []
for i in range(0, len(user_songs)):
    item_data = user_song_list_count_sub[user_song_list_count_sub['title'] == user_songs[i]]
    item_users = set(item_data['user'].unique())
    user_songs_users.append(item_users)

#display(user_songs_users)

cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)
for i in range(0,len(all_songs)):
        songs_i_data = user_song_list_count_sub[user_song_list_count_sub['title'] == all_songs[i]]
        users_i = set(songs_i_data['user'].unique())
        for j in range(0,len(user_songs)):       
            users_j = user_songs_users[j]
            users_intersection = users_i.intersection(users_j)
            
            if len(users_intersection) != 0:
                users_union = users_i.union(users_j)
                cooccurence_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
            else:
                cooccurence_matrix[j,i] = 0

user_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
user_sim_scores = np.array(user_sim_scores)[0].tolist()
sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)

columns = ['user_id', 'song', 'score', 'rank']
df = pd.DataFrame(columns=columns)

rank = 1 
for i in range(0,len(sort_index)):
    if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= 10:
        df.loc[len(df)]=[user_id,all_songs[sort_index[i][1]],sort_index[i][0],rank]
        rank = rank+1
        
if df.shape[0] == 0:
    print("The current user has no songs for training the item similarity based recommendation model.")
else:
    print(df)
