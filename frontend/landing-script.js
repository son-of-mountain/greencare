// Smooth scrolling
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Navigate to main app
function enterApp() {
    window.location.href = '/app/index.html';
}

// Health & Environment Interactive Canvas Animation
class HealthEnvironmentAnimation {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.targetMouseX = 0;
        this.targetMouseY = 0;
        this.connections = [];
        
        this.resize();
        this.init();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    init() {
        const particleCount = 80;
        const symbols = ['🌱', '💚', '🌿', '🍃', '💧', '⚕️', '🩺', '💊', '🏥', '❤️'];
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 3 + 2,
                symbol: symbols[Math.floor(Math.random() * symbols.length)],
                symbolSize: Math.random() * 20 + 15,
                isSymbol: Math.random() > 0.7,
                color: `rgba(79, 209, 197, ${Math.random() * 0.5 + 0.3})`,
                pulseSpeed: Math.random() * 0.02 + 0.01,
                pulsePhase: Math.random() * Math.PI * 2
            });
        }
    }
    
    onMouseMove(e) {
        this.targetMouseX = e.clientX;
        this.targetMouseY = e.clientY;
    }
    
    animate() {
        // Smooth mouse movement
        this.mouseX += (this.targetMouseX - this.mouseX) * 0.1;
        this.mouseY += (this.targetMouseY - this.mouseY) * 0.1;
        
        // Clear canvas with fade effect
        this.ctx.fillStyle = 'rgba(15, 28, 63, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw particles
        this.particles.forEach((particle, i) => {
            // Mouse interaction
            const dx = this.mouseX - particle.x;
            const dy = this.mouseY - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const maxDistance = 200;
            
            if (distance < maxDistance) {
                const force = (maxDistance - distance) / maxDistance;
                particle.vx += (dx / distance) * force * 0.2;
                particle.vy += (dy / distance) * force * 0.2;
            }
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Boundaries
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            // Friction
            particle.vx *= 0.98;
            particle.vy *= 0.98;
            
            // Pulse effect
            particle.pulsePhase += particle.pulseSpeed;
            const pulse = Math.sin(particle.pulsePhase) * 0.3 + 1;
            
            // Draw particle
            if (particle.isSymbol) {
                this.ctx.save();
                this.ctx.globalAlpha = 0.6 + Math.sin(particle.pulsePhase) * 0.2;
                this.ctx.font = `${particle.symbolSize * pulse}px Arial`;
                this.ctx.textAlign = 'center';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(particle.symbol, particle.x, particle.y);
                this.ctx.restore();
            } else {
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.radius * pulse, 0, Math.PI * 2);
                this.ctx.fillStyle = particle.color;
                this.ctx.fill();
                
                // Glow effect
                this.ctx.shadowBlur = 10;
                this.ctx.shadowColor = particle.color;
                this.ctx.fill();
                this.ctx.shadowBlur = 0;
            }
            
            // Draw connections
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dx2 = particle.x - p2.x;
                const dy2 = particle.y - p2.y;
                const dist = Math.sqrt(dx2 * dx2 + dy2 * dy2);
                
                if (dist < 100) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    const opacity = (1 - dist / 100) * 0.3;
                    this.ctx.strokeStyle = `rgba(79, 209, 197, ${opacity})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        });
        
        // Draw DNA helix effect near mouse
        this.drawDNAHelix(this.mouseX, this.mouseY);
        
        requestAnimationFrame(() => this.animate());
    }
    
    drawDNAHelix(x, y) {
        const time = Date.now() * 0.001;
        const amplitude = 50;
        const frequency = 0.1;
        const points = 30;
        
        this.ctx.beginPath();
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle1 = t * Math.PI * 4 + time;
            const angle2 = t * Math.PI * 4 + time + Math.PI;
            
            const x1 = x + Math.sin(angle1) * amplitude - 100;
            const y1 = y + t * 200 - 100;
            const x2 = x + Math.sin(angle2) * amplitude - 100;
            const y2 = y + t * 200 - 100;
            
            if (i === 0) {
                this.ctx.moveTo(x1, y1);
            } else {
                this.ctx.lineTo(x1, y1);
            }
            
            // Draw connecting lines
            if (Math.abs(Math.sin(angle1)) < 0.2) {
                this.ctx.save();
                this.ctx.strokeStyle = 'rgba(79, 209, 197, 0.4)';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(x1, y1);
                this.ctx.lineTo(x2, y2);
                this.ctx.stroke();
                this.ctx.restore();
            }
        }
        
        this.ctx.strokeStyle = 'rgba(44, 122, 123, 0.6)';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
    }
}

// Counter animation for impact stats
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.ceil(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.ceil(current);
        }
    }, 16);
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.3,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Trigger counter animations
            if (entry.target.classList.contains('impact-card')) {
                const counter = entry.target.querySelector('.counter');
                if (counter && !counter.classList.contains('animated')) {
                    const target = parseInt(counter.getAttribute('data-target'));
                    animateCounter(counter, target);
                    counter.classList.add('animated');
                }
            }
            
            // Add visible class for CSS animations
            entry.target.classList.add('visible');
            
            // Stop observing once animated
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Initialize canvas animation
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('healthCanvas');
    if (canvas) {
        new HealthEnvironmentAnimation(canvas);
    }
    
    // Observe impact cards
    const impactCards = document.querySelectorAll('.impact-card');
    impactCards.forEach(card => observer.observe(card));
    
    // Observe mission points
    const missionPoints = document.querySelectorAll('.mission-point');
    missionPoints.forEach(point => observer.observe(point));
    
    // Observe visual cards
    const visualCards = document.querySelectorAll('.visual-card');
    visualCards.forEach(card => observer.observe(card));
    
    // Add scroll listener for navbar
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
        }
        
        lastScroll = currentScroll;
    });
    
    // Parallax effect for hero background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.particle, .medical-icon');
        
        parallaxElements.forEach((el, index) => {
            const speed = 0.3 + (index * 0.1);
            const yPos = -(scrolled * speed);
            el.style.transform = `translateY(${yPos}px)`;
        });
    });
    
    // Add hover effect to navigation links
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                scrollToSection(targetId);
            }
        });
    });
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    button {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .mission-point, .visual-card, .impact-card {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.6s ease-out;
    }
    
    .mission-point.visible, .visual-card.visible, .impact-card.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    .mission-point:nth-child(1).visible {
        transition-delay: 0.1s;
    }
    
    .mission-point:nth-child(2).visible {
        transition-delay: 0.2s;
    }
    
    .mission-point:nth-child(3).visible {
        transition-delay: 0.3s;
    }
    
    .impact-card:nth-child(1).visible {
        transition-delay: 0.1s;
    }
    
    .impact-card:nth-child(2).visible {
        transition-delay: 0.2s;
    }
    
    .impact-card:nth-child(3).visible {
        transition-delay: 0.3s;
    }
    
    .impact-card:nth-child(4).visible {
        transition-delay: 0.4s;
    }
`;
document.head.appendChild(style);

// Preload images and optimize performance
window.addEventListener('load', () => {
    // Add loaded class to body for additional animations
    document.body.classList.add('loaded');
});

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Recalculate positions if needed
        console.log('Window resized');
    }, 250);
});

// Add mouse move parallax effect for hero
const hero = document.querySelector('.hero');
if (hero) {
    hero.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        const particles = document.querySelectorAll('.particle');
        particles.forEach((particle, index) => {
            const speed = (index + 1) * 10;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            
            particle.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
}

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        // Activate special mode
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = '';
        }, 3000);
        
        // Show message
        const msg = document.createElement('div');
        msg.textContent = '🎉 Mode Santé Booster Activé! 🎉';
        msg.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--primary);
            color: white;
            padding: 2rem 3rem;
            border-radius: 16px;
            font-size: 1.5rem;
            font-weight: 700;
            z-index: 10000;
            animation: fadeInUp 0.5s ease-out;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        `;
        document.body.appendChild(msg);
        setTimeout(() => {
            msg.remove();
        }, 3000);
    }
});

// Log welcome message
console.log('%c🌱 Bienvenue sur GreenCare!', 'color: #2c7a7b; font-size: 20px; font-weight: bold;');
console.log('%cPlateforme de transformation numérique et écologique pour la santé', 'color: #4a5568; font-size: 14px;');
