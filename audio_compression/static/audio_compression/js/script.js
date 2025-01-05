document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.freq-button');
    const hiddenInput = document.getElementById('cutoff_frequency');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            buttons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            hiddenInput.value = button.getAttribute('data-value');
        });
    });
});
