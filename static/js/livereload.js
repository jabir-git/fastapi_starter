// WebSocket for live reload
const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
const socket = new WebSocket(
  protocol + "//" + window.location.host + "/reload",
);
socket.onmessage = (event) => {
  if (event.data === "reload") window.location.reload();
};
