let particleSketch = (p) => {
  let colours = [
    '#0E2440', // Dark blue
    '#6A517D', // Purple
    '#C25D8C', // Pink
    '#F57382', // Light red
    '#FAC2AA' // Peach
  ];

  let addParticleCounter = 0; // Counter to control particle addition

  p.setup = function() {
    let particleCanvas = p.createCanvas(p.windowWidth-20, 700); // Create the canvas to fill the width of the screen
    particleCanvas.parent('particle-canvas'); // Attach the canvas to the dedicated container
    p.angleMode(p.DEGREES);
    p.frameRate(30); 
  }

  p.windowResized = function() {
    let width = Math.min(screen.height, window.innerWidth);
    p.resizeCanvas(width, 700); // Keeps the height fixed at 700
    p.redraw(); // Redraw the canvas after resizing
};


  p.draw = function() {
    p.clear(); // Clear the background every frame

    // Update and display particles
    updateParticles();

    // Add new particles at a controlled rate
    if (addParticleCounter % 10 === 0 && particles.length < 80) { // Adjust the modulus value to control the rate
      addParticle();
    }

    addParticleCounter++; // Increment the counter each frame
  }

  class Particle {
    constructor(x, y, color, particlesArray) {
        this.x = x;
        this.y = y;
        this.vx = p.random(0.5, 2); // Bias velocity towards the right (positive x direction)
        this.vy = p.random(-2, -0.5); // Bias velocity upwards (negative y direction)
        this.alpha = 255; // Full opacity initially
        this.size = p.random(5, 10); // Random size for the particles
        this.color = color; // Particle color
        this.particlesArray = particlesArray; // Reference to the particles array
        this.speed = 2;
    }

    update() {
        this.x += this.vx*this.speed;
        this.y += this.vy*this.speed;
        this.alpha -= 0.5; // Fade out the particle

        if (this.isDead()) {
            this.removeSelf(); // Remove itself from the array if dead
        }
    }

    isDead() {
        return this.alpha <= 0; // Particle is considered dead when fully transparent
    }

    removeSelf() {
        const index = this.particlesArray.indexOf(this);
        if (index > -1) {
            this.particlesArray.splice(index, 1); // Remove this particle from the array
        }
    }

    display() {
        p.noStroke();
        p.fill(this.color + p.hex(p.int(this.alpha), 2)); // Adjust color with alpha transparency
        p.ellipse(this.x, this.y, this.size, this.size);
    }
  }

  let particles = []; // Array to hold the particles

  function addParticle() {
    // Spawn particles along the bottom edge of the canvas
    let x = p.random(-300, p.width); // Anywhere along the bottom edge
    let y = p.random(p.height + 50, p.height + 150); // Off canvas below the bottom

    let color = p.random(colours); // Random color from the palette
    particles.push(new Particle(x, y, color, particles));
  }

  function updateParticles() {
    for (let i = 0; i < particles.length; i++) {
        let particle = particles[i];
        particle.update();
        particle.display();
    }
  }
}

new p5(particleSketch);
