from django.shortcuts import render
from .rainy_day import add_tracks
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