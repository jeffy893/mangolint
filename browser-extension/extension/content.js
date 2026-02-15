const MIN_WORDS = 15;

// Track which elements have already had their "typing started" logged,
// so we only log once per focus session.
const activeInputs = new WeakSet();
// Track which elements already have a pending or completed query
const queriedInputs = new WeakSet();

// Attributes that suggest a non-prose field (form data, credentials, etc.)
const NON_PROSE_HINTS = [
  "search", "query", "email", "mail", "username", "user", "login",
  "password", "pass", "phone", "tel", "zip", "postal", "address",
  "street", "city", "state", "country", "url", "link", "code",
  "captcha", "otp", "token", "coupon", "promo", "amount", "price",
  "quantity", "number", "card", "cvv", "expir", "sort", "filter",
  "first.?name", "last.?name", "full.?name", "display.?name", "nick",
  "company", "org", "title", "subject", "tag",
];
const NON_PROSE_RE = new RegExp(NON_PROSE_HINTS.join("|"), "i");

// Attributes / context that suggest a prose composition field
const PROSE_HINTS = [
  "comment", "reply", "post", "message", "body", "content",
  "description", "bio", "about", "story", "note", "text",
  "compose", "editor", "write", "draft", "review", "feedback",
];
const PROSE_RE = new RegExp(PROSE_HINTS.join("|"), "i");

function getFieldSignature(el) {
  return [
    el.name, el.id, el.placeholder,
    el.getAttribute("aria-label"),
    el.getAttribute("data-testid"),
    el.className,
  ].filter(Boolean).join(" ");
}

function isProseField(el) {
  // Ignore all <input> elements — single-line fields are almost never prose
  if (el.tagName === "INPUT") return false;

  // contentEditable elements used as rich-text editors (e.g. social media, email composers)
  if (el.isContentEditable) {
    const sig = getFieldSignature(el);
    if (NON_PROSE_RE.test(sig)) return false;
    // Rich-text compose boxes are typically large; check the element or its
    // container for prose hints, otherwise accept if it has meaningful size
    if (PROSE_RE.test(sig)) return true;
    const closest = el.closest("[role='textbox'], [contenteditable='true']") || el;
    const closestSig = getFieldSignature(closest);
    if (PROSE_RE.test(closestSig)) return true;
    // Accept sizeable contentEditable regions (likely an editor)
    return closest.offsetHeight >= 80;
  }

  // <textarea> — check hints to exclude non-prose uses (code, address, etc.)
  if (el.tagName === "TEXTAREA") {
    const sig = getFieldSignature(el);
    if (NON_PROSE_RE.test(sig)) return false;
    if (PROSE_RE.test(sig)) return true;
    // Larger textareas without explicit hints are likely prose (comments, posts)
    return el.rows >= 3 || el.offsetHeight >= 80;
  }

  return false;
}

function getTextContent(el) {
  if (el.isContentEditable) return el.innerText || "";
  return el.value || "";
}

