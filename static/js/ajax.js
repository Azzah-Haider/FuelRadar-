// ============================================
// AJAX Functions for FuelRadar
// ============================================

// Get CSRF token from Django
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// ============================================
// 1. LIVE SEARCH - Instant Version
// ============================================

function performSearch() {
    const query = document.getElementById('searchInput')?.value || '';
    const city = document.getElementById('cityFilter')?.value || '';
    
    const url = `/stations/api/search/?q=${encodeURIComponent(query)}&city=${encodeURIComponent(city)}`;
    console.log('🔍 Searching:', url);
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('✅ Search results:', data);
            updateStationCardsInstant(data);
        })
        .catch(error => {
            console.error('❌ Search error:', error);
        });
}

function updateStationCardsInstant(data) {
    const container = document.getElementById('stationContainer');
    if (!container) {
        console.error('❌ stationContainer not found!');
        return;
    }
    
    console.log('🔄 Updating station cards with', data.count, 'stations');
    
    if (data.stations.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-search" style="font-size: 4rem; color: #D1D5DB;"></i>
                <h4 class="mt-3 text-muted">No Stations Found</h4>
                <p class="text-muted">Try adjusting your search criteria.</p>
            </div>
        `;
        const countBadge = document.getElementById('stationCount');
        if (countBadge) countBadge.textContent = '0 Stations';
        return;
    }
    
    let html = '<div class="row g-4">';
    
    data.stations.forEach(function(station) {
        // Queue Status
        let queueHTML = '';
        if (station.queue_status) {
            const icons = {
                'green': 'check-circle',
                'yellow': 'clock',
                'red': 'exclamation-circle'
            };
            queueHTML = `
                <span class="status-badge status-${station.queue_status.status}">
                    <i class="bi bi-${icons[station.queue_status.status] || 'circle'}"></i>
                    ${station.queue_status.status_display}
                </span>
                <span class="text-muted ms-2">
                    <i class="bi bi-car-front"></i> ${station.queue_status.queue_length} cars
                </span>
            `;
        } else {
            queueHTML = `
                <span class="status-badge status-green">
                    <i class="bi bi-check-circle"></i> No Queue Info
                </span>
            `;
        }
        
        // Fuel Prices
        let fuelHTML = '';
        if (station.fuel_prices && station.fuel_prices.length > 0) {
            fuelHTML = `
                <div class="mt-2">
                    <small class="text-muted fw-bold">Fuel Prices:</small>
                    <div class="d-flex flex-wrap gap-1 mt-1">
                        ${station.fuel_prices.map(function(p) {
                            return `<span class="fuel-badge fuel-available">${p.fuel_type}: ${p.price} SDG</span>`;
                        }).join('')}
                    </div>
                </div>
            `;
        }
        
        // Rating
        let ratingHTML = '';
        if (station.avg_rating && station.avg_rating > 0) {
            const fullStars = Math.round(station.avg_rating);
            const starsHtml = '⭐'.repeat(fullStars);
            ratingHTML = `
                <div class="d-flex align-items-center gap-2 mt-1">
                    <span class="text-warning">${starsHtml}</span>
                    <span class="text-muted small">(${station.total_ratings || 0})</span>
                </div>
            `;
        } else {
            ratingHTML = `
                <div class="d-flex align-items-center gap-2 mt-1">
                    <span class="text-muted small"><i class="bi bi-star"></i> No ratings yet</span>
                </div>
            `;
        }
        
        // Map Link
        let mapHTML = '';
        if (station.map_link && station.map_link !== 'null' && station.map_link.trim() !== '') {
            mapHTML = `
                <button type="button" class="btn btn-teal btn-sm mt-2" data-bs-toggle="modal" data-bs-target="#mapModal${station.id}">
                    <i class="bi bi-geo-alt"></i> View Location
                </button>
            `;
        }
        
        html += `
            <div class="col-md-4">
                <div class="station-card h-100 p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <h5 class="station-name mb-0">
                            <i class="bi bi-fuel-pump text-teal"></i> ${station.name}
                        </h5>
                    </div>
                    ${ratingHTML}
                    <p class="station-location">
                        <i class="bi bi-geo-alt text-danger"></i> ${station.location}
                    </p>
                    <p class="station-location">
                        <i class="bi bi-building text-info"></i> ${station.city}
                    </p>
                    <div class="mt-2">${queueHTML}</div>
                    ${fuelHTML}
                    ${station.operating_hours ? `
                        <p class="mt-2 mb-0 text-muted small">
                            <i class="bi bi-clock"></i> ${station.operating_hours}
                        </p>
                    ` : ''}
                    ${mapHTML}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Update count
    const countBadge = document.getElementById('stationCount');
    if (countBadge) countBadge.textContent = `${data.count} Stations`;
}

// ============================================
// 2. SCROLL TO STATIONS
// ============================================

function scrollToStations() {
    const stationSection = document.getElementById('stations');
    if (stationSection) {
        stationSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            setTimeout(function() {
                searchInput.focus();
            }, 500);
        }
    }
}

