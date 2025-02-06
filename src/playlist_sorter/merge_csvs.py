from pprint import pprint
import pandas as pd
import os


# Tried using sound analysis from kaggle dataset
# high_pop_songs = pd.read_csv('data/high_popularity_spotify_data.csv')
# low_pop_songs = pd.read_csv('data/low_popularity_spotify_data.csv')


# song_analysis = pd.concat([high_pop_songs, low_pop_songs])
# song_analysis.drop_duplicates('id', inplace=True)


# tracks_df = dict_to_df(all_tracks)
# tracks_df['date'] = pd.json_normalize(tracks_df['album'])['release_date']
# new_tracks_df = tracks_df[['id', 'name', 'popularity', 'duration_ms', 'date']]


# tracks_all_analysis = new_tracks_df.merge(song_analysis, how='left', on='id')
# print(tracks_all_analysis)
# print(tracks_all_analysis['energy'].notnull().sum())


# Only 10% of the playlist has sound analysis data
# Would have then done clustering on the sound analysis to find groups of 'vibes' the playlist could split into




# But now using multiple datasets


def dict_to_df(dict):
    return pd.DataFrame.from_dict(dict, orient='columns')


def get_kaggle_data():
    kaggle_data = []
    for file in os.listdir("C:\\Users\\Josh\\OneDrive\\Documents\\PYTHON\\Project\\spotify\\data"):
        data = pd.read_csv(f"C:\\Users\\Josh\\OneDrive\\Documents\\PYTHON\\Project\\spotify\\data\\{file}")
        if 'id' not in data.columns:
            if 'track_id' in data.columns:
                data['id'] = data['track_id']
            else:
                data['id'] = data['spotify_id']
        
        data = data[['id', 'valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'mode']]
        kaggle_data.append(data)

    return kaggle_data


def join_data(kaggle_data, all_tracks):
    song_analysis = pd.concat(kaggle_data)
    song_analysis.drop_duplicates('id', inplace=True)

    tracks_df = dict_to_df(all_tracks)
    tracks_df['date'] = pd.json_normalize(tracks_df['album'])['release_date']
    tracks_df['year'] = tracks_df['date'].str.split('-').str[0]
    new_tracks_df = tracks_df[['id', 'name', 'popularity', 'duration_ms', 'year', 'uri']]

    tracks_all_analysis = new_tracks_df.merge(song_analysis, how='left', on='id')

    return tracks_all_analysis


# print(tracks_all_analysis)
# print(tracks_all_analysis['energy'].notnull().sum())

# Over 50% of my playlist songs have song analysis data now