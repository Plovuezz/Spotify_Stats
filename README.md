# Spotify Stats Tracker
#### Video Demo:  (https://youtu.be/wVAGaUPBjBE)
#### Description:
Spotify Stats Tracker is a terminal-based Python application that lets users explore insights about their Spotify listening habits.

After securely logging in through the Spotify Web API, users can:

- View their top artists, tracks, and genres over different time ranges (short, medium, long term).
- Analyze their listening trends and preferences.
- Create playlists directly from their top tracks or selected genres.

The app is built using Python and the Spotipy library. It reads Spotify data through API calls, processes it, and interacts with users via command-line prompts.

To use the app, users must register a Spotify Developer application to obtain API credentials and add them to a `.env` file in the project root.

This tool is a great way to explore your Spotify activity and generate playlists based on your actual listening behavior — right from your terminal.

## You can get your API credentials here: https://developer.spotify.com/
#### Then change everything in .env
For redirect_url you can use http://127.0.0.1:8000/callback
+ You should not show others your secret and client_id


