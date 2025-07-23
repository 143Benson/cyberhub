// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.createElement('div');
mobileMenu.className = 'mobile-menu';
mobileMenu.innerHTML = `
    <a href="#services" class="nav-link" data-text="Services">Services</a>
    <a href="#features" class="nav-link" data-text="Features">Features</a>
    <a href="#pricing" class="nav-link" data-text="Pricing">Pricing</a>
    <a href="#contact" class="nav-link" data-text="Contact">Contact</a>
    <div class="mobile-auth">
        <a href="login.html" class="btn-login">Login</a>
        <a href="register.html" class="btn-signup">Sign Up</a>
    </div>
`;
document.body.appendChild(mobileMenu);

const mobileOverlay = document.createElement('div');
mobileOverlay.className = 'mobile-overlay';
document.body.appendChild(mobileOverlay);

mobileMenuBtn.addEventListener('click', () => {
    mobileMenuBtn.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    mobileOverlay.classList.toggle('active');
    document.body.classList.toggle('no-scroll');
});

mobileOverlay.addEventListener('click', () => {
    mobileMenuBtn.classList.remove('active');
    mobileMenu.classList.remove('active');
    mobileOverlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
});

// Header Scroll Effect
const header = document.querySelector('.futuristic-header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Back to Top Button
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTop.classList.add('active');
    } else {
        backToTop.classList.remove('active');
    }
});

backToTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Animated Counters
const statValues = document.querySelectorAll('.stat-value');
const statsSection = document.querySelector('.stats-section');

function animateCounters() {
    const sectionPosition = statsSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.3;

    if (sectionPosition < screenPosition) {
        statValues.forEach(stat => {
            const target = +stat.getAttribute('data-count');
            const count = +stat.innerText;
            const increment = target / 100;

            if (count < target) {
                stat.innerText = Math.ceil(count + increment);
                setTimeout(animateCounters, 20);
            } else {
                stat.innerText = target;
            }
        });
    }
}

window.addEventListener('scroll', animateCounters);

// Initialize Particles.js
document.addEventListener('DOMContentLoaded', function() {
    if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": 80,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#f0a500"
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": 0.3,
                    "random": false,
                    "anim": {
                        "enable": false,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": false,
                        "speed": 40,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#f0a500",
                    "opacity": 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 2,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "bubble": {
                        "distance": 400,
                        "size": 40,
                        "duration": 2,
                        "opacity": 8,
                        "speed": 3
                    },
                    "repulse": {
                        "distance": 200,
                        "duration": 0.4
                    },
                    "push": {
                        "particles_nb": 4
                    },
                    "remove": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true
        });
    }

    // Typing Animation
    const typingText = document.querySelector('.typing-text');
    if (typingText) {
        const text = typingText.textContent;
        typingText.textContent = '';
        
        let i = 0;
        const typing = setInterval(() => {
            if (i < text.length) {
                typingText.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typing);
            }
        }, 100);
    }
});

// Navigation Highlight
const navLinks = document.querySelectorAll('.nav-link');
const navHighlight = document.querySelector('.nav-highlight');

function moveHighlight(e) {
    if (!e.target.classList.contains('nav-link')) return;
    
    const link = e.target;
    const linkRect = link.getBoundingClientRect();
    const navRect = document.querySelector('.neon-nav').getBoundingClientRect();
    
    navHighlight.style.width = `${linkRect.width}px`;
    navHighlight.style.left = `${linkRect.left - navRect.left}px`;
}

navLinks.forEach(link => {
    link.addEventListener('mouseenter', moveHighlight);
});

// Initialize highlight position
if (navLinks.length > 0 && navHighlight) {
    const firstLink = navLinks[0];
    navHighlight.style.width = `${firstLink.offsetWidth}px`;
    navHighlight.style.left = `${firstLink.offsetLeft}px`;
}