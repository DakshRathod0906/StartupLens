/* ============================================================
   StartupLens App – Global JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Initialize all Bootstrap popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible.auto-dismiss');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize Select2 for dynamic tagging
    if (typeof jQuery !== 'undefined' && $.fn.select2) {
        $('.select2-tags').select2({
            theme: 'bootstrap-5',
            tags: true,
            tokenSeparators: [',', ' '],
            placeholder: "Select or type to create new tags...",
            allowClear: true
        });
    }
});
