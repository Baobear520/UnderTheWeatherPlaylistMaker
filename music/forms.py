from django import forms

class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(max_length=64)
