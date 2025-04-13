fetch('/visitors/api/visitors/', { credentials: 'include' })
  .then(response => response.json())
  .then(data => {
    const chartData = data.results || data;  // Handle pagination
    const ctx = document.getElementById('visitorsChart');
    
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.map(v => new Date(v.first_visited).toLocaleDateString()),
        datasets: [{
          label: 'Page Views',
          data: chartData.map(v => v.page_views),
          borderWidth: 1
        }]
      }
    });
  });