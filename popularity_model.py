import pandas as pd
import numpy as np

track_metadata=pd.read_csv('/home/sachet/AI/song_data.csv')
count_play = pd.read_csv('/home/sachet/AI/10000.txt', sep='\t', header=None, names=['user','song','play_count'])
unique_track_metadata = track_metadata.groupby('song_id').max().reset_index()
user_song_list_count = pd.merge(count_play, unique_track_metadata, how='left', left_on='song', right_on='song_id')
user_song_list_count.rename(columns={'play_count':'listen_count'},inplace=True)
del(user_song_list_count['song_id'])

score_list=user_song_list_count.groupby(['title']).agg({'user': 'count'}).reset_index()
score_list.rename(columns={'user': 'score'}, inplace=True)
sorted_score_list=score_list.sort_values(['score','title'], ascending=[0,1])
popularity_recommendations = sorted_score_list.head(10)
print(popularity_recommendations)