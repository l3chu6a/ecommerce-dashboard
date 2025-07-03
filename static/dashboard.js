// static/dashboard.js
function loadData() {
  const start_date = $('#start_date').val();
  const end_date = $('#end_date').val();
  const sku = $('#sku').val();
  const amount_description = $('#amount_description').val();

  $.getJSON(`/api/data/${client_id}`, {
    start_date,
    end_date,
    sku,
    amount_description
  }, function (data) {
    const dates = data.map(d => d.date);
    const totals = data.map(d => d.total);

    const skus = [...new Set(data.map(d => d.sku))];
    const descriptions = [...new Set(data.map(d => d.amount_description))];

    Plotly.newPlot('graph1', [{ x: dates, y: totals, type: 'bar' }], { title: 'Ventas Totales por Fecha' });
    Plotly.newPlot('graph2', [{ x: skus, y: skus.map(s => data.filter(d => d.sku === s).reduce((a, b) => a + b.total, 0)), type: 'bar' }], { title: 'Ventas por SKU' });
    Plotly.newPlot('graph3', [{ x: descriptions, y: descriptions.map(desc => data.filter(d => d.amount_description === desc).reduce((a, b) => a + b.total, 0)), type: 'bar' }], { title: 'Distribución por Amount Description' });
    Plotly.newPlot('graph4', [{ x: dates, y: totals, type: 'scatter' }], { title: 'Tendencia de Ventas en el Tiempo' });
  });
}

document.addEventListener('DOMContentLoaded', loadData);