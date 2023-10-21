from django.urls import path
from . import views 


urlpatterns = [
    path('', view=views.login,name='login'),
    path('create-playlist/',view=views.create_playlist,name='create playlist') 
    
]