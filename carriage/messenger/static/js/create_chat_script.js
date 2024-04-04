function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([\w-]+)/);
    return cookieValue ? cookieValue[1] : '';
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-chat-form').addEventListener('submit', function(event) {
        event.preventDefault();


        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok');
        })
        .then(data => {

            console.log('Chat created:', data);

            window.location.href = `/chat/${data.id}/`;
        })
        .catch(error => {
            console.error('Error creating chat:', error);
        });
    });
});