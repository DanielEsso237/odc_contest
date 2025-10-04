document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('create-trial');
    const addButton = document.querySelector('.add-event-button');
    const closeButton = document.querySelector('.close-modal');
    const form = document.querySelector('.event-form');

    if (addButton) {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'block';
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    if (form) {
        form.addEventListener('submit', function(e) {
            const title = document.getElementById('title').value.trim();
            if (!title) {
                e.preventDefault();
                alert('Le titre de l\'épreuve est obligatoire.');
                document.getElementById('title').focus();
            }
        });
    }

    // Gestion de la touche Échap pour fermer le modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    });
});