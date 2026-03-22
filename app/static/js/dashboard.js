const ws = new WebSocket(
  (location.protocol === "https:" ? "wss://" : "ws://") +
  window.location.host +
  "/api/payments/ws/dashboard"
);

ws.onmessage = function (event) {
  const payment = JSON.parse(event.data);
  const table = document.querySelector(".rent-table tbody");
  if (!table) return;

  let row = table.querySelector(`tr[data-id='${payment.id}']`);

  if (row) {
    row.className = "status-" + payment.color;
    row.querySelector(".badge").innerText = payment.status.toUpperCase();
    row.querySelector(".badge").className = "badge " + payment.color;

    row.cells[3].innerText = "₦" + payment.amount_due.toLocaleString();
    row.cells[4].innerText = "₦" + payment.amount_paid.toLocaleString();
    row.cells[5].innerText = payment.due_date;
    row.cells[7].innerText = payment.agent_name || "-";
  } else {
    const newRow = table.insertRow();
    newRow.dataset.id = payment.id;
    newRow.className = "status-" + payment.color;
    newRow.innerHTML = `
      <td>${payment.tenant}</td>
      <td>${payment.phone || "-"}</td>
      <td>${payment.unit}</td>
      <td>₦${payment.amount_due.toLocaleString()}</td>
      <td>₦${payment.amount_paid.toLocaleString()}</td>
      <td>${payment.due_date}</td>
      <td><span class="badge ${payment.color}">
        ${payment.status.toUpperCase()}
      </span></td>
      <td>${payment.agent_name || "-"}</td>
    `;
  }
};
