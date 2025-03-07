Spotify Playlist Creator 🎶
Spotify Playlist Creator is a Python-based application that allows you to automatically generate Spotify playlists based on your listening history from Last.fm. With a modern and user-friendly interface, this tool lets you select a time period (last day, last week, last 4 weeks, or last year), choose the number of tracks, and create a playlist in your Spotify account with just a few clicks. Additionally, it displays the currently playing track on Spotify in real-time.

This project is perfect for music enthusiasts who want to organize their favorite tracks into playlists effortlessly. It integrates with the Spotify API and Last.fm API to provide a seamless experience.

Features ✨
Automatic Playlist Creation: Generate Spotify playlists based on your Last.fm listening history.

Customizable Time Periods: Choose from:

Last day

Last week

Last 4 weeks

Last year

Track Limit: Set a limit for the number of songs in your playlist.

Real-Time Track Display: See what’s currently playing on Spotify directly in the app.

Modern UI: Built with CustomTkinter for a sleek and intuitive interface.

Easy to Use: Simple and straightforward workflow.

How It Works 🛠️
Authentication: Log in to your Spotify account via OAuth2.

Select Period and Limit: Choose a time period and set the maximum number of tracks for your playlist.

Fetch Tracks: The app retrieves your most-listened tracks from Last.fm.

Create Playlist: The tracks are added to a new playlist in your Spotify account.

Real-Time Updates: The app displays the currently playing track on Spotify.

Technologies Used 💻
Python: Core programming language.

Spotify API: For playlist creation and fetching currently playing tracks.

Last.fm API: For retrieving listening history.

CustomTkinter: For building a modern and responsive user interface.

Threading: For real-time updates without blocking the UI.

Installation 🚀
Clone the repository:

bash
Copy
git clone https://github.com/kalelwz/spotify.py
cd spotify.py
Install the required dependencies:

bash
Copy
pip install -r requirements.txt
Set up your API credentials:

Obtain a Last.fm API key from Last.fm API.

Obtain a Spotify Client ID and Secret from the Spotify Developer Dashboard.

Replace the placeholders in the code with your credentials.

Run the application:

bash
Copy
python spotify.py
Screenshots 📸
Screenshot 1
Main interface with period selection and track limit.

Screenshot 2
Playlist created successfully in Spotify.

Contributing 🤝
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

License 📄
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments 🙏
Spotify for their amazing API.

Last.fm for providing listening history data.

CustomTkinter for the beautiful UI components.

Enjoy creating playlists and reliving your favorite music moments! 🎧

Feel free to customize this description further to match your style! 😊
