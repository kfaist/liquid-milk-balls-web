const express = require("express");
const path = require("path");
const http = require("http");
const { WebSocketServer } = require("ws");

const PORT = process.env.PORT || 3000;
const app = express();

// Parse JSON bodies
app.use(express.json());

// Serve static site (index.html, css, js, etc.)
app.use(express.static(path.join(__dirname)));

// Health check for Railway
app.get("/healthz", (_req, res) => res.status(200).send("ok"));

// LiveKit token endpoint
const { requireAuth, joinRoom } = require("./server/api/join");
app.post("/api/join", requireAuth, joinRoom);

const server = http.createServer(app);

// WS on the *same* server/port at /ws
const wss = new WebSocketServer({ server, path: "/ws" });
wss.on("connection", (ws) => {
  const keepalive = setInterval(() => { try { ws.ping(); } catch {} }, 25000);
  ws.on("message", (msg) => {
    for (const client of wss.clients) {
      if (client !== ws && client.readyState === client.OPEN) {
        try { client.send(msg); } catch {}
      }
    }
  });
  ws.on("close", () => clearInterval(keepalive));
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`[server] HTTP+WS listening on :${PORT}`);
});