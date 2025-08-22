let yourSketch = (p) => {
  // Define the color palette
  let colours = [
    '#0E2440', // Dark blue
    '#6A517D', // Purple
    '#C25D8C', // Pink
    '#F57382', // Light red
    '#FAC2AA'  // Peach
  ];
    
  p.setup = function() {
    let canvas = p.createCanvas(p.windowWidth-20, 700); // Create the canvas to fill the width of the screen
    canvas.parent('background-canvas'); // Attach the canvas to the dedicated container
    p.noLoop(); // Draw only once
    p.background('#000000');
    p.angleMode(p.DEGREES);
  };


  p.windowResized = function() {
    let width = Math.min(screen.width, window.innerWidth);
    p.resizeCanvas(height, 700); // Keeps the height fixed at 700
    p.redraw(); // Redraw the canvas after resizing
};

  p.draw = function() {
    let gridSize = Math.sqrt(40); // Create a grid that approximately matches the number of splashes
    let cellWidth = p.width / gridSize; // Calculate the width of each cell
    let cellHeight = p.height / gridSize; // Calculate the height of each cell

    // Draw layered splashes
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            let x = i * cellWidth + p.random(0, cellWidth); // Position within the cell with some randomness
            let y = j * cellHeight + p.random(0, cellHeight); // Position within the cell with some randomness
            let color = p.random(colours);
            drawSplash(x, y, color);
        }
    }
    drawLargeCircles();
};

  function drawSplash(x, y, color) {
    let layers = p.int(p.random(2, 5)); // Number of circle layers
    for (let i = 0; i < layers; i++) {
      let size = p.random(10, 70); // Varying sizes for a splash effect
      let glowSize = size / 1.5;
      drawGlow(x, y, color, size, glowSize); // Pass 'p' as the first parameter
      p.fill(color);
      p.noStroke();
      p.ellipse(x, y, size); // Central circle
      drawSplatter(x, y, color, size, glowSize); // Pass 'p' as the first parameter
    }
  }

  function drawGlow(x, y, color, size, glowSize) {
    let alpha = 50; // Starting alpha value for the glow
    let glowSteps = glowSize / 5; // Number of steps in the glow effect, based on the glow size
    for (let i = 0; i < glowSteps; i++) {
      p.fill(color + p.hex(p.int(alpha), 2)); // Add transparency to the glow
      p.noStroke();
      p.ellipse(x, y, size + i * 5, size + i * 5); // Larger ellipses for a more pronounced glow
      alpha -= 5; // Gradually decrease the alpha to fade the glow
    }
  }

  function drawSplatter(x, y, color, size, glowSize) {
    let splatters = p.int(p.random(20, 30)); // Number of splatters
    for (let i = 0; i < splatters; i++) {
      let splatterX = x + p.random(-size, size);
      let splatterY = y + p.random(-size, size);
      let splatterSize = p.random(2, size / 2); // Smaller splatter circles
      // drawGlow(splatterX, splatterY, color, splatterSize, glowSize); // Pass 'p' as the first parameter
      p.fill(color);
      p.noStroke();
      p.ellipse(splatterX, splatterY, splatterSize);
    }
  }

  function drawLargeCircles() {
    let drawn = [];
    let attempts = 0;
    let maxAttempts = 500;
    while (drawn.length < 10 && attempts < maxAttempts) {
      attempts++;
      let circle = {
        x: p.random(p.width),
        y: p.random(p.height),
        size: p.random(40, 100) // Adjust size for larger circles
      };
      let overlapping = false;
      for (let other of drawn) {
        let d = p.dist(circle.x, circle.y, other.x, other.y);
        if (d < circle.size / 2 + other.size / 2) {
          overlapping = true;
          break;
        }
      }
      if (!overlapping) {
        drawn.push(circle);
      }
    }

    // Sort the circles based on the x-coordinate
    drawn.sort((a, b) => a.x - b.x);

    // Draw lines first
    p.stroke(colours[2]); // Use the pink color from the palette for the lines
    p.strokeWeight(2);
    for (let i = 0; i < drawn.length; i++) {
      if (i > 0) {
        p.line(drawn[i].x, drawn[i].y, drawn[i - 1].x, drawn[i - 1].y);
      }
      if (i < drawn.length - 1) {
        p.line(drawn[i].x, drawn[i].y, drawn[i + 1].x, drawn[i + 1].y);
      }
    }

    // Then draw the circles on top of the lines
    for (let i = 0; i < drawn.length; i++) {
      drawDoubleCircle(drawn[i].x, drawn[i].y, drawn[i].size); // Pass 'p' as the first parameter
    }
  }

  function drawDoubleCircle(x, y, diameter) {
    // Outer circle
    p.fill(p.random(colours));
    p.noStroke();
    p.ellipse(x, y, diameter, diameter);

    // Inner circle
    p.fill('#F59371'); // Orange color for the inner circle
    p.ellipse(x, y, diameter * 0.75, diameter * 0.75); // Inner circle is smaller
  }
};


new p5(yourSketch);

  // old stuff

      // function drawHexagonPattern() {
    //   const hexSize = 20; // Define the size of the hexagon
    //   const hexWidth = sqrt(3) * hexSize; // Calculate the width of a hexagon
    //   const hexHeight = 2 * hexSize;
    //   background('#000000');
    
    //   for (let x = 0; x < width + hexWidth; x += hexWidth * 3 / 4) {
    //     for (let y = 0; y < height + hexHeight; y += hexHeight * 0.5) {
    //       const xOffset = (y / hexHeight) % 2 == 1 ? hexWidth * 3 / 8 : 0; // Offset every other row
    //       drawHexagon(x + xOffset, y, hexSize);
    //     }
    //   }
    // }
    
    // function drawHexagon(x, y, s) {
    //   push();
    //   noStroke();
    //   fill('#0E2440'); // Fill color for the hexagon
    //   translate(x, y);
    //   beginShape();
    //   for (let i = 0; i < 6; i++) {
    //     vertex(s * cos(60 * i), s * sin(60 * i));
    //   }
    //   endShape(CLOSE);
    //   pop();
    // }
    
    