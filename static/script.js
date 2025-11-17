    // Dummy function for now
    function sendMessage() {
        const input = document.getElementById('msg');
        const chatBox = document.getElementById('chat-box');

        if (!input.value) return;
        const p = document.createElement('p');
        p.textContent = input.value;
        p.classList.add('message', 'self');
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;
        input.value = '';
    }

const socket = io();
let username = '';
let room = '';

// Join a room
function joinRoom() {
    username = document.getElementById('username').value;
    room = document.getElementById('room').value;
    if (!username || !room) return alert("Enter both username and room");
    socket.emit('join', {username, room});
}

// Listen for messages
socket.on('message', data => {
    const msgbox = document.getElementById("chat-box");
    const p = document.createElement("p");
    p.classList.add('message');

    // Check if message is from me or other
    if (typeof data === 'object') {
        p.textContent = data.msg;
        if (data.sender === username) {
            p.classList.add('self'); // my messages on right
        } else {
            p.classList.add('other'); // others messages on left
        }
    } else {
        // system message
        p.textContent = data;
        p.style.fontStyle = 'italic';
        p.style.textAlign = 'center';
    }

    msgbox.appendChild(p);
    msgbox.scrollTop = msgbox.scrollHeight; // auto scroll
});

// Send private message
function sendMessage() {
    const input = document.getElementById('msg');
    if (!room || !username) return alert("Join a room first!");
    const msg = input.value;
    if (!msg) return;
    socket.emit('private_message', {room, msg, sender: username});
    input.value = '';
}