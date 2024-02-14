UnderTheWeather Spotify(c) playlist maker



This is a Django-based web application that generates personalized music playlists for users based on their preferences and real-time weather conditions. The app integrates with the Spotify API to access user's music preferences and create custom playlists.

Features:

User Authentication: Users get authenticated by Spotify authentication system, in my app users only grant access to their profile data.

Spotify Integration: Integration with Spotify API allows users to access their music libraries and create playlists.

Weather-based Recommendations: The app utilizes a smart algorithm that assosiates current weather conditions to the audio features of a track (danceability,loudnes,energy, valence, popularity) using Spotify metadata.

Dynamic Playlist Generation: Tracks for the playlists are dynamically generated once the location and weather data are obtained.

Celery Integration: Asynchronous task processing with Celery for fetching weather data and track search.

Redis as Message Broker and Cache Backend: Redis is used as the message broker for Celery and as a cache backend for Django.

Responsive UI: User-friendly interface implemented using Django templates, CSS Bootstrap and enhanced with JavaScript/jQuery for dynamic behavior.

Dockerized Deployment: Docker containers for easy deployment and scaling.

