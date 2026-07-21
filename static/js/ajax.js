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
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateStationCardsInstant(data);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

function updateStationCardsInstant(data) {
    const container = document.getElementById('stationContainer');
    if (!container) return;
    
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
    
    data.stations.forEach(station => {
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
        
        let fuelHTML = '';
        if (station.fuel_prices && station.fuel_prices.length > 0) {
            fuelHTML = `
                <div class="mt-2">
                    <small class="text-muted fw-bold">Fuel Prices:</small>
                    <div class="d-flex flex-wrap gap-1 mt-1">
                        ${station.fuel_prices.map(p => 
                            `<span class="fuel-badge fuel-available">${p.fuel_type}: ${p.price} SDG</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
        
        html += `
            <div class="col-md-4">
                <div class="station-card h-100 p-3">
                    <h5 class="station-name">
                        <i class="bi bi-fuel-pump text-teal"></i> ${station.name}
                    </h5>
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
            setTimeout(() => {
                searchInput.focus();
            }, 500);
        }
    }
}

// ============================================
// 3. INITIALIZE (on page load)
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
    
    console.log('✅ All systems ready!');
});