from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import os, random, string, uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to hold room data. Each room is a dict: { "movie": <filename> }
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-room')
def create_room():
    room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    rooms[room_code] = {"movie": None}
    return redirect(url_for('host_room', room_code=room_code))

@app.route('/host/<room_code>')
def host_room(room_code):
    if room_code not in rooms:
        return "Room not found", 404
    return render_template('host.html', room_code=room_code)

@app.route('/join-room', methods=['POST'])
def join_room_route():
    room_code = request.form.get('room_code', '').strip().upper()
    if room_code in rooms:
        return redirect(url_for('watch_party', room_code=room_code))
    else:
        return "Invalid Room Code", 400

@app.route('/upload-movie', methods=['POST'])
def upload_movie():
    room_code = request.form.get('room_code')
    if room_code not in rooms:
        return "Room not found", 404
    if 'movie' not in request.files:
        return "No file uploaded", 400
    file = request.files['movie']
    if file.filename == '':
        return "No file selected", 400
    # Accept any file type (no conversion, no restrictions)
    ext = os.path.splitext(file.filename)[1].lower()
    filename = room_code + "_" + str(uuid.uuid4()) + ext
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    rooms[room_code]['movie'] = filename
    # Redirect to the watch party page and mark the user as host via query parameter
    return redirect(url_for('watch_party', room_code=room_code, host='true'))

@app.route('/watch/<room_code>')
def watch_party(room_code):
    if room_code not in rooms:
        return "Room not found", 404
    movie = rooms[room_code]['movie']
    # Determine host status from the URL query parameter
    host = request.args.get('host', 'false').lower() == 'true'
    return render_template('watch.html', room_code=room_code, movie=movie, host=host)

@app.route('/video/<room_code>')
def serve_video(room_code):
    if room_code not in rooms or not rooms[room_code]['movie']:
        return "Video not found", 404
    filename = rooms[room_code]['movie']
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ------------------- Socket.IO Events ------------------- #

@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    join_room(room)
    emit('status', {'msg': f"A user has joined room {room}."}, room=room)

@socketio.on('sync')
def handle_sync(data):
    room = data.get('room')
    emit('sync', data, room=room, include_self=False)

@socketio.on('message')
def handle_message(data):
    room = data.get('room')
    msg = data.get('msg')
    emit('message', {'msg': msg}, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
