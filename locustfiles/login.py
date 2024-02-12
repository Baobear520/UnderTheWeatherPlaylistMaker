import time
from random import uniform
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """A class for performance testing endpoints"""

    wait_time = between(1,5)

    @task(1)
    def authenticate(self):
        self.client.get("/authenticate",name='authenticate')

    @task(1)
    def login(self):
        self.client.get("/",name='login')

    @task(5)
    def login_success(self):
        self.client.get("/login/success",name='login-success')
    
    @task(5)
    def create_playlist(self):
        lat = str(uniform(0,180))
        lon = str(uniform(0,180))
        url = "/create-playlist/?lat=" + lat + "&" + lon
        self.client.get(url,name='create-playlist')
        time.sleep(5)
        self.client.post(url, json={"playlist_name":"name"},name='create-playlist/?lat=...&lon=...')

    @task(3)
    def create_playlist_success(self):
        self.client.get("/create-playlist/success",name='created')
        
    