 # "Under The Weather" Spotify® Playlist Maker #

## Task
Develop a web application that generates Spotify playlists based on user preferences and current weather conditions. The app should include a simple frontend (markup and styles + weather widget) and a Django backend, support Spotify API authentication, have an algorithm for track selection, data caching, tests, and be deployed on a remote server using Docker Compose with CI/CD setup.

## Project Description
This web app helps Spotify users (both free and premium) create personalized playlists with tracks that match the weather conditions at their location.

**Playlist Formation**

Playlist formation is divided into 3 stages:

- **Analysis of User's Music Preferences and Extracting Popular Genres**

  The key parameter for creating Spotify's recommended playlists is "genre." While the user loads the homepage, the backend algorithm scans the most-listened-to artists and extracts the musical genres they belong to. It then determines the top 3 genres (e.g., "rock," "pop," "dance music"). To add some variety, the algorithm adds 2 random genres (like "k-pop" or "soundtrack") so that the user can discover something new. So, we have 5 genres to work with!

- **Fetching Weather Data by User's Location**

  The app will ask permission to get geolocation coordinates, allowing the backend algorithm to retrieve weather data from www.openweathermap.org.

- **Mapping Weather Data to Specific Audio Characteristics**

  Let’s say it’s raining, so you might feel a bit down and not want to listen to something too fast or loud (though this is subjective). The app will try to find tracks with low danceability, energy, loudness, and valence from the 5 selected genres, plus 10 tracks that have the word "rain" in their titles. Voilà! A playlist of 50 tracks is ready!

**Playlist Creation**

By the time the homepage fully loads with the welcome message for the authorized user and the playlist creation form, we already have a playlist of 50 tracks (this task was handled in the background by Celery). All that’s left is to enter the desired name for the playlist in the form field, and after validating the uniqueness of the name, the user will be redirected to a page with a playlist link (meaning that a playlist has already been created on Spotify with the chosen name and filled with the previously selected tracks).

**Playlist Listening**

After clicking the "Listen on Spotify" button, the user is redirected to www.spotify.com, directly to the page with the created playlist.

## Features
- **User Authentication**: Users authenticate via Spotify, granting access only to their profiles.
- **Spotify API Integration**: The app connects to the Spotify API, allowing users to view their music libraries and create playlists.
- **OpenWeather API Integration**: The app uses OpenWeather API to retrieve current weather data based on the user's location. This data is then used to generate playlists that match the current weather.
- **Weather-Based Recommendations**: An intelligent algorithm links current weather conditions with track characteristics (like danceability, loudness, energy, mood, popularity) from Spotify metadata.
- **Dynamic Playlist Generation**: Playlists are generated dynamically after fetching location and weather data.
- **Celery Integration**: Asynchronous task handling using Celery for fetching weather data and finding tracks.
- **Redis as Message Broker and Cache**: Redis is used as a message broker for Celery and as a caching system for Django.
- **Responsive Interface**: The app features a user-friendly interface implemented with Django templates, Bootstrap CSS, and JavaScript/jQuery for dynamic interactions.
- **Docker for Deployment**: The app is packaged in Docker containers for simplified deployment and scaling.

## Endpoints Overview
- `/` — Entry point (redirects to the authentication page or homepage).
- `/authenticate` — Handles user authentication via Spotify.
- `/login/success` — Successful authorization page.
- `/create-playlist/` — Page with a weather widget and form for creating a weather-based playlist (app's main page).
- `/create-playlist/success` — Page with a button linking to the Spotify playlist URL.
- `/contacts` — Contact information page.
- `/about` — App information page.

## Installation and Setup

### Requirements:
- Python 3.8+
- Django 4.0+
- Celery
- Redis
- Docker
- Spotify API
- OpenWeather API

### Installation Steps:
Clone the repository:

```
git clone https://github.com/YOUR-USERNAME/UnderTheWeatherPlaylistMaker.git
```
Switch to the project folder:

```
cd UnderTheWeatherPlaylistMaker
```
Set up a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

Install dependencies:

```
pip install -r requirements.txt
```
Set up environment variables for Spotify API authentication and OpenWeather API access. Create a .env file in the project root and add the following lines:

```
SPOTIFY_CLIENT_ID=<your-spotify-client-id>
SPOTIFY_CLIENT_SECRET=<your-spotify-client-secret>
SPOTIFY_REDIRECT_URI=<your-redirect-uri>
OPENWEATHER_API_KEY=<your-openweather-api-key>
```

Set up Redis and run it locally or via Docker:

```
docker run -p 6379:6379 redis
```

Start Celery:
```
celery -A config worker --loglevel=info
```
Run database migrations:

```
python manage.py migrate
```
Start the Django server:
```
python manage.py runserver
```

### Deployment in Docker ###

You can deploy the app in Docker by following these steps:

- Ensure you have Docker and Docker Compose installed.

- Build and start the containers:
```
docker compose up --build
```
## Testing ##

To run tests, use Django test runner:
```
python manage.py test
```

## Contacts ##

For questions or support, contact via email: admitry424@gmail.com
