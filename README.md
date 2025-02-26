
# Watch Party Web App

A simple watch party application that lets a host create a room, upload a movie, and have guests join via a six-digit room code. The host controls the video playback (play, pause, seek) and all connected guests see the synchronized video along with a real-time chat.

> **Note:**  
> This project allows direct uploads of various video formats. However, browsers natively support only a few formats (like MP4, WebM, and Ogg). For the best playback experience, please use a browser-compatible format.

## Features

- **Room-Based Watch Party:**  
  - **Host:** Creates a room, uploads a movie, and controls video playback.
  - **Guest:** Joins a room using a six-digit room code and watches the video in sync with the host.
  
- **Real-Time Video Synchronization:**  
  The host’s actions (play, pause, seek) are broadcast to all guests so that everyone is in sync.

- **Real-Time Chat:**  
  All users in the room can exchange messages in a live chat.

- **Modern Responsive UI:**  
  Built with modern CSS animations and a clean design.

## Project Structure
watch-party/ ├── app.py ├── requirements.txt ├── README.md ├── uploads/ # (Directory for uploaded movie files) ├── static/ │ ├── script.js # Client-side JavaScript for video sync and chat │ ├── styles.css # Styling for the application └── templates/ ├── index.html # Landing page: Create/Join Room ├── host.html # Host page: Room info & movie upload └── watch.html # Watch party page:Video player & chat


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Tejavani/Watch-Party
   cd watch-party
2.**INSTALL Dependencies:**
pip install -r requirements.txt

3.**run the application:**
python app.py



