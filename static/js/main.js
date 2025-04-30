document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle search form submission
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const keyword = document.getElementById('search-input').value.trim();
            if (!keyword) {
                e.preventDefault();
                showAlert('Please enter a search term', 'warning');
            }
        });
    }

    // Handle time period selection for stock charts
    const periodSelectors = document.querySelectorAll('.period-selector');
    if (periodSelectors.length > 0) {
        periodSelectors.forEach(button => {
            button.addEventListener('click', function() {
                const symbol = this.getAttribute('data-symbol');
                const period = this.getAttribute('data-period');
                updateChart(symbol, period);
            });
        });
    }

    // Initialize stock detail chart if on stock detail page
    const chartContainer = document.getElementById('price-chart');
    if (chartContainer && window.historicalData) {
        createStockChart(window.historicalData);
        createVolumeChart(window.historicalData);
    }
});

// Update the chart when period changes
function updateChart(symbol, period) {
    // Show loading indicator
    document.getElementById('chart-loading').classList.remove('d-none');
    
    // Update active period button
    document.querySelectorAll('.period-selector').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-period') === period) {
            btn.classList.add('active');
        }
    });
    
    // Fetch new data for the selected period
    fetch(`/api/stock/${symbol}/data?period=${period}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update the chart with new data
            if (window.priceChart) {
                window.priceChart.destroy();
            }
            if (window.volumeChart) {
                window.volumeChart.destroy();
            }
            
            createStockChart(data);
            createVolumeChart(data);
            
            // Hide loading indicator
            document.getElementById('chart-loading').classList.add('d-none');
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
            showAlert('Failed to load chart data', 'danger');
            document.getElementById('chart-loading').classList.add('d-none');
        });
}

// Display alert/notification
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => {
            alertContainer.removeChild(alert);
        }, 150);
    }, 5000);
}
