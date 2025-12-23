// ========================================
// 🏥 MEDICARE PRO - JavaScript Module
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initNavbar();
    initParticles();
    initAnimations();
    initFormEnhancements();
    initAlerts();
});

// ===== NAVBAR =====
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarNav = document.querySelector('.navbar-nav');

    // Scroll effect
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile menu toggle
    if (navbarToggle && navbarNav) {
        navbarToggle.addEventListener('click', () => {
            navbarNav.classList.toggle('active');

            // Animate hamburger
            const spans = navbarToggle.querySelectorAll('span');
            spans.forEach((span, i) => {
                span.style.transform = navbarNav.classList.contains('active')
                    ? i === 0 ? 'rotate(45deg) translate(5px, 5px)'
                        : i === 1 ? 'opacity: 0'
                            : 'rotate(-45deg) translate(7px, -6px)'
                    : '';
            });
        });
    }

    // Close menu on link click (mobile)
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navbarNav) navbarNav.classList.remove('active');
        });
    });
}

// ===== PARTICLES =====
function initParticles() {
    const particlesContainer = document.querySelector('.particles');
    if (!particlesContainer) return;

    // Create floating particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.animationDuration = `${20 + Math.random() * 15}s`;
        particle.style.width = `${5 + Math.random() * 10}px`;
        particle.style.height = particle.style.width;
        particlesContainer.appendChild(particle);
    }
}

// ===== ANIMATIONS =====
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animate class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // Add stagger delays to grid items
    document.querySelectorAll('.features-grid .feature-card, .stats-grid .stat-card').forEach((el, i) => {
        el.style.animationDelay = `${i * 0.1}s`;
    });
}

// ===== FORM ENHANCEMENTS =====
function initFormEnhancements() {
    // Add floating label effect
    document.querySelectorAll('.form-group input, .form-group select, .form-group textarea').forEach(input => {
        // Focus effects
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('focused');
            if (this.value) {
                this.parentElement.classList.add('filled');
            } else {
                this.parentElement.classList.remove('filled');
            }
        });

        // Check initial state
        if (input.value) {
            input.parentElement.classList.add('filled');
        }
    });

    // File input preview
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function () {
            const label = this.parentElement.querySelector('.file-input-label');
            if (label && this.files.length > 0) {
                label.innerHTML = `<i class="fas fa-check-circle"></i> ${this.files[0].name}`;
                label.style.borderColor = 'var(--success-500)';
                label.style.color = 'var(--success-500)';
            }
        });
    });

    // Form validation visual feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            const inputs = this.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.parentElement.classList.add('error');
                    input.style.borderColor = 'var(--error-500)';
                } else {
                    input.parentElement.classList.remove('error');
                    input.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'error');
            }
        });
    });

    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function () {
            const strength = getPasswordStrength(this.value);
            updatePasswordStrength(this, strength);
        });
    });
}

function getPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    return strength;
}

function updatePasswordStrength(input, strength) {
    const colors = ['#f44336', '#ff9800', '#ffeb3b', '#8bc34a', '#4caf50'];
    const labels = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'];

    let indicator = input.parentElement.querySelector('.password-strength');
    if (!indicator && strength > 0) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.style.cssText = 'margin-top: 5px; font-size: 0.8rem; display: flex; gap: 5px; align-items: center;';
        input.parentElement.appendChild(indicator);
    }

    if (indicator) {
        const bars = Array(5).fill(0).map((_, i) =>
            `<div style="flex: 1; height: 4px; border-radius: 2px; background: ${i < strength ? colors[strength - 1] : 'rgba(255,255,255,0.1)'}"></div>`
        ).join('');
        indicator.innerHTML = `${bars} <span style="color: ${colors[strength - 1]}; margin-left: 10px;">${labels[strength - 1] || ''}</span>`;
    }
}

// ===== ALERTS =====
function initAlerts() {
    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

function showAlert(message, type = 'info') {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `<i class="fas ${icons[type]}"></i> ${message}`;

    // Insert at top of main content
    const main = document.querySelector('.main-content') || document.body;
    main.insertBefore(alert, main.firstChild);

    // Auto dismiss
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// ===== UTILITY FUNCTIONS =====
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const h = parseInt(hours);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const hour = h % 12 || 12;
    return `${hour}:${minutes} ${ampm}`;
}

function formatDate(dateString) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// ===== LOADING STATES =====
function showLoading(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    return originalText;
}

function hideLoading(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== RIPPLE EFFECT FOR BUTTONS =====
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function (e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;

        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===== COUNTER ANIMATION =====
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Initialize counters when visible
document.querySelectorAll('[data-counter]').forEach(el => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(el, parseInt(el.dataset.counter));
                observer.unobserve(el);
            }
        });
    });
    observer.observe(el);
});
