// dashboard.js
const client = window.location.pathname.split("/").pop();

const filters = {
  range: "all", // all, month, week, yesterday
  sku: "",
  amount_description: ""
};

function applyDateFilter(dateStr) {
  const today = new Date();
  const d = new Date(dateStr);
  if (filters.range === "yesterday") {
    const y = new Date(today);
    y.setDate(today.getDate() - 1);
    return d.toDateString() === y.toDateString();
  } else if (filters.range === "week") {
    const w = new Date(today);
    w.setDate(today.getDate() - 7);
    return d >= w;
  } else if (filters.range === "month") {
    const m = new Date(today);
    m.setMonth(today.getMonth() - 1);
    return d >= m;
  }
  return true; // all
}

async function fetchAndRender() {
  const res = await fetch(`/api/data/${client}`);
  const data = await res.json();
  if (!Array.isArray(data)) return;

  const dateMap = {};
  data.forEach(row => {
    const rawDate = row.date;
    const d = new Date(rawDate);
    const amt = parseFloat(row.total || 0);
    const desc = (row.amount_description || "").toLowerCase();
    const sku = (row.sku || "").toLowerCase();

    if (!applyDateFilter(rawDate)) return;
    if (filters.sku && !sku.includes(filters.sku.toLowerCase())) return;
    if (filters.amount_description && !desc.includes(filters.amount_description.toLowerCase())) return;

    const dateKey = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`; // Agrupar por mes

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
    margin: { t: 30 },
    xaxis: { title: "Month" },
    yaxis: { title: "Amount" },
    plot_bgcolor: bg,
    paper_bgcolor: bg,
    font: { color: "#333" }
  });

  Plotly.newPlot("salesChart", [{ x: dates, y: salesArr, mode: "lines", line: { color: "#16a34a" }, name: "Sales" }], layout("", "#16a34a", "#ecfdf5"));
  Plotly.newPlot("unitsChart", [{ x: dates, y: unitsArr, mode: "lines", line: { color: "#2563eb" }, name: "Units" }], layout("", "#2563eb", "#eff6ff"));
  Plotly.newPlot("profitChart", [{ x: dates, y: profitArr, mode: "lines", line: { color: "#9333ea" }, name: "Profit" }], layout("", "#9333ea", "#f5f3ff"));
  Plotly.newPlot("adsChart", [{ x: dates, y: adsArr, mode: "lines", line: { color: "#f87171" }, name: "Advertising" }], layout("", "#f87171", "#fef2f2"));
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
});

fetchAndRender();
