from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Join a room
@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} has joined the chat.", to=room)

# Private message to a room
@socketio.on('private_message')
def handle_private_message(data):
    room = data['room']
    msg = data['msg']
    sender = data['sender']
    # Send message to room
    send({'msg': msg, 'sender': sender}, to=room)

if __name__ == '__main__':
    socketio.run(app)
