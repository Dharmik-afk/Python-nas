/**
 * Main Application Script
 * Global initializations and utility functions can be placed here.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Media Vault Frontend Loaded');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        })
    }
});

// HTMX Global Events
document.body.addEventListener('htmx:beforeSwap', function(evt) {
    // Allow 404 responses to swap (for empty folder states or handled errors)
    if (evt.detail.xhr.status === 404) {
        evt.detail.shouldSwap = true;
        evt.detail.isError = false;
    }
});
