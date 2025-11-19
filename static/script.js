const socket = io();
let username = '';
let room = '';

function joinRoom() {
    username = document.getElementById('username').value;
    room = document.getElementById('room').value;
    if (!username || !room) return alert("Enter both username and room");
    socket.emit('join', {username, room});
}

socket.on('message', data => {
    const msgbox = document.getElementById("chat-box");
    const p = document.createElement("p");
    p.classList.add('message');

    if (typeof data === 'object') {
        p.textContent = data.msg;
        if (data.sender === username) {
            p.classList.add('self'); 
        } else {
            p.classList.add('other');
        }
    } else {
        p.textContent = data;
        p.style.fontStyle = 'italic';
        p.style.textAlign = 'center';
    }

    msgbox.appendChild(p);
    msgbox.scrollTop = msgbox.scrollHeight;
});


function sendMessage() {
    const input = document.getElementById('msg');
    if (!room || !username) return alert("Join a room first!");
    const msg = input.value;
    if (!msg) return;
    socket.emit('private_message', {room, msg, sender: username});
    input.value = '';
}