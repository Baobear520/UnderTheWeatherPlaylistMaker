// main.js
document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.getElementById('success-message');
    const playlistForm = document.getElementById('playlist-form');
    const playlistNameInput = document.getElementById('playlist-name');
    const spotifyLink = document.getElementById('spotify-link');
    
    playlistForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const playlistName = playlistNameInput.value;
        
        // Perform an action to create the playlist here
        
        // Once the playlist is created, show the "Great!" message and enable the Spotify link
        successMessage.style.display = 'block';
        
        // Replace "#" with the actual Spotify link or leave it empty
        spotifyLink.href = "https://www.spotify.com/"; // Replace with the actual link
        spotifyLink.style.display = 'block';
    });
});
