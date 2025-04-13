// Date Filter Handler
document.getElementById('dateFilter').addEventListener('submit', function(e) {
  e.preventDefault();
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  loadAllCharts(startDate, endDate);
});

// Initialize charts with empty data
const charts = {
  timeSeries: createChart('timeSeriesChart', 'line', { visits: [], pageviews: [] }),
  devices: createChart('deviceChart', 'doughnut'),
  pages: createChart('pagesChart', 'bar')
};

function createChart(canvasId, type, initialData = {}) {
  const ctx = document.getElementById(canvasId);
  return new Chart(ctx, {
      type: type,
      data: getChartData(type, initialData),
      options: getChartOptions(type)
  });
}

function getChartData(type, data) {
  const base = {
      labels: [],
      datasets: [{
          label: '',
          data: [],
          backgroundColor: []
      }]
  };

  switch(type) {
      case 'line':
          return {
              labels: data.labels || [],
              datasets: [
                  {
                      label: 'Visits',
                      data: data.visits || [],
                      borderColor: 'rgb(75, 192, 192)',
                      tension: 0.1
                  },
                  {
                      label: 'Pageviews',
                      data: data.pageviews || [],
                      borderColor: 'rgb(255, 99, 132)',
                      tension: 0.1
                  }
              ]
          };
      case 'doughnut':
          return {
              labels: data.labels || [],
              datasets: [{
                  data: data.values || [],
                  backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#4bc0c0']
              }]
          };
      case 'bar':
          return {
              labels: data.labels || [],
              datasets: [{
                  label: 'Views',
                  data: data.values || [],
                  backgroundColor: '#4bc0c0'
              }]
          };
  }
}

function getChartOptions(type) {
  const common = {
      responsive: true,
      maintainAspectRatio: false
  };
  
  if (type === 'line') {
      return {
          ...common,
          scales: { y: { beginAtZero: true } }
      };
  }
  return common;
}

async function loadAllCharts(startDate, endDate) {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);

  const response = await fetch(`/visitors/api/visitors/stats/?${params}`);
  const data = await response.json();

  // Update metric cards
  document.getElementById('totalVisitors').textContent = data.time_series.reduce((acc, curr) => acc + curr.visits, 0);
  document.getElementById('avgPageViews').textContent = 
      (data.time_series.reduce((acc, curr) => acc + curr.pageviews, 0) / data.time_series.length || 0).toFixed(1);
  document.getElementById('uniqueDevices').textContent = data.devices.length;

  // Update charts
  updateChart(charts.timeSeries, 'line', {
      labels: data.time_series.map(d => d.date),
      visits: data.time_series.map(d => d.visits),
      pageviews: data.time_series.map(d => d.pageviews)
  });

  updateChart(charts.devices, 'doughnut', {
      labels: data.devices.map(d => d.device),
      values: data.devices.map(d => d.total)
  });

  updateChart(charts.pages, 'bar', {
      labels: data.top_pages.map(p => p.page),
      values: data.top_pages.map(p => p.views)
  });
}

function updateChart(chart, type, data) {
  chart.data = getChartData(type, data);
  chart.update();
}

// Initial load
loadAllCharts();