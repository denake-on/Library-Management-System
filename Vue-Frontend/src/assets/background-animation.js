// Background animation for login page
let canvas;
let particles = [];
const particleCount = 100;

function setup() {
  canvas = createCanvas(windowWidth, windowHeight);
  canvas.position(0, 0);
  canvas.style('z-index', '-1');
  
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: random(width),
      y: random(height),
      size: random(1, 3),
      speedX: random(-1, 1),
      speedY: random(-1, 1),
      opacity: random(0.3, 0.7)
    });
  }
}

function draw() {
  background(30, 30, 40, 10);
  
  // Draw particles
  fill(100, 150, 200, 50);
  noStroke();
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i];
    ellipse(p.x, p.y, p.size);
    
    // Move particles
    p.x += p.speedX;
    p.y += p.speedY;
    
    // Bounce off edges
    if (p.x < 0 || p.x > width) p.speedX *= -1;
    if (p.y < 0 || p.y > height) p.speedY *= -1;
  }
  
  // Draw connecting lines between nearby particles
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const distance = sqrt(dx * dx + dy * dy);
      
      if (distance < 100) {
        stroke(100, 150, 200, map(distance, 0, 100, 0.2, 0));
        line(particles[i].x, particles[i].y, particles[j].x, particles[j].y);
      }
    }
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}