const form = document.getElementById("trip-form");
const results = document.getElementById("results");
const statusEl = document.getElementById("status");
const submitButton = document.getElementById("submit-button");

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[ch]);
}

function renderPlan(plan, index) {
  const destination = escapeHtml(plan.destination || "Travel plan");
  const duration = escapeHtml(plan.duration_days ?? "N/A");
  const budget = escapeHtml(plan.budget || "N/A");
  const companions = escapeHtml(plan.companions || "N/A");
  const pace = escapeHtml(plan.pace || "N/A");
  const score = Number(plan.match_score || 0).toFixed(3);
  return `
    <article class="trip-card">
      <div class="trip-card-head">
        <div>
          <h3>${index + 1}. ${destination}</h3>
          <div class="meta">
            <span class="tag">${duration} days</span>
            <span class="tag">${budget} budget</span>
            <span class="tag">${companions}</span>
            <span class="tag">${pace} pace</span>
          </div>
        </div>
        <span class="score">Similarity ${score}</span>
      </div>
      <div class="trip-card-body">
        <h4>DAY-WISE ITINERARY</h4>
        <div class="plan-text">${escapeHtml(plan.daily_plan || "No daily plan is available in this record.")}</div>
        <h4>COMPLETE TRIP PLAN</h4>
        <div class="plan-text">${escapeHtml(plan.trip_plan || "No complete trip plan is available in this record.")}</div>
      </div>
    </article>`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  data.days = Number(data.days);
  submitButton.disabled = true;
  submitButton.innerHTML = "<span>Finding matching plans...</span><span>…</span>";
  statusEl.textContent = "Searching dataset";
  results.innerHTML = `<div class="empty-state"><h3>Finding your travel match</h3><p>The backend is loading the dataset and ranking candidate plans. First run may take longer.</p></div>`;

  try {
    const response = await fetch("http://127.0.0.1:5000/api/itinerary", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The API returned an error.");

    const notice = payload.notice ? `<div class="alert">${escapeHtml(payload.notice)}</div>` : "";
    results.innerHTML = notice + (payload.recommendations || []).map(renderPlan).join("");
    statusEl.textContent = `${payload.recommendations?.length || 0} plans found`;
    if (!payload.recommendations?.length) {
      results.innerHTML = `<div class="empty-state"><h3>No matching plans found</h3><p>Try a broader destination or select “Any” for more preferences.</p></div>`;
    }
  } catch (error) {
    statusEl.textContent = "Connection issue";
    results.innerHTML = `<div class="alert"><strong>Could not generate recommendations.</strong><br>${escapeHtml(error.message)}<br><br>Check that the backend is running at http://127.0.0.1:5000 and that dependencies/model downloads completed.</div>`;
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = "<span>Generate my itinerary</span><span>↗</span>";
  }
});
