from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room, leave_room
import os  # Added for getting PORT from environment
import threading
import requests
import time  # for keep-alive ping

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)  # Keep your existing SocketIO setup

# ---------------- Keep-alive thread ----------------
def keep_alive():
    while True:
        try:
            requests.get("https://chatapp2-6.onrender.com")  # your app URL
        except:
            pass
        time.sleep(1 * 3600)  # every 1 hour

threading.Thread(target=keep_alive, daemon=True).start()
# ---------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


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
    send({'msg': f"{sender}: {msg}", 'sender': sender}, to=room)


if __name__ == '__main__':
    # Use Render's PORT environment variable if available
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
