from django import forms
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Authorization
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        redirect_uri='http://localhost:8080',
        scope='playlist-modify-public'
    )
)

class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(
        max_length=64, 
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter the name here'}
        )
    )

    def clean_playlist_name(self):
        playlist_name = self.cleaned_data['playlist_name']
        
        # Server-side validation if the playlist name is unique
        all_playlists = sp.current_user_playlists()['items']
        all_playlists_names = [playlist['name'] for playlist in all_playlists]

        if playlist_name in all_playlists_names:
            raise forms.ValidationError('This name already exists')
        return playlist_name


        
    



