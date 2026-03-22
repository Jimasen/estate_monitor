const ws = new WebSocket(`ws://${location.host}/ws/tenant/status`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  const subDot = document.getElementById("subscription-dot");
  const rentDot = document.getElementById("rent-dot");

  updateDot(subDot, data.subscription);
  updateDot(rentDot, data.rent);
};

function updateDot(el, cfg) {
  el.className = "status-dot " + cfg.color;

  if (cfg.blink === "fast") el.classList.add("blink-fast");
  if (cfg.blink === "slow") el.classList.add("blink-slow");
}
