
// Handle Contact Form Submission
document.getElementById('contactForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch('/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Display the message to the user
        const messageDiv = document.getElementById('message-response');
        if (data.success) {
            messageDiv.textContent = data.message || 'Message sent successfully!';
            messageDiv.style.color = 'green'; // Success message in green
        } else {
            messageDiv.textContent = data.message || 'Message failed to send. Please try again.';
            messageDiv.style.color = 'red'; // Error message in red
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const messageDiv = document.getElementById('message-response');
        messageDiv.textContent = 'An error occurred. Please try again.';
        messageDiv.style.color = 'red'; // Error message in red
    });
});