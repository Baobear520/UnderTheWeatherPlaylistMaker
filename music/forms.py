from django import forms
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def validate(name):
    if len(name) <5:
        raise forms.ValidationError('Cannot be shorter than 5 symbols')
   

class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(max_length=64,validators=[validate])


