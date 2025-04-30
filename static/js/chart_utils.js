// Create the stock price chart
function createStockChart(data) {
    if (!data || !data.dates || data.dates.length === 0) {
        console.warn('No chart data available');
        return;
    }
    
    const ctx = document.getElementById('price-chart').getContext('2d');
    
    // Calculate chart gradients
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(54, 162, 235, 0.7)');
    gradient.addColorStop(1, 'rgba(54, 162, 235, 0.1)');
    
    // Create chart
    window.priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Stock Price',
                data: data.prices,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHitRadius: 30,
                pointHoverBackgroundColor: 'rgba(54, 162, 235, 1)',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', {
                                    style: 'currency',
                                    currency: 'USD'
                                }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 10
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    position: 'right',
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.2)'
                    }
                }
            }
        }
    });
}

// Create the volume chart
function createVolumeChart(data) {
    if (!data || !data.dates || data.dates.length === 0) {
        console.warn('No volume data available');
        return;
    }
    
    const ctx = document.getElementById('volume-chart').getContext('2d');
    
    window.volumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Volume',
                data: data.volumes,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US').format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    position: 'right',
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) {
                                return (value / 1000000).toFixed(1) + 'M';
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'K';
                            }
                            return value;
                        }
                    },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.2)'
                    }
                }
            }
        }
    });
}

// Format currency values
function formatCurrency(value) {
    if (value === undefined || value === null || value === 'N/A') return 'N/A';
    
    // Parse the value to a float if it's a string
    const numValue = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]+/g, '')) : value;
    
    // Check if parsing resulted in a valid number
    if (isNaN(numValue)) return 'N/A';
    
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(numValue);
}

// Format large numbers with K, M, B, T suffixes
function formatLargeNumber(value) {
    if (value === undefined || value === null || value === 'N/A') return 'N/A';
    
    // Parse the value to a float if it's a string
    const numValue = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]+/g, '')) : value;
    
    // Check if parsing resulted in a valid number
    if (isNaN(numValue)) return 'N/A';
    
    if (numValue >= 1000000000000) {
        return (numValue / 1000000000000).toFixed(2) + 'T';
    } else if (numValue >= 1000000000) {
        return (numValue / 1000000000).toFixed(2) + 'B';
    } else if (numValue >= 1000000) {
        return (numValue / 1000000).toFixed(2) + 'M';
    } else if (numValue >= 1000) {
        return (numValue / 1000).toFixed(2) + 'K';
    }
    
    return numValue.toFixed(2);
}

// Format percentage values
function formatPercentage(value) {
    if (value === undefined || value === null || value === 'N/A') return 'N/A';
    
    // Parse the value to a float if it's a string
    let numValue = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]+/g, '')) : value;
    
    // Check if parsing resulted in a valid number
    if (isNaN(numValue)) return 'N/A';
    
    // Make sure the value is formatted as a percentage
    return numValue.toFixed(2) + '%';
}
