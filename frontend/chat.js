// Configuration
const API_URL = "http://localhost:8000/api/chat";

// State
const history = [];

// DOM
const chat = document.getElementById("chat");
const form = document.getElementById("input-form");
const input = document.getElementById("message");

function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

async function sendMessage(text) {
    addMessage("user", text);
    history.push({ role: "user", content: text });

    const msgDiv = addMessage("assistant", "");
    msgDiv.classList.add("loading");

    input.disabled = true;
    form.querySelector("button").disabled = true;

    let fullText = "";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, history: history.slice(0, -1) }),
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        msgDiv.classList.remove("loading");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // Parse SSE events from buffer.
            const lines = buffer.split("\n");
            buffer = lines.pop(); // Keep incomplete line in buffer.

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue;
                const jsonStr = line.slice(6);
                try {
                    const event = JSON.parse(jsonStr);
                    if (event.type === "delta") {
                        fullText += event.text;
                        msgDiv.textContent = fullText;
                        chat.scrollTop = chat.scrollHeight;
                    } else if (event.type === "error") {
                        fullText += `\n[Error: ${event.message}]`;
                        msgDiv.textContent = fullText;
                    }
                } catch (e) {
                    // Skip malformed JSON.
                }
            }
        }

        if (!fullText) {
            msgDiv.textContent = "No response.";
        }
        history.push({ role: "assistant", content: fullText });
    } catch (err) {
        msgDiv.classList.remove("loading");
        msgDiv.textContent = `Error: ${err.message}`;
    } finally {
        input.disabled = false;
        form.querySelector("button").disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendMessage(text);
});
