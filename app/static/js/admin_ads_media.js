// app/static/js/admin_ads_media.js

async function loadPendingAds() {
  const res = await fetch("/api/admin/ads/pending");
  const ads = await res.json();

  const body = document.getElementById("ads-body");
  body.innerHTML = "";

  ads.forEach(ad => {
    const row = document.createElement("tr");
    row.dataset.id = ad.id;
    row.innerHTML = `
      <td>${ad.id}</td>
      <td>${ad.title}</td>
      <td>${ad.owner}</td>
      <td>
        <button onclick="approveAd(${ad.id})">Approve</button>
        <button onclick="rejectAd(${ad.id})">Reject</button>
      </td>
    `;
    body.appendChild(row);
  });
}

async function loadPendingMedia() {
  const res = await fetch("/api/admin/media/pending");
  const media = await res.json();

  const body = document.getElementById("media-body");
  body.innerHTML = "";

  media.forEach(m => {
    const row = document.createElement("tr");
    row.dataset.id = m.id;
    row.innerHTML = `
      <td>${m.id}</td>
      <td>${m.name}</td>
      <td>${m.uploader}</td>
      <td>
        <button onclick="approveMedia(${m.id})">Approve</button>
        <button onclick="rejectMedia(${m.id})">Reject</button>
      </td>
    `;
    body.appendChild(row);
  });
}

async function approveAd(id) {
  await fetch(`/api/admin/ads/${id}/approve`, { method: "POST" });
  loadPendingAds();
}

async function rejectAd(id) {
  await fetch(`/api/admin/ads/${id}/reject`, { method: "POST" });
  loadPendingAds();
}

async function approveMedia(id) {
  await fetch(`/api/admin/media/${id}/approve`, { method: "POST" });
  loadPendingMedia();
}

async function rejectMedia(id) {
  await fetch(`/api/admin/media/${id}/reject`, { method: "POST" });
  loadPendingMedia();
}

loadPendingAds();
loadPendingMedia();
