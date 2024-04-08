#genius access token: TGwh02eoUW6GzZeSl4Ed5mfWM6WKz8PmJf9w40oRmHfDYFnrDGjBROgYe-Tyh476
#spotify client ID: 0e3323585eca4482a792eb98d357b2e7
#spotify client secret: a39fb145124b49ab9df5dda73cad6f5d
#uri: https://google.com


import os
import json
import time
import spotipy
import lyricsgenius as lg


os.environ["SPOTIPY_CLIENT_ID"] = '0e3323585eca4482a792eb98d357b2e7'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'a39fb145124b49ab9df5dda73cad6f5d'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://google.com'
os.environ["GENIUS_ACCESS_TOKEN"] = 'TGwh02eoUW6GzZeSl4Ed5mfWM6WKz8PmJf9w40oRmHfDYFnrDGjBROgYe'

spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
spotify_secret = os.environ['SPOTIPY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']

scope = 'user-read-currently-playing'

oauth_object = spotipy.SpotifyOAuth(client_id=spotify_client_id,
                                   client_secret=spotify_secret,
                                   redirect_uri=spotify_redirect_uri,
                                   scope=scope)

token_info = oauth_object.get_cached_token()
if not token_info:
    token_info = oauth_object.get_access_token(as_dict=False)
token = token_info['access_token']

spotify_object = spotipy.Spotify(auth=token)
genius_object = lg.Genius(genius_access_token)

# Initialize variables to store the previous song's title and artist
prev_song_title = None
prev_artist_name = None

while True:
    current_song = spotify_object.currently_playing()

    if current_song is not None:
        artist_name = current_song['item']['album']['artists'][0]['name']
        song_title = current_song['item']['name']

        if (song_title != prev_song_title) or (artist_name != prev_artist_name):
            print("\nCurrently playing:", artist_name, "-", song_title)

            song = genius_object.search_song(title=song_title, artist=artist_name)
            if song:
                lyrics = song.lyrics
                print(lyrics)
                print("\n ---> End of Lyrics! <----- \n")
            else:
                print("Lyrics not found for this song.")
            
            # Update the previous song's title and artist
            prev_song_title = song_title
            prev_artist_name = artist_name
    else:
        print("No song is currently playing.")
    
    # Wait for a few seconds before checking again
    time.sleep(15)  # Adjust the sleep duration as needed
