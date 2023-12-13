import logging
from django.urls import path
from . import views 

logger = logging.getLogger(__name__)

urlpatterns = [
    path('',view=views.login, name='login'),
    path('login/success',view=views.login_success,name='login-success'),
    path('authenticate',view=views.authenticate, name='authenticate'),
    path('create-playlist/',view=views.create_playlist,name='create-playlist'),
    path('create-playlist/success',view=views.created,name='created'), 
    path('contacts',view=views.contacts,name='contacts'),
    path('about',view=views.about,name='about'),
]