// ═══════════════════════════════════════════════════════
// js/chatbot.js — Core Engine & UI Logic
// Rule-Based AI Chatbot · Internship Project
// ═══════════════════════════════════════════════════════

'use strict';

// ── State ─────────────────────────────────────────────
const STATE = {
  history:    [],   // { role, text, time }
  msgCount:   0,
  isTyping:   false,
  theme:      'light',
};

// ── Keyword fallback map ──────────────────────────────
const KEYWORD_MAP = {
  python:        'Python 🐍 is a top choice for AI and data science! Great for beginners too.',
  javascript:    'JavaScript runs everywhere — in browsers and on servers via Node.js!',
  html:          'HTML is the skeleton of every website. Start there if you\'re new!',
  css:           'CSS makes things look beautiful! Flexbox and Grid are your best friends.',
  ai:            'Artificial Intelligence is amazing! This chatbot uses rule-based AI — no ML needed.',
  machine:       'Machine Learning is a branch of AI where systems learn from data. Very powerful!',
  chatbot:       'You\'re talking to one right now! 🤖 This chatbot uses pattern matching rules.',
  algorithm:     'Algorithms are step-by-step problem-solving instructions. The backbone of CS!',
  database:      'Databases store data. SQL (relational) and MongoDB (NoSQL) are popular choices.',
  api:           'APIs let programs talk to each other. REST and GraphQL are common styles.',
  internship:    'Internships are gold! Build real projects, network, and learn on the job 🚀',
  project:       'Projects like this chatbot are perfect for a portfolio. Keep building!',
  github:        'GitHub is where developers share code. Push your projects there — employers look!',
  vscode:        'VS Code is the most popular code editor! Extensions make it super powerful.',
  loop:          'Loops repeat code. `for` loops iterate a set number of times; `while` loops run until a condition is false.',
  array:         'Arrays hold ordered lists of values. In JS: `const arr = [1, 2, 3]`',
  function:      'Functions are reusable blocks of code. `function greet(name) { return "Hi " + name; }`',
  variable:      'Variables store data. Use `const` for fixed values and `let` for changing ones in JS.',
  object:        'Objects store key-value pairs. In JS: `const user = { name: "Alice", age: 25 }`',
};

// ── Fallback responses ────────────────────────────────
const FALLBACKS = [
  'Hmm, I\'m not sure about that one. Try /help to see what I can do! 🤔',
  'I didn\'t quite catch that. Could you rephrase it?',
  'That\'s outside my current rules, but I\'m always learning! Try asking something else.',
  'Interesting question! My pattern-matching engine doesn\'t cover that yet. Try /help 📋',
];

// ── Core engine: getResponse ──────────────────────────
function getResponse(raw) {
  const input = raw.trim();
  const lower  = input.toLowerCase();

  // ── Slash commands
  if (lower === '/help')    return buildHelp();
  if (lower === '/clear')   { setTimeout(clearChat, 50); return null; }
  if (lower === '/history') { setTimeout(() => showPanel('history'), 50); return 'Opening history panel… 📜'; }
  if (lower === '/rules')   { setTimeout(() => showPanel('rules'), 50);   return 'Opening rules panel… 📋'; }

  // ── Pattern match against RULES array (rules.js)
  for (const rule of RULES) {
    for (const pattern of rule.patterns) {
      if (pattern.test(lower)) {
        const pool = rule.responses;
        const pick  = pool[Math.floor(Math.random() * pool.length)];
        return typeof pick === 'function' ? pick(lower) : pick;
      }
    }
  }

  // ── Keyword fallback
  for (const [keyword, reply] of Object.entries(KEYWORD_MAP)) {
    if (lower.includes(keyword)) return reply;
  }

  // ── Default fallback
  return FALLBACKS[Math.floor(Math.random() * FALLBACKS.length)];
}

// ── Build help text ───────────────────────────────────
function buildHelp() {
  return (
    '🤖 Here\'s what I can do:\n\n' +
    '💬 Greetings & small talk\n' +
    '🧮 Math: "what is 12 * 8?", "sqrt 144", "25% of 200"\n' +
    '🕐 Time & date: "what time is it?", "what day is today?"\n' +
    '😄 Jokes: "tell me a joke"\n' +
    '🌟 Facts: "tell me a fun fact"\n' +
    '💻 Coding: ask about Python, JS, HTML, CSS…\n' +
    '🌡️ Conversions: "100 km to miles", "37 C to F"\n\n' +
    '⌨️ Commands:\n' +
    '  /help    — show this message\n' +
    '  /clear   — clear the chat\n' +
    '  /history — view conversation log\n' +
    '  /rules   — view all active rules'
  );
}

// ── Add message to chat ───────────────────────────────
function addMessage(text, role) {
  const container = document.getElementById('chat-messages');
  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const row = document.createElement('div');
  row.className = `msg-row ${role}`;

  // Format text: bold **text** and newlines
  const formatted = text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');

  row.innerHTML = `
    <div class="avatar">${role === 'bot' ? '🤖' : '👤'}</div>
    <div class="msg-meta">
      <div class="bubble">${formatted}</div>
      <div class="timestamp">${now}</div>
    </div>`;

  container.appendChild(row);
  container.scrollTop = container.scrollHeight;

  // Save to history
  STATE.history.push({ role, text, time: now });
  STATE.msgCount++;
  updateStatsBadge();
  refreshHistoryPanel();
}

