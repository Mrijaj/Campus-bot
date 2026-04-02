let currentLanguage = 'English';

const languageGreetings = {
    'English': `नमस्ते! (Namaste!) <br> I am your campus bot. I can help you in multiple languages. <br> <strong>Quick Links:</strong>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm">💰 Fees</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm">📜 Scholarship</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm">📅 Timetable</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm">☎️ Help</button>
                </div>`,
    'Hindi': `नमस्ते! <br> मैं आपका कैंपस सहायक हूँ। मैं आपकी कई भाषाओं में मदद कर सकता हूँ। <br> <strong>त्वरित लिंक:</strong>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm">💰 शुल्क</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm">📜 छात्रवृत्ति</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm">📅 समय सारणी</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm">☎️ सहायता</button>
                </div>`,
    'Marathi': `नमस्कार! <br> मी आपला कॅम्पस सहाय्यक आहे. मी तुम्हाला अनेक भाषांमध्ये मदत करू शकतो। <br> <strong>द्रुत दुवे:</strong>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm">💰 शुल्क</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm">📜 शिष्यवृत्ती</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm">📅 वेळापत्रक</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm">☎️ मदत</button>
                </div>`,
    'Tamil': `வணக்கம்! <br> நான் உங்கள் வளாக உதவியாளர். நான் உங்களுக்கு பல மொழிகளில் உதவ முடியும். <br> <strong>விரைவான இணைப்புகள்:</strong>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm">💰 கட்டணம்</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm">📜 உதவித்தொகை</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm">📅 கால அட்டவணை</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm">☎️ உதவி</button>
                </div>`
};

/** Initialize theme and default greeting on load */
window.onload = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').innerHTML = '☀️ Light Mode';
    }
    addMessage('bot', languageGreetings['English']);
};

function toggleTheme() {
    const body = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    if (body.getAttribute('data-theme') === 'dark') {
        body.removeAttribute('data-theme');
        btn.innerHTML = '🌙 Dark Mode';
        localStorage.setItem('theme', 'light');
    } else {
        body.setAttribute('data-theme', 'dark');
        btn.innerHTML = '☀️ Light Mode';
        localStorage.setItem('theme', 'dark');
    }
}

function setLanguage(lang) {
    currentLanguage = lang;
    const chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML = '';

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.replace('btn-primary', 'btn-outline-secondary');
        if(btn.innerText.includes(lang)) {
            btn.classList.replace('btn-outline-secondary', 'btn-primary');
        }
    });

    document.getElementById('userQuery').placeholder = `Ask in ${lang}...`;
    addMessage('bot', languageGreetings[lang]);
}

function handleKey(e) { if (e.key === 'Enter') askBot(); }

function addMessage(type, content) {
    const chatWindow = document.getElementById('chat-window');
    const div = document.createElement('div');
    div.className = type === 'user' ? 'user-msg' : 'bot-msg';
    div.innerHTML = content;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return div;
}

function sendMenuQuery(topic) {
    if(topic === 'Contact Office') {
        addMessage("bot", "Please visit the Admin Office (Room 102) or call +91-141-270XXXX.");
        return;
    }
    document.getElementById('userQuery').value = `Inform me about ${topic}`;
    askBot();
}

async function askBot() {
    const queryInput = document.getElementById('userQuery');
    const query = queryInput.value.trim();
    if(!query) return;

    addMessage('user', query);
    queryInput.value = '';

    const typingDiv = addMessage('bot', '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>');

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: query, language: currentLanguage })
        });
        const data = await res.json();
        typingDiv.innerHTML = data.answer;
    } catch (err) {
        typingDiv.innerText = "Error: Campus server unreachable.";
    }
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
}