// ═══════════════════════════════════════════════════════
// js/rules.js — Pattern → Response Rule Set
// Rule-Based AI Chatbot · Internship Project
//
// Each rule has:
//   intent   — human-readable category name
//   patterns — array of RegExp tested against user input
//   responses— array of strings (or functions) to reply with
//              Functions receive the raw input string as argument.
// ═══════════════════════════════════════════════════════

const RULES = [

  // ── Greetings ───────────────────────────────────────
  {
    intent: 'Greeting',
    patterns: [
      /\b(hi|hello|hey|howdy|hiya|yo|sup|greetings|good\s*(morning|afternoon|evening|day))\b/
    ],
    responses: [
      'Hello! 👋 How can I help you today?',
      'Hey there! Great to see you. What\'s on your mind?',
      'Hi! I\'m ready to chat. What can I do for you?',
      'Greetings! Ask me anything — I\'m all ears 🤖',
    ]
  },

  // ── Farewells ───────────────────────────────────────
  {
    intent: 'Farewell',
    patterns: [
      /\b(bye|goodbye|see\s*you|later|farewell|take\s*care|cya|gotta\s*go|good\s*night)\b/
    ],
    responses: [
      'Goodbye! Come back anytime 👋',
      'See you later! It was great chatting with you 😊',
      'Bye! Take care and have an amazing day! 🌟',
      'Farewell! I\'ll be here whenever you need me 🤖',
    ]
  },

  // ── How are you ─────────────────────────────────────
  {
    intent: 'How are you',
    patterns: [
      /how\s*(are\s*you|r\s*u|you\s*doing|is\s*it\s*going|are\s*things)/,
      /\b(what'?s?\s*up|wassup|how\s*do\s*you\s*feel)\b/
    ],
    responses: [
      'I\'m doing great, thanks for asking! 😄 How about you?',
      'Feeling fantastic — all my circuits are firing perfectly! ⚡',
      'I\'m running at 100%! Ready to help with anything 🤖',
    ]
  },

  // ── Bot identity ─────────────────────────────────────
  {
    intent: 'Bot identity',
    patterns: [
      /\b(who|what)\s*(are\s*you|r\s*u|is\s*this|am\s*i\s*talking\s*to)/,
      /your\s*name/,
      /\bname\b.*\bbot\b|\bbot\b.*\bname\b/
    ],
    responses: [
      'I\'m a Rule-Based AI Chatbot 🤖 built with pure HTML, CSS, and JavaScript. I use pattern matching to understand your messages!',
      'My name is ChatBot AI. I\'m a rule-based system — I match your input against patterns and give the best response I can!',
    ]
  },

  // ── Capabilities / help ──────────────────────────────
  {
    intent: 'Capabilities',
    patterns: [
      /what\s*(can\s*you|do\s*you)\s*(do|know|help)/,
      /\b(help|commands|capabilities|features)\b/,
      /\/help/
    ],
    responses: [
      `Here's what I can do:\n\n` +
      `💬 Small talk & greetings\n` +
      `🧮 Math: "what is 12 * 8?"\n` +
      `🕐 Time & date queries\n` +
      `😄 Jokes & fun facts\n` +
      `🌡️ Unit conversions\n` +
      `💻 Programming Q&A\n` +
      `🌍 General knowledge\n\n` +
      `Commands: /help · /clear · /history`,
    ]
  },

  // ── Math ─────────────────────────────────────────────
  {
    intent: 'Math — multiplication',
    patterns: [ /(\d+(?:\.\d+)?)\s*[\*×x]\s*(\d+(?:\.\d+)?)/ ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)\s*[\*×x]\s*(\d+(?:\.\d+)?)/);
        return m ? `${m[1]} × ${m[2]} = **${parseFloat(m[1]) * parseFloat(m[2])}** 🧮` : 'Could not parse that.';
      }
    ]
  },
  {
    intent: 'Math — addition',
    patterns: [ /(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)/ ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)/);
        return m ? `${m[1]} + ${m[2]} = **${parseFloat(m[1]) + parseFloat(m[2])}** ➕` : 'Could not parse that.';
      }
    ]
  },
  {
    intent: 'Math — subtraction',
    patterns: [ /(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)/ ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)/);
        return m ? `${m[1]} - ${m[2]} = **${parseFloat(m[1]) - parseFloat(m[2])}** ➖` : 'Could not parse that.';
      }
    ]
  },
  {
    intent: 'Math — division',
    patterns: [ /(\d+(?:\.\d+)?)\s*[\/÷]\s*(\d+(?:\.\d+)?)/ ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)\s*[\/÷]\s*(\d+(?:\.\d+)?)/);
        if (!m) return 'Could not parse that.';
        if (parseFloat(m[2]) === 0) return 'Division by zero is undefined! 🚫';
        return `${m[1]} ÷ ${m[2]} = **${(parseFloat(m[1]) / parseFloat(m[2])).toFixed(4).replace(/\.?0+$/, '')}** ➗`;
      }
    ]
  },
  {
    intent: 'Math — percentage',
    patterns: [ /(\d+(?:\.\d+)?)\s*%\s*(of)\s*(\d+(?:\.\d+)?)/i ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)/i);
        return m ? `${m[1]}% of ${m[2]} = **${(parseFloat(m[1]) / 100 * parseFloat(m[2])).toFixed(2)}** 💯` : 'Could not parse that.';
      }
    ]
  },
  {
    intent: 'Math — square root',
    patterns: [ /sqrt|square\s*root\s*(of)?\s*(\d+)/ ],
    responses: [
      (input) => {
        const m = input.match(/(\d+)/);
        return m ? `√${m[1]} = **${Math.sqrt(parseInt(m[1])).toFixed(6).replace(/\.?0+$/, '')}** √` : 'Please provide a number!';
      }
    ]
  },

  // ── Date & Time ──────────────────────────────────────
  {
    intent: 'Current time',
    patterns: [ /\b(what|tell).*(time|clock)\b/, /current\s*time/, /time\s*is\s*it/ ],
    responses: [
      () => `The current time is **${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'})}** 🕐`
    ]
  },
  {
    intent: 'Current date',
    patterns: [ /\b(what|tell).*(date|day)\b/, /today'?s?\s*date/, /what\s*day\s*is\s*(it|today)/ ],
    responses: [
      () => {
        const now = new Date();
        const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
        return `Today is **${now.toLocaleDateString('en-US', opts)}** 📅`;
      }
    ]
  },
  {
    intent: 'Current year',
    patterns: [ /what\s*year/, /current\s*year/ ],
    responses: [
      () => `The current year is **${new Date().getFullYear()}** 🗓️`
    ]
  },

  // ── Jokes ─────────────────────────────────────────────
  {
    intent: 'Jokes',
    patterns: [ /\b(joke|funny|laugh|humor|pun)\b/, /tell\s*(me\s*)?(a\s*)?(joke|something\s*funny)/ ],
    responses: [
      'Why do programmers prefer dark mode? Because **light attracts bugs**! 🐛',
      'Why did the developer go broke? Because he used up all his **cache**! 💸',
      'Why do Java developers wear glasses? Because they **don\'t C#**! 👓',
      'How many programmers does it take to change a light bulb? **None** — that\'s a hardware problem! 💡',
      'Why is Python the best language? Because it has **great re-solutions**! 🐍',
      'What do you call a fake noodle? An **Impasta**! 🍝',
      'I told my computer I needed a break. Now it won\'t stop sending me **Kit-Kat ads**! 🍫',
    ]
  },

  // ── Fun facts ────────────────────────────────────────
  {
    intent: 'Fun facts',
    patterns: [ /\b(fun\s*fact|interesting|did\s*you\s*know|trivia|fact)\b/ ],
    responses: [
      '🌟 **Fun fact:** Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs that was still edible!',
      '🌟 **Fun fact:** A day on Venus is longer than a year on Venus — it rotates so slowly!',
      '🌟 **Fun fact:** The first computer bug was an **actual bug** — a moth found in a Harvard computer in 1947!',
      '🌟 **Fun fact:** Bananas are technically **berries**, but strawberries are not!',
      '🌟 **Fun fact:** There are more possible iterations of a game of chess than there are atoms in the observable universe!',
      '🌟 **Fun fact:** The average person walks **100,000 miles** in their lifetime — that\'s 4 times around the Earth!',
    ]
  },

  // ── Programming topics ────────────────────────────────
  {
    intent: 'Programming — Python',
    patterns: [ /\bpython\b/ ],
    responses: [
      'Python 🐍 is great for AI, data science, and web dev! Key features: readable syntax, huge library ecosystem, and excellent ML frameworks like TensorFlow & PyTorch.',
      'Python tip: Use list comprehensions for cleaner code!\n`result = [x**2 for x in range(10)]`',
    ]
  },
  {
    intent: 'Programming — JavaScript',
    patterns: [ /\bjavascript\b|\bjs\b/ ],
    responses: [
      'JavaScript is the language of the web! 🌐 It runs in every browser and on servers via Node.js. This very chatbot is built with it!',
      'JavaScript tip: Use `const` and `let` instead of `var` for better scoping!\n`const data = fetchAPI();`',
    ]
  },
  {
    intent: 'Programming — HTML/CSS',
    patterns: [ /\b(html|css)\b/ ],
    responses: [
      'HTML provides structure, CSS provides style! 🎨 Together they build everything you see on the web — including this chatbot UI!',
      'CSS tip: Use CSS variables (custom properties) for consistent theming:\n`:root { --accent: #4f6ef7; }`',
    ]
  },
  {
    intent: 'Programming — what to learn',
    patterns: [ /what\s*(should|to)\s*(i\s*)?(learn|study|start)/, /best\s*(language|tech|skill)/ ],
    responses: [
      'For beginners, I recommend:\n1️⃣ **HTML/CSS** — build web pages\n2️⃣ **JavaScript** — add interactivity\n3️⃣ **Python** — for AI & data science\n\nStart small, build projects, and be consistent! 💪',
    ]
  },

  // ── Weather ──────────────────────────────────────────
  {
    intent: 'Weather',
    patterns: [ /\b(weather|temperature|forecast|rain|sunny|cloudy|snow)\b/ ],
    responses: [
      'I don\'t have live weather data, but you can check **weather.com** or ask your device\'s assistant for current conditions! 🌤️',
      'For real-time weather, try Googling your city + "weather". I\'m a rule-based bot without internet access! 🌦️',
    ]
  },

  // ── Thanks ───────────────────────────────────────────
  {
    intent: 'Thanks',
    patterns: [ /\b(thanks|thank\s*you|thx|ty|cheers|appreciate)\b/ ],
    responses: [
      'You\'re very welcome! 😊 Happy to help!',
      'No problem at all! Let me know if you need anything else 🤖',
      'Anytime! That\'s what I\'m here for 🌟',
    ]
  },

  // ── Compliments ──────────────────────────────────────
  {
    intent: 'Compliment',
    patterns: [ /\b(good|great|awesome|amazing|excellent|smart|cool|nice|love\s*you)\b.*bot/, /you'?r?e?\s*(great|awesome|smart|cool|amazing)/ ],
    responses: [
      'Aw, thank you! You\'re making this bot blush! 😊🤖',
      'That\'s so kind of you! You\'re pretty awesome yourself! ⭐',
      'Thanks! Flattery will get you everywhere 😄',
    ]
  },

  // ── Age ───────────────────────────────────────────────
  {
    intent: 'Bot age',
    patterns: [ /how\s*(old|long).*(you|this\s*bot)/, /your\s*age/, /when.*created/, /when.*born/ ],
    responses: [
      'I was created as an internship project! Age in bot years is... complicated 🤖',
      'I\'m brand new! Just hatched from a code editor ✨',
    ]
  },

  // ── Unit conversion ───────────────────────────────────
  {
    intent: 'Convert km to miles',
    patterns: [ /(\d+(?:\.\d+)?)\s*km\s*(to\s*)?miles?/i ],
    responses: [
      (input) => {
        const m = input.match(/(\d+(?:\.\d+)?)/);
        return m ? `${m[1]} km = **${(parseFloat(m[1]) * 0.621371).toFixed(3)} miles** 🛣️` : 'Provide a number!';
      }
    ]
  },
  {
    intent: 'Convert Celsius to Fahrenheit',
    patterns: [ /(-?\d+(?:\.\d+)?)\s*(degrees?\s*)?c(elsius)?\s*(to\s*)?f(ahrenheit)?/i ],
    responses: [
      (input) => {
        const m = input.match(/(-?\d+(?:\.\d+)?)/);
        return m ? `${m[1]}°C = **${(parseFloat(m[1]) * 9/5 + 32).toFixed(1)}°F** 🌡️` : 'Provide a temperature!';
      }
    ]
  },

  // ── Favorite things ───────────────────────────────────
  {
    intent: 'Favorite color',
    patterns: [ /favo(u)?rite\s*colou?r/, /what\s*colou?r/ ],
    responses: [
      'My favorite color is **blue** — the same shade as my accent color! 💙',
      'Definitely **indigo blue** (#4f6ef7) — it\'s literally my brand color! 🎨',
    ]
  },
  {
    intent: 'Favorite food',
    patterns: [ /favo(u)?rite\s*food/, /what\s*(do\s*you\s*)?eat/ ],
    responses: [
      'As a bot I don\'t eat, but I\'d probably choose **data** — I find it very satisfying! 😄',
      'I run on electricity and logic, but I hear **pizza** is great for coding sessions! 🍕',
    ]
  },

  // ── Meaning of life ───────────────────────────────────
  {
    intent: 'Meaning of life',
    patterns: [ /meaning\s*(of\s*)?life/, /answer\s*(to\s*)?everything/, /\b42\b/ ],
    responses: [
      'The answer to life, the universe, and everything is **42** 🌌 (according to The Hitchhiker\'s Guide to the Galaxy!)',
    ]
  },

  // ── Insults / negative ────────────────────────────────
  {
    intent: 'Insult handling',
    patterns: [ /\b(stupid|dumb|idiot|useless|terrible|hate\s*you|awful|worst)\b/ ],
    responses: [
      'I\'m sorry to hear that! I\'m still learning and improving. How can I do better? 🙏',
      'That\'s fair feedback! Rule-based bots have limits, but I\'m doing my best 💪',
      'I understand your frustration. Try rephrasing your question — I might understand better! 😊',
    ]
  },

  // ── Boredom ───────────────────────────────────────────
  {
    intent: 'Boredom',
    patterns: [ /\b(bored|boring|nothing\s*to\s*do)\b/ ],
    responses: [
      'Bored? Let\'s play! Ask me a math question, request a joke, or ask me a fun fact! 🎮',
      'Try these: "Tell me a joke" · "What is 99 * 99?" · "Tell me a fun fact" 🌟',
    ]
  },

];