// ============================================
// 3. AUTO-REFRESH STATION LIST
// ============================================

function startAutoRefresh() {
    setInterval(function() {
        console.log('🔄 Auto-refreshing station list...');
        performSearch();
    }, 3000);
}

// ============================================
// 5. QUEUE STATUS UPDATE (AJAX)
// ============================================

function updateQueueStatus(status, queueLength, stationId) {
    console.log('📤 Updating queue:', {status, queueLength, stationId});
    
    const data = {
        status: status,
        queue_length: parseInt(queueLength) || 0,
        station_id: stationId
    };
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCSRFToken();
    
    fetch('/stations/api/update-queue/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        console.log('📥 Response status:', response.status);
        return response.json();
    })
    .then(function(data) {
        console.log('✅ Queue update response:', data);
        if (data.success) {
            showNotification('success', data.message);
            updateQueueDisplay(data, stationId);
        } else {
            showNotification('error', data.error || 'Something went wrong');
        }
    })
    .catch(function(error) {
        console.error('❌ Queue update error:', error);
        showNotification('error', 'Network error. Please try again.');
    });
}

function updateQueueDisplay(data, stationId) {
    console.log('🔄 Updating queue display for station:', stationId);
    
    const queueBadge = document.getElementById('queueStatusBadge-' + stationId);
    const queueCars = document.getElementById('queueCars-' + stationId);
    const queueTime = document.getElementById('queueTime-' + stationId);
    
    if (queueBadge) {
        const icons = {
            'green': 'check-circle',
            'yellow': 'clock',
            'red': 'exclamation-circle'
        };
        queueBadge.className = 'status-badge status-' + data.status;
        queueBadge.innerHTML = `
            <i class="bi bi-${icons[data.status] || 'circle'}"></i>
            ${data.status_display}
        `;
    }
    
    if (queueCars) {
        queueCars.textContent = data.queue_length + ' cars waiting';
    }
    
    if (queueTime) {
        queueTime.textContent = 'Updated: ' + data.updated_at;
    }
}

// ============================================
// 6. NOTIFICATIONS
// ============================================

function showNotification(type, message) {
    const container = document.getElementById('notificationContainer');
    if (!container) {
        console.warn('⚠️ notificationContainer not found');
        return;
    }
    
    const icons = {
        'success': 'check-circle',
        'error': 'x-circle',
        'warning': 'exclamation-circle'
    };
    
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 'alert-warning';
    
    const html = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="bi bi-${icons[type] || 'info-circle'}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', html);
    
    setTimeout(function() {
        const alerts = container.querySelectorAll('.alert');
        if (alerts.length > 0) {
            const lastAlert = alerts[alerts.length - 1];
            const closeBtn = lastAlert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }
    }, 4000);
}

// ============================================
// 4. INITIALIZE (on page load)
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 FuelRadar AJAX initialized!');
    
    // Search input - triggers on typing
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        console.log('✅ Search input found');
        searchInput.addEventListener('input', performSearch);
    } else {
        console.warn('⚠️ Search input not found');
    }
    
    // City filter - triggers on change
    const cityFilter = document.getElementById('cityFilter');
    if (cityFilter) {
        console.log('✅ City filter found');
        cityFilter.addEventListener('change', performSearch);
    } else {
        console.warn('⚠️ City filter not found');
    }
    
    // Search button - triggers on click
    const searchBtn = document.querySelector('button[onclick="performSearch()"]');
    if (searchBtn) {
        console.log('✅ Search button found');
        searchBtn.addEventListener('click', performSearch);
    } else {
        console.warn('⚠️ Search button not found');
    }
    
    // Start auto-refresh
    const stationContainer = document.getElementById('stationContainer');
    if (stationContainer) {
        startAutoRefresh();
        console.log('✅ Auto-refresh started (every 3s)');
    }
    
    console.log('✅ All systems ready!');
});