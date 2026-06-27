# 🤖 Rule-Based AI Chatbot
**Internship Project · HTML · CSS · JavaScript**

A fully functional rule-based AI chatbot built with **zero dependencies** —
pure HTML, CSS, and Vanilla JavaScript. Runs in any browser via VS Code Live Server.

---

## 🚀 Quick Start

1. Open the folder in **VS Code**
2. Install the **Live Server** extension (if you don't have it)
3. Right-click `index.html` → **Open with Live Server**
4. Chat! 🎉

---

## 📁 Project Structure

```
rule-based-chatbot/
├── index.html          # Entry point + UI markup
├── css/
│   └── style.css       # Full styling + light/dark themes
├── js/
│   ├── rules.js        # All pattern → response rules
│   └── chatbot.js      # Engine, UI logic, commands
└── README.md
```

---

## ✨ Features

| Feature              | Details |
|----------------------|---------|
| Pattern matching     | Regex-powered intent detection |
| 30+ rules            | Greetings, math, time, jokes, facts, coding Q&A, unit conversion |
| Math engine          | +, -, ×, ÷, %, √ with dynamic computation |
| Typing animation     | Animated dots + realistic delay |
| Slash commands       | `/help`, `/clear`, `/history`, `/rules` |
| Quick reply buttons  | One-click common queries |
| Chat history panel   | Full session log, most-recent-first |
| Rules panel          | Inspect all active rules live |
| Export chat          | Download `.txt` conversation log |
| Light/Dark theme     | Toggle with one click |
| Keyboard shortcuts   | `Ctrl+K` to focus input |
| Responsive           | Works on mobile + desktop |
| Stats counters       | Live message & rule count in sidebar |

---

## 🧠 How It Works

```
User input → toLowerCase → Test against RULES patterns
                               ↓ match found
                           Pick random response from pool
                           (functions get the input to compute dynamic answers)
                               ↓ no match
                           Test KEYWORD_MAP
                               ↓ no match
                           Return random FALLBACK response
```

### Adding a new rule

Open `js/rules.js` and add an object to the `RULES` array:

```js
{
  intent: 'Greet in Spanish',
  patterns: [ /\b(hola|buenos\s*dias)\b/ ],
  responses: [
    '¡Hola! 👋 How can I help you?',
    '¡Buenos días! What can I do for you today?',
  ]
}
```

That's it — the engine picks it up automatically!

---

## 🛠️ Tech Stack

- **HTML5** — semantic structure
- **CSS3** — custom properties, flexbox, keyframe animations
- **Vanilla JS** — engine, DOM manipulation, state management

---

## 📊 Internship Deliverables

- [x] Rule-based NLP architecture
- [x] Professional UI with sidebar navigation
- [x] Light & dark theme support
- [x] Conversation history & export
- [x] Responsive design (mobile-friendly)
- [x] Extensible rules system
- [x] Zero external dependencies

---

*Built with ❤️ as an internship project*
