function showPage(pageId) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
        if (page.id === pageId) {
            page.classList.add('active');
        } else {
            page.classList.remove('active');
        }
    });
}
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    // Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const name = form.querySelector('input[name="name"]').value.trim();
            const email = form.querySelector('input[name="email"]').value.trim();
            const password = form.querySelector('input[name="password"]').value.trim();

            if (!name || !email || !password) {
                alert('All fields are required!');
                return;
            }

            if (!validateEmail(email)) {
                alert('Please enter a valid email address!');
                return;
            }

            form.submit();
        });
    });

    // Notification Dismissal
    const notifications = document.querySelectorAll('.notifications ul li');
    notifications.forEach(notification => {
        notification.addEventListener('click', () => {
            notification.style.display = 'none';
        });
    });

    // Email Validation Function
    function validateEmail(email) {
        const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return re.test(email);
    }
});
document.addEventListener('DOMContentLoaded', () => {
    showPage('dashboard');

    // Sample data for humidity and temperature
    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'Humidity (%)',
                data: [55, 50, 60, 65, 70, 75, 80, 85, 75, 70, 65, 60],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                yAxisID: 'y-axis-1',
            },
            {
                label: 'Temperature (°C)',
                data: [10, 12, 14, 16, 18, 20, 22, 24, 22, 20, 18, 16],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                yAxisID: 'y-axis-2',
            }
        ]
    };

    // Configuration options
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                'y-axis-1': {
                    type: 'linear',
                    position: 'left',
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Humidity (%)'
                    }
                },
                'y-axis-2': {
                    type: 'linear',
                    position: 'right',
                    ticks: {
                        beginAtZero: true,
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Temperature (°C)'
                    }
                }
            }
        }
    };

    // Render the chart
    const ctx = document.getElementById('humidityTemperatureChart').getContext('2d');
    new Chart(ctx, config);
});


// Render the chart
const ctx = document.getElementById('humidityTemperatureChart').getContext('2d');
const humidityTemperatureChart = new Chart(ctx, config);