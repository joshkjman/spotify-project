import requests


def get_top_5(token, type):
    url = f'https://api.spotify.com/v1/me/top/{type}?limit=5'
    headers = {'Authorization': 'Bearer ' + token}

    artists_tracks = []

    if type == 'artists':
        for item in requests.get(url, headers=headers).json()['items']:
            # names.append(item['name'])
            # images.append(item['images'][0]['url'])
            # spotify_uris.append(item['uri'])
            artists_tracks.append((item['name'], item['images'][0]['url'], item['uri']))

    
    elif type == 'tracks':
        for item in requests.get(url, headers=headers).json()['items']:
            # names.append(item['name'])
            # spotify_uris.append(item['uri'])
            artists_tracks.append((item['name'], item['uri']))

    return artists_tracks