function wordCount(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

// ── Styles injected once ──
const STYLE_ID = "mangolint-styles";
function injectStyles() {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = STYLE_ID;
  style.textContent = `
    .mangolint-panel {
      position: absolute;
      padding: 10px 14px;
      background: #fdf6ec;
      border: 2px solid #d4c4a8;
      border-radius: 8px;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: 14px;
      line-height: 2;
      color: #2d2a24;
      box-shadow: 0 4px 16px rgba(0,0,0,0.15);
      z-index: 2147483647;
    }
    .mangolint-panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      font-size: 12px;
      color: #7a6a52;
    }
    .mangolint-close {
      cursor: pointer;
      background: none;
      border: none;
      font-size: 16px;
      color: #7a6a52;
      padding: 0 4px;
      line-height: 1;
    }
    .mangolint-close:hover { color: #2d2a24; }
    .mangolint-word-wrapper {
      position: relative;
      display: inline;
    }
    .mangolint-highlight {
      background: #ffe0a6;
      border-bottom: 2px solid #b35c00;
      padding: 2px 4px;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .mangolint-highlight:hover { background: #ffd080; }
    .mangolint-dropdown {
      display: none;
      position: absolute;
      left: 0;
      top: 100%;
      background: #fff;
      border: 1px solid #d4c4a8;
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.12);
      padding: 6px 0;
      z-index: 2147483647;
      min-width: 220px;
      white-space: normal;
    }
    .mangolint-dropdown.open { display: block; }
    .mangolint-dropdown-item {
      padding: 6px 12px;
      cursor: pointer;
      transition: background 0.1s;
    }
    .mangolint-dropdown-item:hover { background: #fdf0dc; }
    .mangolint-replacement-word {
      font-weight: 600;
      color: #b35c00;
    }
    .mangolint-replacement-lang {
      font-size: 11px;
      color: #7a6a52;
    }
    .mangolint-replacement-pronunciation {
      font-size: 11px;
      font-style: italic;
      color: #8a7a62;
    }
    .mangolint-replacement-explanation {
      font-size: 11px;
      color: #555;
      margin-top: 2px;
    }
    .mangolint-applied {
      color: #b35c00;
      font-weight: 600;
    }
  `;
  document.head.appendChild(style);
}

// ── Panel rendering ──

function esc(str) {
  const d = document.createElement("span");
  d.textContent = str;
  return d.innerHTML;
}

function removePanel(el) {
  const existing = el._mangolintPanel;
  if (existing && existing.parentNode) {
    existing.parentNode.removeChild(existing);
  }
  el._mangolintPanel = null;
}

function replaceWordInField(el, original, replacement) {
  const escaped = original.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(escaped, "i");
  if (el.isContentEditable) {
    el.innerText = el.innerText.replace(re, replacement);
  } else {
    el.value = el.value.replace(re, replacement);
  }
}

function showSuggestions(el, text, suggestions) {
  injectStyles();
  removePanel(el);

  if (!suggestions.length) return;

  // Group suggestions by their lowercase original phrase
  const map = new Map();
  for (const s of suggestions) {
    const key = s.original.toLowerCase();
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(s);
  }

  // Build a regex that matches any original phrase (longest first to prefer multi-word)
  const originals = [...map.keys()].sort((a, b) => b.length - a.length);
  const escaped = originals.map((o) => o.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const matchRe = new RegExp(`(${escaped.join("|")})`, "gi");

  // Split text into alternating plain / matched segments
  let html = "";
  let lastIndex = 0;
  for (const m of text.matchAll(matchRe)) {
    const matchStart = m.index;
    const matched = m[0];
    // Append any plain text before this match
    if (matchStart > lastIndex) {
      html += esc(text.slice(lastIndex, matchStart));
    }
    const items = map.get(matched.toLowerCase());
    const id = "ml-" + Math.random().toString(36).slice(2, 8);
    let dropHtml = `<div class="mangolint-dropdown" id="${id}">`;
    for (const item of items) {
      dropHtml += `
        <div class="mangolint-dropdown-item"
             data-dropdown-id="${id}"
             data-replacement="${esc(item.replacement)}"
             data-original="${esc(item.original)}">
          <div>
            <span class="mangolint-replacement-word">${esc(item.replacement)}</span>
            <span class="mangolint-replacement-lang">(${esc(item.language)})</span>
          </div>
          ${item.pronunciation ? `<div class="mangolint-replacement-pronunciation">${esc(item.pronunciation)}</div>` : ""}
          <div class="mangolint-replacement-explanation">${esc(item.explanation)}</div>
        </div>`;
    }
    dropHtml += "</div>";
    html += `<span class="mangolint-word-wrapper"><span class="mangolint-highlight" data-dropdown-id="${id}">${esc(matched)}</span>${dropHtml}</span>`;
    lastIndex = matchStart + matched.length;
  }
  // Append any remaining plain text
  if (lastIndex < text.length) {
    html += esc(text.slice(lastIndex));
  }

  const panel = document.createElement("div");
  panel.className = "mangolint-panel";
  panel.innerHTML =
    `<div class="mangolint-panel-header"><span>MangoLint suggestions</span><button class="mangolint-close">&times;</button></div>` +
    html;

  // Close button
  panel.querySelector(".mangolint-close").addEventListener("click", () => removePanel(el));

  // Toggle dropdowns on highlight click
  panel.addEventListener("click", (e) => {
    const highlight = e.target.closest(".mangolint-highlight");
    if (highlight) {
      const ddId = highlight.dataset.dropdownId;
      panel.querySelectorAll(".mangolint-dropdown.open").forEach((d) => {
        if (d.id !== ddId) d.classList.remove("open");
      });
      document.getElementById(ddId).classList.toggle("open");
      e.stopPropagation();
      return;
    }

    // Apply replacement on dropdown item click
    const item = e.target.closest(".mangolint-dropdown-item");
    if (item) {
      const replacement = item.dataset.replacement;
      const original = item.dataset.original;
      replaceWordInField(el, original, replacement);
      // Replace the highlight in the panel with the applied word
      const wrapper = item.closest(".mangolint-word-wrapper");
      const applied = document.createElement("span");
      applied.className = "mangolint-applied";
      applied.textContent = replacement;
      wrapper.replaceWith(applied);
      e.stopPropagation();
    }
  });

  // Position panel below the text field, appended to body to escape stacking contexts
  document.body.appendChild(panel);
  const rect = el.getBoundingClientRect();
  panel.style.left = `${rect.left + window.scrollX}px`;
  panel.style.top = `${rect.bottom + window.scrollY + 4}px`;
  panel.style.width = `${rect.width}px`;
  el._mangolintPanel = panel;
}

// Close dropdowns when clicking outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".mangolint-word-wrapper")) {
    document.querySelectorAll(".mangolint-dropdown.open").forEach((d) => d.classList.remove("open"));
  }
});

