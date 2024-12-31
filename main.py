import os
import spotipy
from dotenv import load_dotenv
from ytmusicapi import YTMusic
from ytmusicapi.auth.oauth import OAuthCredentials
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

load_dotenv()

scope = ["user-library-read", "user-read-private"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

client_id = str(os.getenv('YTMUSIC_ID'))
client_secret = str(os.getenv('YTMUSIC_SECRET'))
ytmusic = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(client_id, client_secret))


def rate_track(video_id):
    ytmusic.rate_song(video_id, rating='INDIFFERENT')
    ytmusic.rate_song(video_id, rating='LIKE')


def search_music_youtube(name, artist):
    query = f'{name} - {artist}'
    search_results = ytmusic.search(query)
    video_id = ''
    for result in search_results:
        if 'videoId' in result.keys():
            video_id = result['videoId']
            break

    if video_id == '':
        return False

    rate_track(video_id)
    return True


def get_user_saved_track(offset):
    result = sp.current_user_saved_tracks(limit=1, offset=offset)
    return result['items'][0]['track']


def move_playlist_from_spotify_to_youtube(initial_offset, ordered=False):
    errors = 0
    idx = initial_offset

    while idx > 0:
        if errors > 10:
            print("Too many errors, stopping")
            break

        track = {}

        try:
            track = get_user_saved_track(idx)
            if track is None:
                break
        except:
            errors += 1
            print("\tAn exception occurred")
            sleep(5)
            continue

        artist = track['artists'][0]['name']
        name = track['name']
        searchAndLikeMusic = search_music_youtube(name, artist)

        if searchAndLikeMusic:
            print(f"Track {idx} - {artist} - {name} - OK")
        else:
            print(f"Track {idx} - {artist} - {name} - NOT FOUND")

        if ordered:
            idx += 1
        else:
            idx -= 1


move_playlist_from_spotify_to_youtube(1663)
