import spotipy.exceptions
from dotenv import load_dotenv
import os
import sys
from datetime import date
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def main():

    #Removing .cache File
    if os.path.exists(".cache"):
        os.remove(".cache")


    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")

    scopes = "user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"


    sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scopes))
    username = sp.current_user()
    print("\n\n")
    print(f"Hello, {username['display_name']}")
    print("\n\n")

    first_choice = True
    while True:
        if first_choice:
            choice = input("What do you like to see(songs, artists, genres, to exit type exit): ").strip().lower()
        else:
            choice = input("What else?(songs, artists, genres, to exit type exit): ").strip().lower()


        if choice == "songs":
            get_songs(sp)
            first_choice = False
        elif choice == "artists":
            get_artists(sp)
            first_choice = False
        elif choice == "genres":
            get_genres(sp)
            first_choice = False
        elif choice == "exit":
            sys.exit(0)
        else:
            print("Wrong input, please try smth from these (songs, artists, genres, exit)", end="\n\n")


def get_songs(sp):

    #Quantity of songs defining and check
    quantity = prompt_user("How many songs do you want to see (1-50): ",
                           retry_prompt = "Please type a valid number from 1 to 50: ",
                           numbers_range=[1, 50])


    #Period defining and check
    term = prompt_user("For what time period? (short - month, medium - 6 month, long - all time): ",
                           retry_prompt="Please type a correct term(short, medium, long): ",
                           valid_options=["short", "medium", "long"])
    term += "_term"


    #Creating list of song`s dicts
    try:
        tracks = sp.current_user_top_tracks(limit=quantity, time_range=term)
    except spotipy.SpotifyException as e:
        print(f"Spotify API error {e}")
        sys.exit(1)

    #Displaing songs
    print("\n\n")
    print(
        f"Top {quantity} songs for the last {term.replace('_term', '')} term:\n"
    )

    for index, item in enumerate(tracks['items'], start=1):
        # Get track URL from ID
        track_url = f"https://open.spotify.com/track/{item['id']}"
        print(f"{index}. {item['name']} - {item['artists'][0]['name']} - {track_url}")
    print("\n\n")


    #If the user wants to create playlist(default No)
    want_playlist = yes_no("Do you want to create playlist?: ", default=False)

    #Creating playlist Block
    if want_playlist:

        # Make playlist public or private(private by default)
        is_public = yes_no("Do you want to make it public?: ", default=False)


        #Playlist name and description
        user_id = sp.current_user()['id']
        today = date.today()
        playlist_name = f"My favorite songs for {today.strftime('%B %d')}"
        playlist_description = f"My favorite songs based on listening stats for {today.strftime('%B %d')}"

        #Creating empty playlist
        try:
            new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name,
                                                    description=playlist_description, public=is_public)
        except spotipy.SpotifyException as e:
            print("Spotify API error:", e)
            sys.exit(1)
        except Exception as e:
            print("Something went wrong:", e)
            return

        #Creating List of track uris
        track_uris = [track['uri'] for track in tracks['items']]


        #Adding tracks to playlist
        try:
            sp.playlist_add_items(playlist_id=new_playlist['id'], items=track_uris)
        except spotipy.SpotifyException as e:
            print("Spotify API error:", e)
            sys.exit(1)
        except Exception as e:
            print("Something went wrong:", e)
            return

        playlist_id = f"https://open.spotify.com/playlist/{new_playlist['id']}"
        print("\n\n")
        print(f"Playlist created successfully - {playlist_id}")
        print("\n\n")

    #No
    else:
        print("\n\n")


def get_artists(sp):

    # Quantity of artists defining and check
    quantity = prompt_user("How many artists do you want to see (1-50): ",
                           retry_prompt="Please type a valid number from 1 to 50: ",
                           numbers_range=[1, 50])


    # Period defining and check
    term = prompt_user("For what time period? (short - month, medium - 6 month, long - all time): ",
                       retry_prompt="Please type a correct term(short, medium, long): ",
                       valid_options=["short", "medium", "long"])
    term += "_term"


    #Creating List of artists dicts
    try:
        artists = sp.current_user_top_artists(limit=quantity, time_range=term)
    except spotipy.SpotifyException as e:
        print(f"Spotify API error {e}")
        sys.exit(1)


    #Displaing artists
    print("\n\n")
    print(
        f"Top {quantity} artists for the last {term.replace('_term', '')} term:\n"
    )

    for index, artist in enumerate(artists['items'], start=1):
        print(f"{index}. {artist['name']}", end="")
        if artist['genres']:
            print(f" - {artist['genres'][0]}", end="")

        # Get artist URL from ID
        artist_url = f"https://open.spotify.com/artist/{artist['id']}"
        print(f" - {artist_url}")
    print("\n\n")



