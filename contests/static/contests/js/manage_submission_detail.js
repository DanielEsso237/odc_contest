document.addEventListener('DOMContentLoaded', function() {
    const rejectButton = document.querySelector('.reject-button');
    if (rejectButton) {
        rejectButton.addEventListener('click', function(event) {
            if (!confirm('⚠️ Êtes-vous sûr de vouloir rejeter et supprimer définitivement cette soumission ?')) {
                event.preventDefault();
            }
        });
    }

    
    const form = document.querySelector('form');
    const publishButton = document.querySelector('.publish-button');
    if (form && publishButton) {
        form.addEventListener('submit', function(e) {
            const clickedBtn = document.activeElement;
            if (clickedBtn.name === 'publish' || clickedBtn.name === 'reject') {
                clickedBtn.disabled = true;
                clickedBtn.innerHTML = '<span class="loading"></span> Traitement...';
                setTimeout(() => {
                    clickedBtn.disabled = false;
                    clickedBtn.innerHTML = clickedBtn.name === 'publish' ? 'Publier la soumission' : 'Rejeter et supprimer';
                }, 5000); 
            }
        });
    }

   
    const videos = document.querySelectorAll('video.submission-media');
    videos.forEach(video => {
        video.addEventListener('mouseenter', function() {
            if (this.paused) {
                this.play().catch(err => {
                    console.log('Autoplay bloqué par le navigateur:', err);
                });
            }
        });
        video.addEventListener('mouseleave', function() {
            this.pause();
        });
    });

    
    const images = document.querySelectorAll('img.submission-media');
    images.forEach(img => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', function() {
            const overlay = document.createElement('div');
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                cursor: zoom-out;
            `;
            const imgClone = this.cloneNode();
            imgClone.style.cssText = `
                max-width: 95%;
                max-height: 95%;
                object-fit: contain;
                box-shadow: 0 0 50px rgba(0,0,0,0.5);
            `;
            overlay.appendChild(imgClone);
            document.body.appendChild(overlay);
            overlay.addEventListener('click', function() {
                document.body.removeChild(overlay);
            });
        });
    });

    // Compteur de caractères pour le textarea
    const textarea = document.getElementById('moderator_text');
    if (textarea) {
        const counter = document.createElement('div');
        counter.style.cssText = `
            text-align: right;
            font-size: 12px;
            color: #64748b;
            margin-top: 5px;
        `;
        textarea.parentElement.appendChild(counter);
        
        function updateCounter() {
            const length = textarea.value.length;
            counter.textContent = `${length} caractère${length > 1 ? 's' : ''}`;
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }
});