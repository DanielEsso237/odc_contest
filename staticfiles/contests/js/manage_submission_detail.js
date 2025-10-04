document.addEventListener('DOMContentLoaded', function() {
    const rejectButton = document.querySelector('.reject-button');
    
    if (rejectButton) {
        rejectButton.addEventListener('click', function(event) {
            if (!confirm('Êtes-vous sûr de vouloir rejeter cette soumission ?')) {
                event.preventDefault();
            }
        });
    }
});