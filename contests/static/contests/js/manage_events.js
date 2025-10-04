document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('create-event');
    const btn = document.querySelector('.add-event-button');
    const span = document.querySelector('.close-modal');

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});