import requests
import json
from pprint import pprint
from urllib.parse import urlencode


# def get_token():
#     auth_string = client_id + ':' + client_secret
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')


#     url = 'https://accounts.spotify.com/api/token'
#     headers = {
#         'Authorization': 'Basic ' + auth_base64,
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
    
#     data = {'grant_type': 'client_credentials'}
#     result = requests.post(url, headers=headers, data=data)
#     token = result.json()["access_token"]
#     return token


def num_songs_playlist(token, playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}?market=gb&limit=10'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    return json.loads(response.content)['tracks']['total']


def get_playlist_items(token, playlist_id, offset):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?market=gb&offset={offset}'
    headers = {'Authorization': 'Bearer ' + token}
    result = requests.get(url, headers=headers)
    json_playlist = result.content

    dict_playlist = [song['track'] for song in json.loads(json_playlist)['items'] if song['track']]
    return dict_playlist


def playlist_songs(token, playlist_id):
    all_tracks = []

    total = num_songs_playlist(token, playlist_id)
    for n in range(0, total, 100):
        playlist = get_playlist_items(token, playlist_id, n)
        all_tracks.append(playlist)

    all_tracks = [t for track in all_tracks for t in track]
    return all_tracks