def get_genres(sp):
    max_artists = 50
    max_playlist_results = 10

    # Quantity of genres defining and check
    quantity = prompt_user("How many genres do you want to see (1-20): ",
                           retry_prompt="Please type a valid number from 1 to 20: ",
                           numbers_range=[1, 20])


    # Period defining and check
    term = prompt_user("For what time period? (short - month, medium - 6 month, long - all time): ",
                       retry_prompt="Please type a correct term(short, medium, long): ",
                       valid_options=["short", "medium", "long"])
    term += "_term"


    # Creating List of artists dicts
    try:
        artists = sp.current_user_top_artists(limit=max_artists, time_range=term)
    except spotipy.SpotifyException as e:
        print(f"Spotify API error {e}")
        sys.exit(1)


    #Calculating genres and their overall percentage
    genres = []
    for artist in artists['items']:
        for genre in artist['genres']:
            found = False
            for g in genres:
                if g['name'] == genre:
                    g['value'] += 1
                    found = True
                    break
            if not found:
                g = {'name': genre, 'value': 1}
                genres.append(g)

    all_values = sum(g['value'] for g in genres)


    quantity = min(quantity, len(genres))


    #Displaying genres
    print(end="\n\n")
    print(
        f"Top {quantity} genres for the last {term.replace('_term', '')} term:\n"
    )

    genres = sorted(genres, key=lambda x: x['value'], reverse=True)

    for index, i in enumerate(range(quantity), start=1):
        print(f"{index}. {genres[i]['name']} - {genres[i]['value'] * 100 / all_values:.1f}%")
    print(end="\n\n")


    #If user wants playlist based on genre(default no)
    want_playlist = yes_no("Do you want to find playlist based on genre?: ", default=False)
    print("\n")

    if want_playlist:

        #Display recommended genres
        genres_list = []
        max_number = 0
        for i in range(len(genres)):
            if len(genres[i]['name']) > max_number:
                max_number = len(genres[i]['name'])
            genres_list.append(genres[i]['name'])



        count = 0
        for i in genres_list:
            if count == 2:
                print(i, " " * (max_number - len(i)), end="|\n", sep="")
                count = 0
                continue
            print(i, " " * (max_number - len(i)), end="| ", sep="")
            count += 1

        print('\n')


        wanted_genre = prompt_user("You may like something from listed above or you can try your genre: ")
        wanted_genre = wanted_genre.strip().lower()

        print('\n')

        #Search playlist based on genre
        try:
            results2 = sp.search(q=wanted_genre, type="playlist", limit=max_playlist_results)
        except spotipy.SpotifyException as e:
            print(f"Spotify API error {e}")
            return

        #Displaying playlist
        print(f"Results of searching for {wanted_genre} playlists: \n")

        for i in range(10):
            if results2['playlists']['items'][i] is not None:
                print(f"{results2['playlists']['items'][i]['external_urls']['spotify']} - "
                        f"{results2['playlists']['items'][i]['name']}")
        print("\n")



#S1mple yes or no function
def yes_no(prompt, default=None):
    while True:
        answer = input(prompt).strip().lower()
        if answer == "exit":
            sys.exit(0)
        elif answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        elif answer == "" and default is not None:
            return default
        else:
            print("Please answer yes or no.")




#Defining and check user answer
def prompt_user(prompt, retry_prompt=None, numbers_range=None, valid_options=None, can_exit=True):

    current_prompt = prompt

    while True:

        answer = input(current_prompt).strip()

        #User wants to exit
        if can_exit and answer.lower() == "exit":
            sys.exit(0)

        #Numeric answer
        if numbers_range:
            try:
                value = int(answer)
                if numbers_range[0] <= value <= numbers_range[1]:
                    return value
            except ValueError:
                pass

        #Option answer
        if valid_options:
            if answer.lower() in valid_options:
                return answer.lower()


        #If we dont need specific answer
        if numbers_range is None and valid_options is None:
            return answer


        if retry_prompt:
            current_prompt = retry_prompt



if __name__ == "__main__":
 main()

