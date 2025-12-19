document.addEventListener("DOMContentLoaded", () => {
  const FAQ_PATH = "/static/js/chatbot/faq.json";
  const STORAGE_KEY = "agg_chat_history_v1";
  const GREET_KEY = "agg_chat_greeted_v1";
  const TYPING_DURATION = 2000; // 2 segundos

  const container = document.getElementById("chatbot-container");
  if (!container) return;

  if (!container.querySelector(".chatbot-toggle")) {
    container.innerHTML = `
      <div class="chatbot-panel" aria-hidden="true">
        <div class="chatbot-header">
          <div class="title"><i class='bx bx-robot'></i><span>Asistente Aggregatum</span></div>
          <button class="close-btn" id="chatbot-close"><i class='bx bx-x'></i></button>
        </div>

        <div class="chatbot-messages" id="chatbot-messages"></div>

        <div class="chatbot-input-area">
          <input id="chatbot-input" class="chatbot-input" type="text" placeholder="Escribe tu pregunta...">
          <button id="chatbot-send" class="chatbot-send-btn"><i class='bx bx-send'></i></button>
        </div>
      </div>

      <button class="chatbot-toggle" id="chatbot-toggle">
        <i class='bx bx-chat'></i>
      </button>
    `;
  }

  /* Elementos */
  const panel = container.querySelector(".chatbot-panel");
  const toggleBtn = container.querySelector("#chatbot-toggle");
  const closeBtn = container.querySelector("#chatbot-close");
  const sendBtn = container.querySelector("#chatbot-send");
  const inputEl = container.querySelector("#chatbot-input");
  const messagesEl = container.querySelector("#chatbot-messages");

  /* Estado */
  let faqData = [];

  // Eliminar conversacion con sessionStorage
  let history = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "[]");
  let greeted = sessionStorage.getItem(GREET_KEY) === "1";

  let isTyping = false;

  /* Cargar FAQ */
  fetch(FAQ_PATH)
    .then((r) => r.json())
    .then((data) => {
      faqData = data;
      renderHistory();
    })
    .catch(() => console.warn("FAQ no disponible"));

  /* ========== EVENTOS ========== */

  toggleBtn.addEventListener("click", () =>
    panel.style.display === "flex" ? closePanel() : openPanel()
  );

  closeBtn.addEventListener("click", closePanel);

  sendBtn.addEventListener("click", handleSend);
  inputEl.addEventListener(
    "keypress",
    (e) => e.key === "Enter" && handleSend()
  );

  /* ========== APERTURA ========== */

  function openPanel() {
    panel.style.display = "flex";
    panel.setAttribute("aria-hidden", "false");
    inputEl.focus();

    if (!greeted) {
      const greet =
        getFAQById("saludo")?.response || "Hola, ¿en qué puedo ayudarte?";
      appendBot(greet, {
        welcome: true,
        suggestions: getFAQById("saludo")?.suggestions,
      });
      greeted = true;

      // CAMBIADO A sessionStorage
      sessionStorage.setItem(GREET_KEY, "1");
    }
  }

  function closePanel() {
    panel.style.display = "none";
    panel.setAttribute("aria-hidden", "true");
  }

  /* ========== ENVÍO ========== */

  function handleSend() {
    const text = inputEl.value.trim();
    if (!text || isTyping) return;

    appendUser(text);
    inputEl.value = "";

    showTyping();
    setTimeout(() => {
      hideTyping();
      const reply = computeReply(text);
      appendBot(reply.text, reply);
    }, TYPING_DURATION);
  }

  /* ========== HISTORIAL ========== */

  function renderHistory() {
    messagesEl.innerHTML = "";
    history.forEach((m) =>
      appendMessage(m.text, m.role, m.welcome, m.suggestions, false)
    );
    scrollToBottom();
  }

  function save(msg) {
    history.push(msg);

    // SessionStorage
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(-50)));
  }

  /* ========== MENSAJES ========== */

  function appendUser(text) {
    appendMessage(text, "user");
    save({ role: "user", text });
  }

  function appendBot(text, opts = {}) {
    appendMessage(text, "bot", opts.welcome, opts.suggestions);
    save({
      role: "bot",
      text,
      welcome: !!opts.welcome,
      suggestions: opts.suggestions || [],
    });
  }

  function appendMessage(
    text,
    role,
    welcome = false,
    suggestions = [],
    saveHist = true
  ) {
    const div = document.createElement("div");
    div.className = `msg ${role}` + (welcome ? " welcome" : "");
    div.textContent = text;

    if (suggestions?.length) {
      const wrap = document.createElement("div");
      wrap.className = "suggestions";

      suggestions.forEach((s) => {
        const chip = document.createElement("div");
        chip.className = "suggestion";
        chip.textContent = s;
        chip.onclick = () => {
          if (isTyping) return;
          appendUser(s);
          showTyping();
          setTimeout(() => {
            hideTyping();
            const r = computeReply(s);
            appendBot(r.text, r);
          }, TYPING_DURATION);
        };
        wrap.appendChild(chip);
      });

      div.appendChild(wrap);
    }

    messagesEl.appendChild(div);
    scrollToBottom();
  }

  /* ========== TYPING ========== */

  function showTyping() {
    if (isTyping || document.getElementById("typing-indicator")) return;

    isTyping = true;

    const div = document.createElement("div");
    div.id = "typing-indicator";
    div.className = "msg bot";
    div.innerHTML = `
      <div class="typing">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
      </div>`;
    messagesEl.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
    isTyping = false;
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  /* ========== RESPUESTAS ========== */

  function computeReply(text) {
    const norm = normalize(text);

    let best = { score: 0, item: null };
    for (const item of faqData) {
      let score = 0;

      item.keywords?.forEach((kw) => {
        const nkw = normalize(kw);
        if (norm === nkw) score += 3;
        else if (norm.includes(nkw)) score += 2;
      });

      if (item.id && norm.includes(item.id)) score += 1;

      if (score > best.score) best = { score, item };
    }

    if (best.item)
      return {
        text: best.item.response,
        suggestions: best.item.suggestions || [],
        action: best.item.action || null,
      };

    const fall = ["servicios", "productos", "proceso", "contacto", "ubicacion"];
    for (const f of fall) {
      if (norm.includes(f)) {
        const i = getFAQById(f);
        if (i)
          return {
            text: i.response,
            suggestions: i.suggestions || [],
            action: i.action || null,
          };
      }
    }

    const def = getFAQById("default");
    return {
      text: def?.response || "No entendí. ¿Deseas ver nuestros servicios?",
      suggestions: def?.suggestions || [],
    };
  }

  /* ========== UTILS ========== */

  function normalize(txt) {
    return txt
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function getFAQById(id) {
    return faqData.find((f) => f.id === id);
  }
});
