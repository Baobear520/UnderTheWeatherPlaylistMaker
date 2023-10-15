from django.http import HttpResponseRedirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect, render
from .rainy_day import add_tracks,get_url

# Create your views here.

def home(request):
    return render(request, template_name='home.html')

def rainy_day(request):
    playlist = add_tracks()
    return render(
        request,
        template_name='music.html',
        context={
            'playlist': playlist
        })

def redirect_to_spotify(request):
        url = get_url()
        return redirect(url)