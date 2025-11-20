from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# --- Flood protection ---
user_last_msg = {}  # Tracks last message timestamp per user
connections_per_ip = {}  # Tracks connections per IP
MAX_CONNECTIONS_PER_IP = 5
MIN_MSG_INTERVAL = 0.5  # seconds between messages

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    ip = request.remote_addr
    connections_per_ip[ip] = connections_per_ip.get(ip, 0) + 1
    if connections_per_ip[ip] > MAX_CONNECTIONS_PER_IP:
        return False  # reject connection if too many per IP


@socketio.on('disconnect')
def handle_disconnect():
    ip = request.remote_addr
    connections_per_ip[ip] = max(connections_per_ip.get(ip, 1) - 1, 0)


@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} joined {room}.", to=room)


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f"{username} left {room}.", to=room)


@socketio.on('private_message')
def handle_private_message(data):
    room = data['room']
    msg = data['msg']
    sender = data['sender']
    now = time.time()

    # Flood protection: ignore messages sent too quickly
    if sender in user_last_msg and now - user_last_msg[sender] < MIN_MSG_INTERVAL:
        return
    user_last_msg[sender] = now

    send({'msg': f"{sender}: {msg}", 'sender': sender}, to=room)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
