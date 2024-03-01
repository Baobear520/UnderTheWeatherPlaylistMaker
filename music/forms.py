from django import forms
from django.core.cache import cache
from .scripts.user_data import get_all_playlists_names
class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the name here',
            }
        )
    )
 
    def __init__(self, *args, **kwargs):
        # Pass the 'sp' object to the form's constructor
        self.sp = kwargs.pop('sp', None)
        super(PlaylistForm, self).__init__(*args, **kwargs)

    def clean_playlist_name(self):
        playlist_name = self.cleaned_data['playlist_name']
        if self.sp is not None:
            #Checking if the value is in cache
            all_playlists_names = cache.get('all_playlists_names')
            #Else making API call
            if not all_playlists_names:
                all_playlists_names = get_all_playlists_names(self.sp)
                #Storing the value in cache
                cache.set('all_playlists_names',all_playlists_names)
                
            # Check if the playlist name already exists
            if playlist_name in all_playlists_names:
                raise forms.ValidationError(
                    message='Playlist with this name already exists')
        return playlist_name



    



