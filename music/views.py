from django.shortcuts import render
from .rainy_day import get_rainy_day_playlist
# Create your views here.


def home(request):
    return render(request, template_name='home.html')


def rainy_day(request):
    playlist = get_rainy_day_playlist()
    return render(
        request,
        template_name='music.html',
        context={
            'playlist': playlist
        })