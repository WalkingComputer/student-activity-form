document.addEventListener('DOMContentLoaded', function () {
    // ===== Theme Switcher =====
    var themeToggle = document.getElementById('theme-toggle');
    var themeIcon = document.getElementById('theme-icon');
    var html = document.documentElement;

    var savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateIcon(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var current = html.getAttribute('data-theme');
            var newTheme = current === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        }
    }

    // ===== Dynamic Viva Topic Field =====
    var choiceField = document.getElementById('id_choice');
    var vivaWrapper = document.getElementById('viva-topic-wrapper');

    if (choiceField && vivaWrapper) {
        function toggleViva() {
            if (choiceField.value === 'tech_viva') {
                vivaWrapper.style.display = 'block';
            } else {
                vivaWrapper.style.display = 'none';
            }
        }

        choiceField.addEventListener('change', toggleViva);
        // Run on page load (important for form re-display with errors)
        toggleViva();
    }

    // ===== Auto-dismiss alerts after 5s =====
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
});