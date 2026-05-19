# visualDraw — Gestural Canvas

A futuristic AI-powered gesture drawing canvas built using **MediaPipe Hands**, **JavaScript**, and **HTML5 Canvas**.  
Control a live pixel-grid drawing board using only your hands through webcam tracking.

---

## Features

- Real-time hand tracking using MediaPipe
- Gesture-based drawing and erasing
- Dynamic grid system (5×5 → 50×50)
- Multiple brush shapes
  - Square
  - Circle
  - Diamond
- Adjustable brush size
- Adjustable opacity
- Adjustable pinch sensitivity
- Adjustable eraser size
- Live FPS monitoring
- Export support:
  - PNG
  - JPEG
  - SVG
  - JSON
- Multiple camera support
- Grid coordinate visualization
- Canvas flip, invert, and fill tools
- Modern futuristic UI with TailwindCSS

---

# Tech Stack

- HTML5
- CSS3
- JavaScript
- MediaPipe Hands
- TailwindCSS
- Canvas API

---

# Hand Gestures

| Gesture | Action |
|----------|--------|
| Right Hand Pinch | Draw |
| Left Hand Open Palm | Erase |

---

# Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/visualDraw.git
```

## Open the project folder

```bash
cd visualDraw
```

## Run locally

Use VS Code Live Server or any local server.

---

# MediaPipe CDN Used

```html
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
```

---

# Project Structure

```bash
visualDraw/
│
├── index.html
├── README.md
└── assets/
```

---

# Core Functionalities

## Drawing Engine

- Grid-based pixel drawing
- Real-time rendering
- Shape-aware brush logic

## Gesture Recognition

- Pinch detection
- Open palm recognition
- Multi-hand tracking

## Export Engine

Supports exporting artwork as:

- PNG
- JPEG
- SVG
- JSON matrix data

---

# Controls

| Control | Function |
|----------|----------|
| Grid Slider | Change grid size |
| Brush Slider | Change brush size |
| Opacity Slider | Adjust opacity |
| Shape Buttons | Change brush shape |
| Export Buttons | Download artwork |
| Toggle Switches | Show/hide overlays |

---

# Future Improvements

- AI shape recognition
- Multiplayer collaborative canvas
- Undo/Redo stack
- Gesture customization
- Mobile optimization
- Save/load projects

---

# Screenshots

Add screenshots here:

```md
![Preview](preview.png)
```

---

# Browser Support

- Chrome
- Edge
- Brave

Recommended: Latest Chromium-based browser.

---

# License

MIT License

---

# Author

Ashwin Jain  
Web Developer & Creative Programmer

Portfolio: http://codemaster.infinityfreeapp.com

---

# Acknowledgements

- MediaPipe
- TailwindCSS
- Google Fonts
- HTML5 Canvas API