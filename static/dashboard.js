// dashboard.js
const client = window.location.pathname.split("/").pop();

const filters = {
  range: "all", // all, month, week, yesterday
  sku: "",
  amount_description: "",
  marketplace: ""
};

function applyDateFilter(dateStr) {
  const today = new Date();
  let startDate = null;
  let endDate = today.toISOString().split("T")[0]; // siempre termina hoy

  if (filters.range === "yesterday") {
    const y = new Date();
    y.setDate(y.getDate() - 1);
    startDate = y.toISOString().split("T")[0];
    endDate = startDate;  // mismo día
  } else if (filters.range === "week") {
    const w = new Date();
    w.setDate(w.getDate() - 7);
    startDate = w.toISOString().split("T")[0];
  } else if (filters.range === "month") {
    const m = new Date();
    m.setMonth(m.getMonth() - 1);
    startDate = m.toISOString().split("T")[0];
  } else if (filters.range === "previous month") {
  const today = new Date();

  const start = new Date(today.getFullYear(), today.getMonth() - 1, 1); // día 1 del mes anterior
  const end = new Date(today.getFullYear(), today.getMonth(), 0);       // último día del mes anterior

  startDate = start.toISOString().split("T")[0];
  endDate = end.toISOString().split("T")[0];
  } else if (filters.range === "all") {
    return {};  // ✅ ¡Este es el truco!
  }
  // const endDate = today.toISOString().split("T")[0];
  return startDate ? { start_date: startDate, end_date: endDate } : {};
}





async function fetchAndRender() {
  const query = new URLSearchParams({
  ...applyDateFilter(),
  sku: filters.sku,
  amount_description: filters.amount_description,
  marketplace: filters.marketplace 
  });
const res = await fetch(`/api/data/${client}?${query}`);
  const data = await res.json();
  if (!Array.isArray(data)) return;

  const dateMap = {};
  data.forEach(row => {
    const rawDate = row.date;
    const d = new Date(rawDate);
    const amt = parseFloat(row.total || 0);
    const desc = (row.amount_description || "").toLowerCase();
    const sku = (row.sku || "").toLowerCase();
    const marketplace = (row.marketplace || "").toLowerCase();


    if (!applyDateFilter(rawDate)) return;
    if (filters.sku && !sku.includes(filters.sku.toLowerCase())) return;
    if (filters.amount_description && !desc.includes(filters.amount_description.toLowerCase())) return;
    if (filters.marketplace && !desc.includes(filters.marketplace.toLowerCase())) return;
    if (filters.marketplace && !marketplace.includes(filters.marketplace.toLowerCase())) return;


    const dateKey = d.toISOString().split("T")[0]; // yyyy-mm-dd


    if (!dateMap[dateKey]) {
      dateMap[dateKey] = { sales: 0, units: 0, ads: 0, profit: 0, refunds: 0 };
    }

    if (desc.includes("principal") || desc.includes("product")) {
      dateMap[dateKey].sales += amt;
      dateMap[dateKey].units += 1;
    } else if (desc.includes("advertising")) {
      dateMap[dateKey].ads += amt;
    } else if (desc.includes("refund")) {
      dateMap[dateKey].refunds += amt;
    }
  });

  let totalSales = 0, totalUnits = 0, totalAds = 0, totalRefunds = 0;
  Object.values(dateMap).forEach(day => {
    totalSales += day.sales;
    totalUnits += day.units;
    totalAds += day.ads;
    totalRefunds += day.refunds;
  });
  const profit = totalSales - totalAds - totalRefunds;
  const payout = totalSales - totalAds;

  document.getElementById("sales").textContent = `$${totalSales.toFixed(2)}`;
  document.getElementById("units").textContent = totalUnits;
  document.getElementById("ads").textContent = `$${totalAds.toFixed(2)}`;
  document.getElementById("refunds").textContent = `$${totalRefunds.toFixed(2)}`;
  document.getElementById("profit").textContent = `$${profit.toFixed(2)}`;
  document.getElementById("payout").textContent = `$${payout.toFixed(2)}`;

  const dates = Object.keys(dateMap).sort();
  const salesArr = dates.map(d => dateMap[d].sales);
  const unitsArr = dates.map(d => dateMap[d].units);
  const adsArr = dates.map(d => dateMap[d].ads);
  const profitArr = dates.map(d => dateMap[d].sales - dateMap[d].ads - dateMap[d].refunds);

  const layout = (title, color, bg) => ({
    title,
    autosize: true, 
    margin: { t: 10 },
    xaxis: { title: "Month" },
    yaxis: { title: "Amount" },
    plot_bgcolor: bg,
    paper_bgcolor: bg,
    font: { color: "#333" }
  });

  Plotly.newPlot("salesChart", [{ x: dates, y: salesArr, mode: "lines+markers", line: { color: "#16a34a" }, marker: { size: 15 }, name: "Sales" }], layout("", "#16a34a", "#ecfdf5"),{ responsive: true });
  Plotly.newPlot("unitsChart", [{ x: dates, y: unitsArr, mode: "lines+markers", line: { color: "#2563eb" }, marker: { size: 15 },name: "Units" }], layout("", "#2563eb", "#eff6ff"),{ responsive: true });
  Plotly.newPlot("profitChart", [{ x: dates, y: profitArr, mode: "lines+markers", line: { color: "#9333ea" }, marker: { size: 15 },name: "Profit" }], layout("", "#9333ea", "#f5f3ff"),{ responsive: true });
  Plotly.newPlot("adsChart", [{ x: dates, y: adsArr, mode: "lines+markers", line: { color: "#f87171" }, marker: { size: 15 },name: "Advertising" }], layout("", "#f87171", "#fef2f2"),{ responsive: true });
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("button[data-range]").forEach(btn => {
    btn.addEventListener("click", () => {
      filters.range = btn.dataset.range;
      fetchAndRender();
    });
  });
  const skuInput = document.getElementById("skuFilter");
  if (skuInput) skuInput.addEventListener("input", e => {
    filters.sku = e.target.value;
    fetchAndRender();
  });
  const descInput = document.getElementById("descFilter");
  if (descInput) descInput.addEventListener("input", e => {
    filters.amount_description = e.target.value;
    fetchAndRender();
  });
    const markInput = document.getElementById("markFilter");
  if (markInput) markInput.addEventListener("input", e => {
    filters.marketplace = e.target.value;
    fetchAndRender();
});

fetchAndRender();
});
