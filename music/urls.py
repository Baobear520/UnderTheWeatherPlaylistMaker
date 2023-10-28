from django.urls import path
from . import views 


urlpatterns = [
    path('', view=views.login,name='login'),
    path('homepage',view=views.home_page,name='home page'),
    path('create-playlist/',view=views.create_playlist,name='create playlist'),
    path('create-playlist/success',view=views.created,name='created') 
    
]