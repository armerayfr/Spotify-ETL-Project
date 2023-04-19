import json
import requests
import datetime
from datetime import timedelta, datetime
import pandas as pd

curr_playlist_url = 'https://api.spotify.com/v1/me/player/recently-played'


def get_current_recently_played(access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        }

    today = datetime.now()
    # print('today=====', today)
    yesterday = today - timedelta(days=1)
    # print('yesterday=====', yesterday)
    '''request to API'''
    try:
        req = requests.get(curr_playlist_url, headers=headers)
    except:
        raise Exception(f'The spotify request went wrong')

    data = json.loads(req.text)
    # print(data)

    artists = []
    tracks = []
    played_at_list = []
    timestamp_list = []

    for song in data['items']:
        if yesterday.strftime('%Y-%m-%d') == song['played_at'][0:10]:
            artists.append(song['track']['album']['name'])
            tracks.append(song['track']['name'])
            played_at_list.append(song['played_at'])
            timestamp_list.append(song['played_at'][0:10])

    song_dict = {
        'song_name': tracks,
        'artist_name': artists,
        'played_at': played_at_list,
        'timestamp': timestamp_list
    }

    # SONG DATAFRAME
    song_df = pd.DataFrame(
        song_dict,
        columns=['song_name',
                 'artist_name',
                 'played_at',
                 'timestamp'
                 ]
        )

    return song_df