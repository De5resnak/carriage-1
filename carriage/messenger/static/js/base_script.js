let usersData = [];


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function loadUserData() {
    return fetch('/api/users/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            usersData = data; // Сохраняем данные о пользователях
            console.log('User data loaded:', usersData);
        })
        .catch(error => {
            console.error('Error loading user data:', error);
        });
}
loadUserData();


function loadChatList() {
    fetch('/api/chats/')
        .then(response => response.json())
        .then(data => {

            const chatList = document.getElementById('chat-list');
            chatList.innerHTML = '';


            data.forEach(chat => {
                const chatItem = document.createElement('li');
                chatItem.textContent = chat.name;
                chatItem.setAttribute('data-chat-id', chat.id);
                chatList.appendChild(chatItem);
            });


            attachClickHandlers();
        })
        .catch(error => {
            console.error('Error loading chat list:', error);
        });
}

function attachClickHandlers() {
    const chatItems = document.querySelectorAll('#chat-list li');
    chatItems.forEach(chatItem => {
        chatItem.addEventListener('click', function () {
            const chatId = chatItem.getAttribute('data-chat-id');
            console.log('Chat clicked, ID:', chatId);
            document.body.setAttribute('data-chat-id', chatId);
            openChat(chatId);
        });
    });
}


function openChat(chatId) {
    fetch(`/api/chat/${chatId}/`)
        .then(response => response.json())
        .then(chat => {
            const chatPanel = document.querySelector('.chat-panel');
            chatPanel.innerHTML = '';

            const chatTitle = document.createElement('h3');
            chatTitle.textContent = chat.name;
            chatPanel.appendChild(chatTitle);

            const membersList = document.createElement('ul');
            chat.members.forEach(memberId => {
                const memberItem = document.createElement('li');
                const memberName = getUserNameById(memberId);
                memberItem.textContent = memberName;
                membersList.appendChild(memberItem);
            });
            chatPanel.appendChild(membersList);

            const messagesList = document.createElement('ul');
            chat.messages.forEach(message => {
                const messageItem = document.createElement('li');
                const senderName = getUserNameById(message.sender);
                messageItem.textContent = `${senderName}: ${message.text}`;
                messagesList.appendChild(messageItem);
            });
            chatPanel.appendChild(messagesList);
        })
        .catch(error => {
            console.error('Error loading chat details:', error);
        });
}


function loadChatDetails(chatId) {
    fetch(`/api/chat/${chatId}/`)
        .then(response => response.json())
        .then(chat => {
            const chatPanel = document.querySelector('.chat-panel');
            chatPanel.innerHTML = '';

            const chatTitle = document.createElement('h3');
            chatTitle.textContent = chat.name;
            chatPanel.appendChild(chatTitle);

            const messagesList = document.createElement('ul');
            chat.messages.forEach(message => {
                const messageItem = document.createElement('li');
                messageItem.textContent = `${message.sender_name}: ${message.text}`;
                messagesList.appendChild(messageItem);
            });
            chatPanel.appendChild(messagesList);
            loadUserData();
        })
        .catch(error => {
            console.error('Error loading chat details:', error);
        });
}


function sendMessage(messageText, chatId) {

    const csrftoken = getCookie('csrftoken');
    const messageData = {
        text: messageText
    };


    console.log('Sending message data:', messageData);
    fetch(`/api/chat/${chatId}/send-message/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(messageData)
    })
    .then(response => response.json())
    .then(data => {

        loadChatDetails(chatId);

    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}




loadChatList();


document.getElementById('message-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value.trim();
    const chatId = document.body.getAttribute('data-chat-id');
    console.log('Message text:', messageText);
    if (messageText !== '' && chatId) {
        sendMessage(messageText, chatId);
        messageInput.value = '';
    } else {
        console.error('Invalid message or chatId');
    }
});
function getUserNameById(userId) {
    const user = usersData.find(user => user.id === userId);
    if (user) {
        return user.name;
    } else {
        return "Unknown User";
    }
}


document.getElementById('create-chat-btn').addEventListener('click', function() {
    window.location.href = '/create-chat';
});