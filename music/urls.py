from django.urls import path
from . import views 


urlpatterns = [
    path('',view=views.home),
    path('playlist/',view=views.rainy_day,name='playlist'),
    path('playlist/redirect-to-spotify',view=views.redirect_to_spotify),
]