let currentLanguage = 'English';

/** Rich HTML Greetings for each language */
const languageGreetings = {
    'English': `<strong>Welcome to Campus Support!</strong><br>
                I am your AI assistant. I can help you with documents, fees, and more.<br>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm menu-btn shadow-sm">💰 Fees</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm menu-btn shadow-sm">📜 Scholarship</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm menu-btn shadow-sm">📅 Timetable</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm menu-btn shadow-sm">☎️ Help</button>
                </div>`,
    'Hindi': `<strong>कैंपस सहायता में स्वागत है!</strong><br>
                मैं आपका AI सहायक हूँ। मैं शुल्क और अन्य जानकारियों में मदद कर सकता हूँ।<br>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm menu-btn">💰 शुल्क</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm menu-btn">📜 छात्रवृत्ति</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm menu-btn">📅 समय सारणी</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm menu-btn">☎️ सहायता</button>
                </div>`,
    'Marathi': `<strong>कॅम्पस सपोर्टमध्ये आपले स्वागत आहे!</strong><br>
                मी आपला AI सहाय्यक आहे. मी तुम्हाला फी आणि वेळापत्रकाबद्दल मदत करू शकतो.<br>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm menu-btn">💰 शुल्क</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm menu-btn">📜 शिष्यवृत्ती</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm menu-btn">📅 वेळापत्रक</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm menu-btn">☎️ मदत</button>
                </div>`,
    'Tamil': `<strong>வளாக ஆதரவிற்கு வரவேற்கிறோம்!</strong><br>
                நான் உங்கள் AI உதவியாளர். கட்டணம் மற்றும் பிற விவரங்களுக்கு நான் உதவ முடியும்.<br>
                <div class="menu-buttons">
                    <button onclick="sendMenuQuery('Fee Deadlines')" class="btn btn-outline-primary btn-sm menu-btn">💰 கட்டணம்</button>
                    <button onclick="sendMenuQuery('Scholarship')" class="btn btn-outline-primary btn-sm menu-btn">📜 உதவித்தொகை</button>
                    <button onclick="sendMenuQuery('Timetable')" class="btn btn-outline-primary btn-sm menu-btn">📅 கால அட்டவணை</button>
                    <button onclick="sendMenuQuery('Contact Office')" class="btn btn-outline-danger btn-sm menu-btn">☎️ உதவி</button>
                </div>`
};

window.onload = () => {
    const savedTheme = localStorage.getItem('theme');
    const themeBtn = document.getElementById('theme-toggle');

    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if(themeBtn) themeBtn.innerHTML = '☀️ Light Mode';
    }

    setLanguage('English');
};

function toggleTheme() {
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');

    if (root.getAttribute('data-theme') === 'dark') {
        root.removeAttribute('data-theme');
        btn.innerHTML = '🌙 Dark Mode';
        localStorage.setItem('theme', 'light');
    } else {
        root.setAttribute('data-theme', 'dark');
        btn.innerHTML = '☀️ Light Mode';
        localStorage.setItem('theme', 'dark');
    }
}

/** Resets chat and notifies server to pop session history */
async function resetChat() {
    if (!confirm("Are you sure you want to clear the chat history?")) return;

    try {
        const res = await fetch('/clear_chat', { method: 'POST' });
        if (res.ok) {
            const chatWindow = document.getElementById('chat-window');
            chatWindow.innerHTML = '';
            setLanguage(currentLanguage);
        }
    } catch (err) {
        console.error("Failed to clear chat:", err);
    }
}

function setLanguage(lang) {
    currentLanguage = lang;
    const chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML = '';

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-secondary');
        if(btn.innerText.trim() === lang || btn.getAttribute('onclick').includes(lang)) {
            btn.classList.replace('btn-outline-secondary', 'btn-primary');
        }
    });

    document.getElementById('userQuery').placeholder = `Ask in ${lang}...`;
    addMessage('bot', languageGreetings[lang]);
}

function addMessage(type, content) {
    const chatWindow = document.getElementById('chat-window');
    const div = document.createElement('div');
    div.className = type === 'user' ? 'user-msg' : 'bot-msg';
    div.innerHTML = content;
    chatWindow.appendChild(div);

    chatWindow.scrollTo({
        top: chatWindow.scrollHeight,
        behavior: 'smooth'
    });
    return div;
}

function sendMenuQuery(topic) {
    if(topic === 'Contact Office') {
        addMessage("bot", "🏢 <strong>Office Info:</strong><br>Room 102, Main Admin Block.<br>Phone: +91-141-270XXXX");
        return;
    }
    document.getElementById('userQuery').value = topic;
    askBot();
}

function handleKey(e) { if (e.key === 'Enter') askBot(); }

/** Robust Chat Request with Rate Limit Handling */
async function askBot() {
    const queryInput = document.getElementById('userQuery');
    const query = queryInput.value.trim();
    if(!query) return;

    addMessage('user', query);
    queryInput.value = '';

    const typingDiv = addMessage('bot', `
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `);

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: query,
                language: currentLanguage
            })
        });

        // Handle Rate Limiting (429) specifically
        if (res.status === 429) {
            typingDiv.innerHTML = `<span class="text-warning">⚠️ System Busy: Daily token limit reached. Please try again later.</span>`;
            return;
        }

        if (!res.ok) throw new Error('Server error');

        const data = await res.json();
        typingDiv.innerHTML = data.answer;

    } catch (err) {
        typingDiv.innerHTML = `<span class="text-danger">⚠️ Connection Error: Campus server is unreachable.</span>`;
    }

    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}