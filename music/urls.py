import logging
from django.urls import path
from . import views 

logger = logging.getLogger(__name__)

urlpatterns = [
    path('', view=views.home_page,name='home'),
    path('login',view=views.test_login, name='login'),
    path('contacts',view=views.contacts,name='contacts'),
    path('about',view=views.about,name='about'),
    path('create-playlist/',view=views.create_playlist,name='create-playlist'),
    path('create-playlist/success',view=views.created,name='created') 
    
]