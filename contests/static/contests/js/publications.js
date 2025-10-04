document.addEventListener('DOMContentLoaded', function() {
    initCarousels();
    initVoteButtons();
    initModal();
    initKeyboardNavigation();
});

// ==================== CARROUSEL ====================
function initCarousels() {
    document.querySelectorAll('.media-carousel').forEach(carousel => {
        const submissionId = carousel.dataset.submission;
        updateSlideCounter(submissionId);
        pauseInactiveVideos(carousel);
        
        // Boutons prev/next
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                changeSlide(submissionId, -1);
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                changeSlide(submissionId, 1);
            });
        }
        
        // Indicateurs
        const indicators = carousel.querySelectorAll('.indicator');
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', (e) => {
                e.stopPropagation();
                currentSlide(submissionId, index);
            });
        });
        
        // Click sur images pour fullscreen
        const images = carousel.querySelectorAll('.media-slide img');
        images.forEach(img => {
            img.addEventListener('click', function() {
                openFullscreen(this);
            });
        });
    });
}

function changeSlide(submissionId, direction) {
    const carousel = document.querySelector(`[data-submission="${submissionId}"]`);
    if (!carousel) return;
    
    const slides = carousel.querySelectorAll('.media-slide');
    const indicators = carousel.querySelectorAll('.indicator');
    let currentIndex = -1;
    
    slides.forEach((slide, index) => {
        if (slide.classList.contains('active')) {
            currentIndex = index;
        }
    });
    
    if (currentIndex === -1) return;
    
    let newIndex = currentIndex + direction;
    if (newIndex >= slides.length) newIndex = 0;
    if (newIndex < 0) newIndex = slides.length - 1;
    
    slides[currentIndex].classList.remove('active');
    slides[newIndex].classList.add('active');
    
    if (indicators.length > 0) {
        indicators[currentIndex].classList.remove('active');
        indicators[newIndex].classList.add('active');
    }
    
    pauseInactiveVideos(carousel);
    updateSlideCounter(submissionId, newIndex + 1);
}

function currentSlide(submissionId, slideIndex) {
    const carousel = document.querySelector(`[data-submission="${submissionId}"]`);
    if (!carousel) return;
    
    const slides = carousel.querySelectorAll('.media-slide');
    const indicators = carousel.querySelectorAll('.indicator');
    
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === slideIndex);
    });
    
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === slideIndex);
    });
    
    pauseInactiveVideos(carousel);
    updateSlideCounter(submissionId, slideIndex + 1);
}

function updateSlideCounter(submissionId, currentSlideNum = 1) {
    const carousel = document.querySelector(`[data-submission="${submissionId}"]`);
    if (!carousel) return;
    
    const counter = carousel.querySelector('.current-slide');
    if (counter) {
        counter.textContent = currentSlideNum;
    }
}

function pauseInactiveVideos(carousel) {
    const slides = carousel.querySelectorAll('.media-slide');
    slides.forEach(slide => {
        const video = slide.querySelector('video');
        if (video) {
            if (!slide.classList.contains('active')) {
                video.pause();
            }
        }
    });
}

// ==================== MODAL FULLSCREEN ====================
function initModal() {
    const modal = document.getElementById('fullscreen-modal');
    if (!modal) return;
    
    const closeBtn = modal.querySelector('.close');
    
    // Fermer en cliquant sur le fond
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeFullscreen();
        }
    });
    
    // Fermer avec le bouton X
    if (closeBtn) {
        closeBtn.addEventListener('click', closeFullscreen);
    }
}

function openFullscreen(img) {
    const modal = document.getElementById('fullscreen-modal');
    const modalImg = document.getElementById('fullscreen-image');
    
    if (!modal || !modalImg) return;
    
    modal.style.display = 'block';
    modalImg.src = img.src;
    modalImg.alt = img.alt;
    document.body.style.overflow = 'hidden';
    
    // Animation d'entrée
    setTimeout(() => {
        modal.style.opacity = '1';
    }, 10);
}

function closeFullscreen() {
    const modal = document.getElementById('fullscreen-modal');
    if (!modal) return;
    
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }, 300);
}

// ==================== SYSTÈME DE VOTE ====================
function initVoteButtons() {
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const submissionId = this.dataset.submission;
            toggleVote(submissionId, this);
        });
    });
}

function toggleVote(submissionId, button) {
    // Désactiver le bouton pendant la requête
    button.disabled = true;
    
    fetch(`/contests/vote/${submissionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mettre à jour l'état du bouton
            button.classList.toggle('voted', data.has_voted);
            const voteIcon = button.querySelector('.vote-icon');
            const voteText = button.querySelector('.vote-text');
            const voteCount = button.querySelector('.vote-count');
            
            voteIcon.textContent = data.has_voted ? '♥' : '♡';
            voteText.textContent = data.has_voted ? 'A voté' : 'Voter';
            voteCount.textContent = data.vote_count;
            
            // Animation de succès
            button.style.transform = 'scale(1.1)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 200);
        } else {
            alert('Erreur : ' + (data.error || 'Impossible de voter'));
        }
    })
    .catch(error => {
        console.error('Erreur de vote:', error);
        alert('Une erreur est survenue lors du vote. Veuillez réessayer.');
    })
    .finally(() => {
        button.disabled = false;
    });
}

function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==================== NAVIGATION CLAVIER ====================
function initKeyboardNavigation() {
    let hoveredCarousel = null;
    
    // Détecter le carrousel survolé
    document.querySelectorAll('.media-carousel').forEach(carousel => {
        carousel.addEventListener('mouseenter', function() {
            hoveredCarousel = this.dataset.submission;
        });
        
        carousel.addEventListener('mouseleave', function() {
            hoveredCarousel = null;
        });
    });
    
    // Navigation avec les flèches
    document.addEventListener('keydown', function(e) {
        // Fermer le modal avec Escape
        if (e.key === 'Escape') {
            const modal = document.getElementById('fullscreen-modal');
            if (modal && modal.style.display === 'block') {
                closeFullscreen();
            }
        }
        
        // Navigation dans le carrousel avec les flèches
        if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && hoveredCarousel) {
            e.preventDefault();
            const direction = e.key === 'ArrowLeft' ? -1 : 1;
            changeSlide(hoveredCarousel, direction);
        }
    });
}

// ==================== SUPPORT TOUCH (Mobile) ====================
function initTouchSupport() {
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.querySelectorAll('.media-carousel').forEach(carousel => {
        const submissionId = carousel.dataset.submission;
        
        carousel.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        carousel.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe(submissionId);
        }, { passive: true });
    });
    
    function handleSwipe(submissionId) {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe gauche -> slide suivant
                changeSlide(submissionId, 1);
            } else {
                // Swipe droite -> slide précédent
                changeSlide(submissionId, -1);
            }
        }
    }
}

// Initialiser le support tactile
if ('ontouchstart' in window) {
    initTouchSupport();
}