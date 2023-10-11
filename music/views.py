from django.shortcuts import render,
from rainy_day import get_rainy_day_playlist
# Create your views here.
def rainy_day(request):
    playlist = get_rainy_day_playlist()
    return render(request,template_name='',context={playlist.items()})