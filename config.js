(function () {
  const scheme = location.protocol === "https:" ? "wss" : "ws";
  // Same-origin WS endpoint; 443/80 implied, no explicit port needed.
  window.SIGNALING_SERVER_URL = `${scheme}://${location.host}/ws`;
})();