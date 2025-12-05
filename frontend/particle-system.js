/* ====================================
   GREENCARE PARTICLE SYSTEM
   GPU-Accelerated Canvas Animation
   ==================================== */

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d', { alpha: true });
        this.particles = [];
        this.connections = [];
        this.mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
        this.animationId = null;
        
        this.resize();
        this.init();
        this.setupEvents();
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
    }
    
    init() {
        const particleCount = 120;
        const colors = [
            { r: 255, g: 255, b: 255, name: 'white' },
            { r: 79, g: 209, b: 197, name: 'green' },
            { r: 96, g: 165, b: 250, name: 'cyan' }
        ];
        
        for (let i = 0; i < particleCount; i++) {
            const color = colors[Math.floor(Math.random() * colors.length)];
            const size = Math.random() * 2 + 1.5;
            
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                z: Math.random() * 100,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                baseSize: size,
                size: size,
                color: color,
                opacity: Math.random() * 0.4 + 0.3,
                pulsePhase: Math.random() * Math.PI * 2,
                pulseSpeed: Math.random() * 0.01 + 0.008,
                isSymbol: false
            });
        }
    }
    
    setupEvents() {
        window.addEventListener('resize', () => this.resize());
        
        document.addEventListener('mousemove', (e) => {
            this.mouse.targetX = e.clientX;
            this.mouse.targetY = e.clientY;
        });
        
        // Smooth mouse following
        const updateMouse = () => {
            this.mouse.x += (this.mouse.targetX - this.mouse.x) * 0.1;
            this.mouse.y += (this.mouse.targetY - this.mouse.y) * 0.1;
            requestAnimationFrame(updateMouse);
        };
        updateMouse();
    }
    
    animate() {
        // Fade effect instead of clear for trail
        this.ctx.fillStyle = 'rgba(15, 28, 63, 0.08)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw particles
        this.particles.forEach((particle, i) => {
            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const maxDistance = 200;
            
            if (distance < maxDistance) {
                const force = (maxDistance - distance) / maxDistance;
                particle.vx += (dx / distance) * force * 0.15;
                particle.vy += (dy / distance) * force * 0.15;
            }
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Apply friction
            particle.vx *= 0.985;
            particle.vy *= 0.985;
            
            // Pulse animation
            particle.pulsePhase += particle.pulseSpeed;
            const pulse = Math.sin(particle.pulsePhase) * 0.3 + 1;
            particle.size = particle.baseSize * pulse;
            
            // Depth-based effects
            const depthFactor = 1 - (particle.z / 100) * 0.5;
            const finalOpacity = particle.opacity * depthFactor;
            
            // Draw particle with glow
            this.ctx.save();
            this.ctx.globalAlpha = finalOpacity;
            
            // Outer glow
            const gradient = this.ctx.createRadialGradient(
                particle.x, particle.y, 0,
                particle.x, particle.y, particle.size * 3
            );
            gradient.addColorStop(0, `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${finalOpacity})`);
            gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Core particle
            this.ctx.fillStyle = `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${finalOpacity})`;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.restore();
            
            // Draw connections
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dx2 = particle.x - p2.x;
                const dy2 = particle.y - p2.y;
                const dist = Math.sqrt(dx2 * dx2 + dy2 * dy2);
                
                if (dist < 120) {
                    const opacity = (1 - dist / 120) * 0.25 * finalOpacity;
                    
                    this.ctx.save();
                    this.ctx.globalAlpha = opacity;
                    this.ctx.strokeStyle = `rgb(79, 209, 197)`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                    this.ctx.restore();
                }
            }
        });
        
        // Draw mouse connections
        this.particles.forEach(particle => {
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 150) {
                const opacity = (1 - distance / 150) * 0.3;
                
                this.ctx.save();
                this.ctx.globalAlpha = opacity;
                const gradient = this.ctx.createLinearGradient(
                    particle.x, particle.y,
                    this.mouse.x, this.mouse.y
                );
                gradient.addColorStop(0, 'rgba(79, 209, 197, 0.5)');
                gradient.addColorStop(1, 'rgba(96, 165, 250, 0.5)');
                this.ctx.strokeStyle = gradient;
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(particle.x, particle.y);
                this.ctx.lineTo(this.mouse.x, this.mouse.y);
                this.ctx.stroke();
                this.ctx.restore();
            }
        });
        
        // DNA Helix effect near mouse
        this.drawDNAHelix(this.mouse.x, this.mouse.y);
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    drawDNAHelix(x, y) {
        const time = Date.now() * 0.001;
        const amplitude = 40;
        const points = 25;
        
        this.ctx.save();
        this.ctx.globalAlpha = 0.2;
        
        // First helix strand
        this.ctx.beginPath();
        this.ctx.strokeStyle = '#2c7a7b';
        this.ctx.lineWidth = 2;
        
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 4 + time;
            const px = x + Math.sin(angle) * amplitude - 80;
            const py = y + t * 180 - 90;
            
            if (i === 0) {
                this.ctx.moveTo(px, py);
            } else {
                this.ctx.lineTo(px, py);
            }
            
            // Connection lines at specific points
            if (Math.abs(Math.sin(angle)) < 0.15) {
                const angle2 = angle + Math.PI;
                const px2 = x + Math.sin(angle2) * amplitude - 80;
                
                this.ctx.save();
                this.ctx.strokeStyle = 'rgba(79, 209, 197, 0.3)';
                this.ctx.lineWidth = 1.5;
                this.ctx.beginPath();
                this.ctx.moveTo(px, py);
                this.ctx.lineTo(px2, py);
                this.ctx.stroke();
                this.ctx.restore();
            }
        }
        
        this.ctx.stroke();
        this.ctx.restore();
    }
    
    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Initialize particle system when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        window.particleSystem = new ParticleSystem(canvas);
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.particleSystem) {
        window.particleSystem.destroy();
    }
});
