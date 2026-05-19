from flask import Flask, render_template_string

app = Flask(__name__)

# Suppress the default log line spamming in the terminal console
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route('/')
def index():
    html_layout = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Signify - Grid Canvas Painter</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
        
        <!-- MediaPipe Engine CDN Packages -->
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>

        <style>
            body { font-family: 'Inter', sans-serif; }
        </style>
    </head>
    <body class="bg-slate-50 text-slate-800 h-screen flex flex-col overflow-hidden">

        <!-- Top Navigation Header Bar -->
        <header class="h-16 bg-white border-b border-slate-100 flex items-center justify-between px-6 z-10 shrink-0">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-sm shadow-indigo-200">
                    S
                </div>
                <span class="text-lg font-semibold tracking-tight text-slate-900">Signify Canvas <span class="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full ml-1">v2.0</span></span>
            </div>
            <div class="flex items-center gap-6">
                <div id="mode-badge" class="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-full text-xs font-medium text-slate-600 transition-all">
                    <span id="mode-dot" class="w-2 h-2 bg-slate-400 rounded-full"></span>
                    <span id="mode-text">Hovering Mode</span>
                </div>
                <button onclick="clearCanvasGrid()" class="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 hover:bg-slate-50 rounded-xl text-xs font-medium text-slate-600 transition-colors">
                    <span class="material-symbols-outlined text-sm">delete_sweep</span> Reset Grid
                </button>
            </div>
        </header>

        <!-- Main Workspace Application Frame -->
        <div class="flex flex-1 overflow-hidden">
            <main class="flex-1 p-8 flex gap-8 justify-center items-center overflow-hidden">
                <div class="w-full max-w-4xl aspect-[4/3] bg-white rounded-2xl border border-slate-100 p-4 flex flex-col shadow-sm h-full">
                    <div class="flex items-center justify-between mb-3 px-2">
                        <h2 class="font-semibold text-slate-900 flex items-center gap-2 text-sm">
                            <span class="material-symbols-outlined text-slate-400">draw</span> Gestural 20x20 Matrix Canvas
                        </h2>
                        <span class="text-xs text-slate-400 font-medium">Right: Pinch to Draw | Left: Open Hand to Erase</span>
                    </div>
                    
                    <div class="flex-1 bg-slate-950 rounded-xl overflow-hidden relative flex items-center justify-center min-h-0 shadow-inner">
                        <video id="input_video" class="hidden" autoplay playsinline></video>
                        <!-- Canvas layer matches video frame width and displays the mirror graphics -->
                        <canvas id="output_canvas" class="w-full h-full object-cover transform -scale-x-100"></canvas>
                    </div>
                </div>
            </main>
        </div>

        <script>
            const videoElement = document.getElementById('input_video');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            
            const modeBadge = document.getElementById('mode-badge');
            const modeDot = document.getElementById('mode-dot');
            const modeText = document.getElementById('mode-text');

            const GRID_SIZE = 20;
            // Initialize 2D matrix structure to track structural changes inside grid coordinates
            let gridMatrix = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false));

            function clearCanvasGrid() {
                gridMatrix = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false));
            }

            function onResults(results) {
                if (canvasElement.width !== videoElement.videoWidth) {
                    canvasElement.width = videoElement.videoWidth;
                    canvasElement.height = videoElement.videoHeight;
                }

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                
                // Render the clean raw background stream camera view inside viewport bounds
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

                const cellWidth = canvasElement.width / GRID_SIZE;
                const cellHeight = canvasElement.height / GRID_SIZE;

                let activeMode = "Hovering Mode";

                if (results.multiHandLandmarks && results.multiHandedness) {
                    for (let i = 0; i < results.multiHandLandmarks.length; i++) {
                        const landmarks = results.multiHandLandmarks[i];
                        
                        // MediaPipe mirrors classification labels; adjust string bounds to check true relative positioning
                        const isLeftHand = results.multiHandedness[i].label === 'Right'; 

                        if (!isLeftHand) { 
                            // --- DRAWING LOGIC (RIGHT HAND) ---
                            // Calculate simple 3D vector distance formula metrics across pinch parameters
                            const thumbTip = landmarks[4];
                            const indexTip = landmarks[8];
                            const distance = Math.sqrt(
                                Math.pow(thumbTip.x - indexTip.x, 2) + 
                                Math.pow(thumbTip.y - indexTip.y, 2) + 
                                Math.pow(thumbTip.z - indexTip.z, 2)
                            );

                            // Draw structural guide ring highlights over active control index position loops
                            canvasCtx.beginPath();
                            canvasCtx.arc(indexTip.x * canvasElement.width, indexTip.y * canvasElement.height, 8, 0, 2 * Math.PI);
                            canvasCtx.fillStyle = '#6366f1';
                            canvasCtx.fill();

                            // Pinch threshold check
                            if (distance < 0.04) {
                                activeMode = "Drawing Mode";
                                // Convert relative positional ratios back down into integers matching grid matrices
                                const gridX = Math.floor(indexTip.x * GRID_SIZE);
                                const gridY = Math.floor(indexTip.y * GRID_SIZE);

                                if (gridX >= 0 && gridX < GRID_SIZE && gridY >= 0 && gridY < GRID_SIZE) {
                                    gridMatrix[gridY][gridX] = true; 
                                }
                            }
                        } else {
                            // --- ERASER LOGIC (LEFT HAND) ---
                            const indexUp = landmarks[8].y < landmarks[6].y;
                            const middleUp = landmarks[12].y < landmarks[10].y;
                            const ringUp = landmarks[16].y < landmarks[14].y;
                            const pinkyUp = landmarks[20].y < landmarks[18].y;

                            // Highlight Left palm positional coordinates inside workspace zones
                            const palmBase = landmarks[9];
                            canvasCtx.beginPath();
                            canvasCtx.arc(palmBase.x * canvasElement.width, palmBase.y * canvasElement.height, 10, 0, 2 * Math.PI);
                            canvasCtx.fillStyle = '#ef4444';
                            canvasCtx.fill();

                            // Trigger structural erasure if left hand matrix configuration checks out open
                            if (indexUp && middleUp && ringUp && pinkyUp) {
                                activeMode = "Eraser Mode";
                                const gridX = Math.floor(palmBase.x * GRID_SIZE);
                                const gridY = Math.floor(palmBase.y * GRID_SIZE);

                                if (gridX >= 0 && gridX < GRID_SIZE && gridY >= 0 && gridY < GRID_SIZE) {
                                    gridMatrix[gridY][gridX] = false;
                                }
                            }
                        }
                    }
                }

                // Render current active layout parameters inside our HTML document blocks
                updateModeUI(activeMode);

                // --- CANVAS GRAPHICS RENDERING LAYER ---
                // Draw 70% opacity active cells
                for (let y = 0; y < GRID_SIZE; y++) {
                    for (let x = 0; x < GRID_SIZE; x++) {
                        if (gridMatrix[y][x]) {
                            canvasCtx.fillStyle = 'rgba(34, 197, 94, 0.7)';
                            canvasCtx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
                        }
                    }
                }

                // Draw structural grid system overlay grid borders
                canvasCtx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                canvasCtx.lineWidth = 1;
                for (let i = 0; i <= GRID_SIZE; i++) {
                    // Vertical dividing columns
                    canvasCtx.beginPath();
                    canvasCtx.moveTo(i * cellWidth, 0);
                    canvasCtx.lineTo(i * cellWidth, canvasElement.height);
                    canvasCtx.stroke();

                    // Horizontal dividing lines
                    canvasCtx.beginPath();
                    canvasCtx.moveTo(0, i * cellHeight);
                    canvasCtx.lineTo(canvasElement.width, i * cellHeight);
                    canvasCtx.stroke();
                }

                canvasCtx.restore();
            }

            function updateModeUI(mode) {
                modeText.innerText = mode;
                if (mode === "Drawing Mode") {
                    modeBadge.className = "flex items-center gap-2 px-3 py-1.5 bg-emerald-50 rounded-full text-xs font-medium text-emerald-700 transition-all";
                    modeDot.className = "w-2 h-2 bg-emerald-500 rounded-full animate-pulse";
                } else if (mode === "Eraser Mode") {
                    modeBadge.className = "flex items-center gap-2 px-3 py-1.5 bg-rose-50 rounded-full text-xs font-medium text-rose-700 transition-all";
                    modeDot.className = "w-2 h-2 bg-rose-500 rounded-full animate-bounce";
                } else {
                    modeBadge.className = "flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-full text-xs font-medium text-slate-600 transition-all";
                    modeDot.className = "w-2 h-2 bg-slate-400 rounded-full";
                }
            }

            const hands = new Hands({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
            });
            
            hands.setOptions({
                maxNumHands: 2, // Track both hands simultaneously
                modelComplexity: 1,
                minDetectionConfidence: 0.7,
                minTrackingConfidence: 0.6
            });
            hands.onResults(onResults);

            const camera = new Camera(videoElement, {
                onFrame: async () => {
                    await hands.send({image: videoElement});
                },
                width: 640,
                height: 480
            });
            camera.start();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_layout)

if __name__ == '__main__':
    app.run(debug=True)