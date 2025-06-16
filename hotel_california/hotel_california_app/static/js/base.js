// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du menu fixe
    const header = document.querySelector('.main-header');
    const headerHeight = header.offsetHeight;

    function handleScroll() {
        if (window.scrollY > 50) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll);

    // Défilement fluide pour les ancres
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const targetPosition = target.offsetTop - headerHeight;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Gestion des messages système
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        // Ajouter un bouton de fermeture
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.className = 'alert-close';
        message.appendChild(closeButton);

        // Fermeture du message
        closeButton.addEventListener('click', () => {
            message.remove();
        });

        // Auto-fermeture après 5 secondes
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Animation du menu mobile
    const mobileMenuButton = document.createElement('button');
    mobileMenuButton.className = 'mobile-menu-button';
    mobileMenuButton.innerHTML = '<span></span><span></span><span></span>';
    
    const nav = document.querySelector('.nav-links');
    const headerContainer = document.querySelector('.main-nav');
    
    headerContainer.insertBefore(mobileMenuButton, nav);

    mobileMenuButton.addEventListener('click', () => {
        nav.classList.toggle('nav-open');
        mobileMenuButton.classList.toggle('active');
    });

    // Gestion des formulaires
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showFormError('Veuillez remplir tous les champs obligatoires');
            }
        });
    });
});

// Utilitaires
function showFormError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.textContent = message;
    
    const form = document.querySelector('form');
    form.insertBefore(errorDiv, form.firstChild);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Gestion du chargement des images
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
});

// Détection de la connexion réseau
window.addEventListener('online', () => {
    showNetworkStatus('La connexion est rétablie', 'success');
});

window.addEventListener('offline', () => {
    showNetworkStatus('La connexion est perdue', 'error');
});

function showNetworkStatus(message, type) {
    const statusDiv = document.createElement('div');
    statusDiv.className = `alert alert-${type}`;
    statusDiv.textContent = message;
    document.body.insertBefore(statusDiv, document.body.firstChild);

    setTimeout(() => {
        statusDiv.remove();
    }, 3000);
}