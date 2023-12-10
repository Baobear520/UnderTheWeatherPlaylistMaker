from django.shortcuts import redirect, render
from spotipy import Spotify, DjangoSessionCacheHandler
from spotipy.oauth2 import SpotifyOAuth


# This will run every time before the view is loaded
# Make sure you enable this middleware in your settings.py


def is_user_authenticated(get_response):
    # Initialize request.code because we'll be using that in the login function in views.py
    def middleware(request):
        request.code = None
        if "authenticate" not in request.path:
            # If the current path is not /authenticate then we run this

            # In the function authenticate in views.py, we passed context["auth_url"] to
            # the html so the user can press the link and get sent to the spotify
            # authentication page, once they accept/refuse they will get redirected back
            # to / that the login function handles, but before that happens we must
            # capture the code that the authentication link gave us and put it in request.code
            if request.method == "GET" and request.GET.get("code"):
                request.code = request.GET.get("code")

            # This ensures that the token is valid aka not expired when every view loads
            if not request.code:
                cache_handler = DjangoSessionCacheHandler(request)
                auth_manager = SpotifyOAuth(
                    scope='user-library-read user-top-read playlist-modify-public',
                    cache_handler=cache_handler)
                if not auth_manager.validate_token(cache_handler.get_cached_token()):
                    return redirect("authenticate")

        response = get_response(request)
        return response

    return middleware