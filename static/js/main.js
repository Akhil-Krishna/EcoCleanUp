// EcoCleanUp Hub - Main JavaScript
// COMP639 S1 2026

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.eco-alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Password strength indicator
    const passwordField = document.getElementById('password') || document.getElementById('new_password');
    const strengthBar = document.getElementById('password-strength-bar');
    const strengthText = document.getElementById('password-strength-text');

    if (passwordField && strengthBar) {
        passwordField.addEventListener('input', function () {
            const val = this.value;
            let strength = 0;
            if (val.length >= 8) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[a-z]/.test(val)) strength++;
            if (/\d/.test(val)) strength++;
            if (/[!@#$%^&*(),.?":{}|<>_\-+=\[\]]/.test(val)) strength++;

            const labels = ['', 'Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
            const colours = ['', 'danger', 'warning', 'info', 'primary', 'success'];

            strengthBar.style.width = (strength * 20) + '%';
            strengthBar.className = 'progress-bar bg-' + (colours[strength] || 'danger');
            if (strengthText) strengthText.textContent = labels[strength] || '';
        });
    }

    // Confirm dangerous actions
    const dangerForms = document.querySelectorAll('[data-confirm]');
    dangerForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Show notifications modal automatically if there are unread ones
    const notifModal = document.getElementById('notificationsModal');
    const notifBadge = document.querySelector('.navbar .badge.bg-danger');
    if (notifModal && notifBadge && sessionStorage.getItem('notifShown') !== 'true') {
        sessionStorage.setItem('notifShown', 'true');
        const modal = new bootstrap.Modal(notifModal);
        modal.show();
    }

    // Preview uploaded profile image
    const imageInput = document.getElementById('profile_image');
    const imagePreview = document.getElementById('image-preview');
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Tooltip initialization
    const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipEls.forEach(function (el) { new bootstrap.Tooltip(el); });

});
