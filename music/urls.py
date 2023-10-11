from django.urls import path
from . import views 


urlpatterns = [
    path('',view=views.home),
    path('playlist/',view=views.rainy_day),
]