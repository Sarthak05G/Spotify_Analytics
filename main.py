import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "7b947ce0ea144f75995b8041d644d517"
client_secret = "9ca65631b5d245c786acf9e18379c4ad"

auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

sp = spotipy.Spotify(auth_manager=auth_manager)

results = sp.search(q="Arijit Singh", type="track", limit=5)

for track in results['tracks']['items']:
    print(track['name'])