// ── Server query ──

function querySuggestions(el) {
  const text = getTextContent(el);
  console.log("[MangoLint] Sending query:", text);

  chrome.runtime.sendMessage({ type: "suggest", text }, (resp) => {
    if (chrome.runtime.lastError) {
      console.error("[MangoLint] Message error:", chrome.runtime.lastError.message);
      return;
    }
    if (!resp.ok) {
      console.error("[MangoLint] Server error:", resp.error);
      return;
    }
    console.log("[MangoLint] Response:", resp.data);
    showSuggestions(el, text, resp.data.suggestions || []);
  });
}

// Debounce timers keyed by element
const debounceTimers = new WeakMap();

function handleInput(e) {
  const el = e.target;
  if (!isProseField(el)) return;

  if (!activeInputs.has(el)) {
    activeInputs.add(el);
    console.log("[MangoLint] User started typing in:", el.tagName, el);
  }

  // Clear any existing debounce timer for this element
  const prev = debounceTimers.get(el);
  if (prev) clearTimeout(prev);

  // Wait 4 seconds of inactivity, then query if threshold met
  if (!queriedInputs.has(el)) {
    debounceTimers.set(el, setTimeout(() => {
      debounceTimers.delete(el);
      if (!queriedInputs.has(el) && wordCount(getTextContent(el)) >= MIN_WORDS) {
        queriedInputs.add(el);
        querySuggestions(el);
      }
    }, 4000));
  }
}

function handleFocusOut(e) {
  const el = e.target;
  // Cancel pending timer
  const timer = debounceTimers.get(el);
  if (timer) {
    clearTimeout(timer);
    debounceTimers.delete(el);
  }
  // Reset tracking when the user leaves the field
  activeInputs.delete(el);
  queriedInputs.delete(el);
}

document.addEventListener("input", handleInput, true);
document.addEventListener("focusout", handleFocusOut, true);

console.log("[MangoLint] Content script loaded");
