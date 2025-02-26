// Connect to the Socket.IO server
const socket = io();

// The room code is the last segment of the URL
const room = window.location.pathname.split("/").pop();
socket.emit('join', { room: room });

// Determine if this client is the host by checking the URL query parameter
const urlParams = new URLSearchParams(window.location.search);
const isHost = urlParams.get('host') === 'true';

// Video synchronization
const video = document.getElementById('video-player');
if (video) {
  // If host, send sync events when video plays, pauses, or seeks
  if (isHost) {
    video.addEventListener('play', () => {
      socket.emit('sync', { room: room, action: 'play', time: video.currentTime });
    });
    video.addEventListener('pause', () => {
      socket.emit('sync', { room: room, action: 'pause', time: video.currentTime });
    });
    video.addEventListener('seeked', () => {
      socket.emit('sync', { room: room, action: 'seek', time: video.currentTime });
    });
  }
  
  // All clients listen for sync events and adjust playback (guests only)
  socket.on('sync', (data) => {
    if (!isHost) {
      // Adjust if time difference is more than 0.5 seconds
      if (Math.abs(video.currentTime - data.time) > 0.5) {
        video.currentTime = data.time;
      }
      if (data.action === 'play') {
        video.play();
      } else if (data.action === 'pause') {
        video.pause();
      } else if (data.action === 'seek') {
        video.currentTime = data.time;
      }
    }
  });
}

// Chat functionality
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', () => {
  const msg = chatInput.value.trim();
  if (msg !== '') {
    socket.emit('message', { room: room, msg: msg });
    addChatMessage('You: ' + msg);
    chatInput.value = '';
  }
});

socket.on('message', (data) => {
  addChatMessage(data.msg);
});

function addChatMessage(message) {
  const p = document.createElement('p');
  p.textContent = message;
  chatBox.appendChild(p);
  chatBox.scrollTop = chatBox.scrollHeight;
}
