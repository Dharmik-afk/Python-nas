document.addEventListener('DOMContentLoaded', () => {
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    // Apply the saved theme on page load
    if (currentTheme) {
        if (currentTheme === 'dark-mode') {
            document.body.classList.add('dark-mode');
            if (toggleSwitch) {
                toggleSwitch.checked = true;
            }
        }
    } else {
        // If no theme is saved, check for the user's system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add('dark-mode');
            if (toggleSwitch) {
                toggleSwitch.checked = true;
            }
            localStorage.setItem('theme', 'dark-mode');
        }
    }

    // Function to handle the theme switch toggle
    function switchTheme(e) {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    }

    // Add event listener only if the toggle switch exists on the page
    if (toggleSwitch) {
        toggleSwitch.addEventListener('change', switchTheme);
    }
});
