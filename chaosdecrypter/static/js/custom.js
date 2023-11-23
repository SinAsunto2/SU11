// ----------------------------------------------------------------------------
// Dark mode / light
function setTheme(theme) {
    document.body.classList.toggle('theme-dark', theme === 'dark');
    document.cookie = `theme=${theme}; expires=${new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toUTCString()}; path=/`;
}

window.onload = function() {
    const theme = document.cookie.replace(/(?:(?:^|.*;\s*)theme\s*=\s*([^;]*).*$)|^.*$/, "$1");
    setTheme(theme);
    
    const themeToggle = document.querySelector('.toggle-dark input');
    themeToggle.checked = theme === 'dark';
}

const themeToggle = document.querySelector('.toggle-dark input');
themeToggle.addEventListener('change', function() {
    setTheme(this.checked ? 'dark' : 'light');
});
// ----------------------------------------------------------------------------



var etiquetasB = document.querySelectorAll('b');

etiquetasB.forEach(function(etiqueta) {
    etiqueta.addEventListener('click', function() {
        alert('Me has encontrado :)');
    });
});