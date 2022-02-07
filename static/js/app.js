var config = {
    type: 'pie',
    data: {
      datasets: [{
        data: data,
        backgroundColor: [
        'rgba(255, 99, 132, 0.4)', 
        'rgba(54, 162, 235, 0.4)',
        'rgba(255, 206, 86, 0.4)',
        'rgba(153, 102, 255, 0.4)',
        'rgba(255, 159, 64, 1)'
        ],
        label: 'Population'
      }],
      labels: labels,
    },
    options: {
      responsive: true
    }
  };

  window.onload = function() {
    var ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
  };
