import requests
import json


def get_user_id(token):
    url = f'https://api.spotify.com/v1/me'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    return json.loads(response.content)['id']


def create_playlist_return_id(token, user_id, cluster):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    
    data = json.dumps({"name": f"Test Playlist {cluster}",
        "description": "Test playlist description",
        "public": False})
    
    response = requests.post(url, headers=headers, data=data).json()
    return response['id']


def add_songs_playlist(token, playlist_id, song_uris):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    
    data = json.dumps({'uris': song_uris,
                       'position':0})

    response = requests.post(url, headers=headers, data=data)
    return response