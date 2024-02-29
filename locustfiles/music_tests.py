import time
from random import uniform
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """A class for performance testing endpoints"""

    wait_time = between(3,6)

    @task
    def create_playlist_page(self):
        response = self.client.get("/create_playlist",name='create playlist')
        print(response.status_code)
        print(response.json())
        


        