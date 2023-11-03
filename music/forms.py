from django import forms
from .user_data import get_all_playlists_names
class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(
        max_length=64, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the name here'
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
            all_playlists_names = get_all_playlists_names(self.sp)
            if playlist_name in all_playlists_names:
                raise forms.ValidationError('Playlist with this name already exists')
        
        return playlist_name



    