// ── Typing indicator ──────────────────────────────────
function showTyping() {
  const container = document.getElementById('chat-messages');
  const row = document.createElement('div');
  row.className = 'msg-row bot';
  row.id = 'typing-row';
  row.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div class="typing-dots"><span></span><span></span><span></span></div>
    </div>`;
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}
function hideTyping() {
  const el = document.getElementById('typing-row');
  if (el) el.remove();
}

// ── Handle form submit ────────────────────────────────
function handleSend(event) {
  event.preventDefault();
  const inputEl = document.getElementById('user-input');
  const text = inputEl.value.trim();

  if (!text || STATE.isTyping) return;
  inputEl.value = '';

  addMessage(text, 'user');
  STATE.isTyping = true;

  // Realistic typing delay (600ms–1400ms)
  const delay = 600 + Math.random() * 800;
  showTyping();

  setTimeout(() => {
    hideTyping();
    const reply = getResponse(text);
    if (reply !== null) addMessage(reply, 'bot');
    STATE.isTyping = false;
  }, delay);
}

// ── Quick reply buttons ───────────────────────────────
function sendQuick(text) {
  const inputEl = document.getElementById('user-input');
  inputEl.value = text;
  document.querySelector('.input-form button[type="submit"]').click();
}

// ── Clear chat ────────────────────────────────────────
function clearChat() {
  document.getElementById('chat-messages').innerHTML = '';
  STATE.history.length = 0;
  STATE.msgCount = 0;
  updateStatsBadge();
  refreshHistoryPanel();
  initChat();
}

// ── Export chat ───────────────────────────────────────
function exportChat() {
  if (STATE.history.length === 0) {
    addMessage('No messages to export yet!', 'bot');
    return;
  }
  const lines = [
    '═══════════════════════════════════════',
    '  Rule-Based AI Chatbot — Chat History',
    `  Exported: ${new Date().toLocaleString()}`,
    '═══════════════════════════════════════',
    '',
    ...STATE.history.map(h => `[${h.time}] ${h.role.toUpperCase().padEnd(4)}: ${h.text}`),
    '',
    `Total messages: ${STATE.history.length}`,
  ];
  const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `chatbot-history-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(a.href);
  addMessage('Chat exported! Check your downloads folder 💾', 'bot');
}

// ── Theme toggle ──────────────────────────────────────
function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.dataset.theme === 'dark';
  html.dataset.theme = isDark ? 'light' : 'dark';
  STATE.theme = isDark ? 'light' : 'dark';
  document.getElementById('theme-toggle').textContent = isDark ? '🌙 Dark mode' : '☀️ Light mode';
}

// ── Panel navigation ──────────────────────────────────
function showPanel(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  const panel = document.getElementById(`panel-${name}`);
  if (panel) panel.classList.add('active');

  const navMap = { chat: 0, rules: 1, history: 2 };
  const idx = navMap[name];
  if (idx !== undefined) {
    const btns = document.querySelectorAll('.nav-btn');
    if (btns[idx]) btns[idx].classList.add('active');
  }
}

// ── Stats ─────────────────────────────────────────────
function updateStatsBadge() {
  const msgEl   = document.getElementById('stat-msgs');
  const rulesEl = document.getElementById('stat-rules');
  if (msgEl)   msgEl.textContent   = STATE.msgCount;
  if (rulesEl) rulesEl.textContent = RULES.length;
}

// ── Refresh history panel ─────────────────────────────
function refreshHistoryPanel() {
  const el = document.getElementById('history-list');
  if (!el) return;

  if (STATE.history.length === 0) {
    el.innerHTML = '<p style="color:var(--text-muted);font-size:13px;padding:8px 0">No messages yet. Start chatting!</p>';
    return;
  }

  el.innerHTML = [...STATE.history].reverse().map(h => `
    <div class="history-card">
      <span class="role-badge ${h.role}">${h.role === 'bot' ? '🤖 Bot' : '👤 You'}</span>
      <div class="msg-text">${h.text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}</div>
      <div class="msg-time">${h.time}</div>
    </div>`).join('');
}

// ── Render rules panel ────────────────────────────────
function renderRulesPanel() {
  const el = document.getElementById('rules-list');
  if (!el) return;

  el.innerHTML = RULES.map(rule => {
    const sampleResponse = rule.responses[0];
    const preview = typeof sampleResponse === 'function'
      ? '[Dynamic response based on input]'
      : sampleResponse.substring(0, 90) + (sampleResponse.length > 90 ? '…' : '');
    return `
      <div class="rule-card">
        <div class="intent">${rule.intent}</div>
        <div class="pattern">${rule.patterns[0].toString()}</div>
        <div class="sample">${preview}</div>
      </div>`;
  }).join('');
}

// ── Welcome message ───────────────────────────────────
function initChat() {
  const container = document.getElementById('chat-messages');

  // Welcome banner as a special message
  const row = document.createElement('div');
  row.className = 'msg-row bot';
  row.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="msg-meta">
      <div class="bubble welcome-banner">
        <strong>👋 Welcome to Rule-Based AI Chatbot!</strong><br><br>
        I understand natural language using <strong>pattern matching</strong> across
        <strong>${RULES.length} rules</strong>. I can answer questions, do math,
        tell jokes, share facts, and more.<br><br>
        Type <strong>/help</strong> to see all commands, or just say hi! 😊
      </div>
      <div class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
    </div>`;
  container.appendChild(row);
}

// ── Keyboard shortcuts ────────────────────────────────
document.addEventListener('keydown', (e) => {
  // Ctrl+K = focus input
  if (e.ctrlKey && e.key === 'k') {
    e.preventDefault();
    document.getElementById('user-input').focus();
  }
  // Escape = blur input
  if (e.key === 'Escape') {
    document.getElementById('user-input').blur();
  }
});

// ── Boot ──────────────────────────────────────────────
renderRulesPanel();
updateStatsBadge();
initChat();
