document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('chat-messages');
    const logList = document.getElementById('log-list');

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerText = sender === 'user' ? 'U' : 'AI';

        const textDiv = document.createElement('div');
        textDiv.className = 'text';
        textDiv.innerHTML = text.replace(/\n/g, '<br>'); // Simple Markdown-ish

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(textDiv);

        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            appendMessage(data.response, 'bot');
            fetchLogs(); // Update logs after action
        } catch (e) {
            appendMessage("Error communicating with server.", 'bot');
        }
    }

    async function fetchLogs() {
        try {
            const response = await fetch('/api/logs');
            const data = await response.json();
            // Data is list of dicts
            logList.innerHTML = '';
            // Show latest first
            data.reverse().forEach(log => {
                const logDiv = document.createElement('div');
                logDiv.className = 'log-item';
                logDiv.innerHTML = `
                    <span class="time">${new Date(log.timestamp).toLocaleTimeString()}</span>
                    <span class="type">${log.event_type}</span>
                    <div class="details">${JSON.stringify(log.details)}</div>
                `;
                logList.appendChild(logDiv);
            });
        } catch (e) {
            console.error("Error fetching logs", e);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Poll logs every 5 seconds
    setInterval(fetchLogs, 5000);
    fetchLogs();
});
