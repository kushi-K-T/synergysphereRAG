const API_BASE = "";

async function refreshSystemStatus() {
    try {
        const res = await fetch(`${API_BASE}/system/status`);
        if (!res.ok) return;
        const data = await res.json();
        
        const ollamaEl = document.getElementById("st-ollama");
        if (ollamaEl) {
            ollamaEl.innerText = data.ollama.status || "unavailable";
            ollamaEl.style.color = data.ollama.status === "available" ? "#10b981" : "#ef4444";
        }
        
        const chunksEl = document.getElementById("st-chunks");
        if (chunksEl) chunksEl.innerText = data.vector_chunk_count;
        
        const extEl = document.getElementById("st-ext");
        if (extEl) extEl.innerText = data.external_ai.status;
        
        const mcpEl = document.getElementById("st-mcp");
        if (mcpEl) mcpEl.innerText = data.mcp.status;
        
        loadDocumentList();
    } catch (e) {
        console.error("Status check failed", e);
    }
}

async function loadDocumentList() {
    try {
        const res = await fetch(`${API_BASE}/documents`);
        const docs = await res.json();
        const listDiv = document.getElementById("doc-list");
        if (!listDiv) return;
        if (docs.length === 0) {
            listDiv.innerHTML = "<em>No private documents loaded.</em>";
            return;
        }
        listDiv.innerHTML = docs.map(d => `<div>?? ${d.filename} (${d.chunk_count} chunks)</div>`).join("");
    } catch (e) {
        console.error("Could not fetch documents", e);
    }
}

async function uploadDocument() {
    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) return alert("Select a file first.");
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const res = await fetch(`${API_BASE}/documents/upload`, { method: "POST", body: formData });
        if (res.ok) {
            alert("Uploaded and ingested successfully.");
            fileInput.value = "";
            refreshSystemStatus();
        } else {
            const err = await res.json();
            alert(`Upload failed: ${err.detail}`);
        }
    } catch (e) {
        alert("Upload error: " + e.message);
    }
}

async function triggerIngest() {
    try {
        const res = await fetch(`${API_BASE}/ingest`, { method: "POST" });
        if (res.ok) {
            alert("Ingestion complete.");
            refreshSystemStatus();
        }
    } catch (e) {
        alert("Ingest error: " + e.message);
    }
}

async function handleSend(e) {
    e.preventDefault();
    const input = document.getElementById("query-input");
    const query = input.value.trim();
    if (!query) return;

    appendMessage(query, "user-msg");
    input.value = "";

    const routeTag = document.getElementById("route-indicator");
    routeTag.className = "route-tag route-idle";
    routeTag.innerText = "Processing...";

    const sendBtn = document.getElementById("send-btn");
    if (sendBtn) sendBtn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({ detail: `HTTP ${res.status} error` }));
            appendMessage(`?? ${errData.detail || "Server error"}`, "bot-msg");
            routeTag.className = "route-tag route-idle";
            routeTag.innerText = "Failed";
            return;
        }

        const data = await res.json();
        
        if (data.route === "local") {
            routeTag.className = "route-tag route-local";
            routeTag.innerText = `Local AI (${data.model})`;
        } else {
            routeTag.className = "route-tag route-external";
            routeTag.innerText = `External AI (${data.model})`;
        }

        let content = data.answer;
        if (data.sources && data.sources.length > 0) {
            const sourceHtml = data.sources.map(s => `<span class="source-tag">?? ${s.filename} (p.${s.page})</span>`).join(" ");
            content += `<div class="sources-box"><strong>Sources Cited:</strong><br>${sourceHtml}</div>`;
        }

        appendMessage(content, "bot-msg", true);
        refreshSystemStatus();
    } catch (err) {
        routeTag.className = "route-tag route-idle";
        routeTag.innerText = "Error";
        appendMessage(`?? Request failed: ${err.message}`, "bot-msg");
    } finally {
        if (sendBtn) sendBtn.disabled = false;
    }
}

function appendMessage(text, className, isHtml = false) {
    const container = document.getElementById("messages-container");
    const div = document.createElement("div");
    div.className = `message ${className}`;
    if (isHtml) {
        div.innerHTML = text;
    } else {
        div.innerText = text;
    }
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

window.onload = () => {
    refreshSystemStatus();
    setInterval(refreshSystemStatus, 15000);
};
