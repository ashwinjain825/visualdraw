from flask import Flask, render_template_string, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    html_layout = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gesture To Text</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
        <style>
            body { font-family: 'Inter', sans-serif; }
        </style>
    </head>
    <body class="bg-slate-50 text-slate-800 h-screen flex flex-col overflow-hidden">

        <header class="h-16 bg-white border-b border-slate-100 flex items-center justify-between px-6 z-10 shrink-0">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-lg shadow-sm shadow-indigo-200">
                    S
                </div>
                <span class="text-lg font-semibold tracking-tight text-slate-900">Signify <span class="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full ml-1">v1.0</span></span>
            </div>
            <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 rounded-full">
                    <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                    <span class="text-xs font-medium text-emerald-700">Camera Active</span>
                </div>
                <button class="p-2 hover:bg-slate-50 rounded-full transition-colors text-slate-500">
                    <span class="material-symbols-outlined block">settings</span>
                </button>
            </div>
        </header>

        <div class="flex flex-1 overflow-hidden">
            <aside class="w-64 bg-white border-r border-slate-100 flex flex-col justify-between p-4 shrink-0">
                <div class="space-y-1">
                    <a href="#" class="flex items-center gap-3 px-4 py-3 bg-indigo-50 text-indigo-600 rounded-xl font-medium transition-all">
                        <span class="material-symbols-outlined">dashboard</span>
                        <span>Workspace</span>
                    </a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-slate-50 hover:text-slate-900 rounded-xl font-medium transition-all">
                        <span class="material-symbols-outlined">history</span>
                        <span>History</span>
                    </a>
                    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-slate-50 hover:text-slate-900 rounded-xl font-medium transition-all">
                        <span class="material-symbols-outlined">analytics</span>
                        <span>Analytics</span>
                    </a>
                </div>
                
                <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">System Status</span>
                    <div class="flex justify-between text-xs font-medium text-slate-600">
                        <span>FPS</span>
                        <span class="text-indigo-600">30.0</span>
                    </div>
                </div>
            </aside>

            <main class="flex-1 p-8 flex gap-8 overflow-hidden">
                <div class="flex-1 bg-white rounded-2xl border border-slate-100 p-4 flex flex-col shadow-sm">
                    <div class="flex items-center justify-between mb-4 px-2">
                        <h2 class="font-semibold text-slate-900 flex items-center gap-2">
                            <span class="material-symbols-outlined text-slate-400">videocam</span> Live Feed
                        </h2>
                    </div>
                    <div class="flex-1 bg-slate-900 rounded-xl overflow-hidden relative flex items-center justify-center min-h-0">
                        <img src="/video_feed" class="w-full h-full object-cover">
                    </div>
                </div>

                <div class="w-96 bg-white rounded-2xl border border-slate-100 p-6 flex flex-col shadow-sm shrink-0">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="font-semibold text-slate-900 flex items-center gap-2">
                            <span class="material-symbols-outlined text-slate-400">translate</span> Real-time Output
                        </h2>
                        <button class="text-xs font-medium text-slate-400 hover:text-slate-600 flex items-center gap-1">
                            <span class="material-symbols-outlined text-sm">delete</span> Clear
                        </button>
                    </div>
                    
                    <div class="flex-1 bg-slate-50 rounded-xl p-5 border border-slate-100 flex flex-col overflow-y-auto">
                        <p class="text-slate-400 text-sm font-light italic">Waiting for gestures...</p>
                        <p class="text-2xl font-medium text-slate-800 tracking-wide leading-relaxed mt-2 hidden">HELLO WORLD</p>
                    </div>

                    <div class="mt-6 pt-6 border-t border-slate-100 flex gap-3">
                        <button class="flex-1 py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-medium shadow-sm transition-colors text-sm flex items-center justify-center gap-2">
                            <span class="material-symbols-outlined text-lg">content_copy</span> Copy Text
                        </button>
                        <button class="py-3 px-4 border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-xl font-medium transition-colors text-sm flex items-center justify-center">
                            <span class="material-symbols-outlined text-lg">volume_up</span>
                        </button>
                    </div>
                </div>
            </main>
        </div>

    </body>
    </html>
    """
    return render_template_string(html_layout)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)