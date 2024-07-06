document.addEventListener('DOMContentLoaded', (event) => {
    // Sample data for temperature chart
    const temperatureData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',],
        datasets: [{
            label: 'Temperature (°C)',
            data: [10, 12, 14, 16, 18, 20,],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
        }]
    };

    // Configuration for temperature chart
    const temperatureConfig = {
        type: 'line',
        data: temperatureData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                }
            }
        }
    };

    // Render the temperature chart
    const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(temperatureCtx, temperatureConfig);

    // Sample data for humidity chart
    const humidityData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',],
        datasets: [{
            label: 'Humidity (%)',
            data: [55, 50, 60, 65, 70, 75,],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
        }]
    };

    // Configuration for humidity chart
    const humidityConfig = {
        type: 'line',
        data: humidityData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    }
                }
            }
        }
    };

    // Render the humidity chart
    const humidityCtx = document.getElementById('humidityChart').getContext('2d');
    const humidityChart = new Chart(humidityCtx, humidityConfig);
});