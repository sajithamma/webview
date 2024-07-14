import uvicorn
import browsers as br
from .config import config
from threading import Thread
from .page_view import html_updater
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    if browsers := list(br.browsers()):
        br.launch(browsers[0].get("browser_type"), url=f"http://{config.host}:{config.port}/")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the main HTML page.
    
    Returns:
        HTMLResponse: The rendered HTML template.
    """
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>[=[title]=]</title>
        <style>
            html, body, #main_update_content {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div id="main_update_content"></div>
        <script>
            const socket = new WebSocket(`ws://[=[host]=]:[=[port]=]/ws`);
            socket.onmessage = function(event) {
                document.getElementById("main_update_content").innerHTML = event.data;
            };
            
            let mediaRecorder;
            let audioChunks = [];
            
            async function startRecording() {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                    if (audioChunks.length > 0) {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        const reader = new FileReader();
                        reader.readAsDataURL(audioBlob);
                        reader.onloadend = () => {
                            const base64data = reader.result.split(',')[1];
                            socket.send(JSON.stringify({ type: 'audio', data: base64data }));
                        }
                        audioChunks = [];
                    }
                };
                mediaRecorder.start(100);
            }
            
            function stopRecording() {
                if (mediaRecorder) {
                    mediaRecorder.stop();
                }
            }

            function playAudio(audioData) {
                const audio = new Audio(audioData);
                audio.play();
            }
            
            socket.onmessage = function(event) {
                const message = JSON.parse(event.data);
                if (message.type === 'html') {
                    document.getElementById("main_update_content").innerHTML = message.data;
                } else if (message.type === 'audio') {
                    playAudio(message.data);
                } else if (message.type === 'command') {
                    if (message.data === 'start_listening') {
                        startRecording();
                    } else if (message.data === 'stop_listening') {
                        stopRecording();
                    }
                }
            };
        </script>
    </body>
    </html>"""
    html = html.replace("[=[host]=]", config.host)
    html = html.replace("[=[port]=]", str(config.port))
    html = html.replace("[=[title]=]", config.title)
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections.
    
    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    try:
        await html_updater.connect_view(websocket)
    except Exception as e:
        print(f"Client browser disconnected: {str(e)}")

def run_app():
    """
    Run the FastAPI application using uvicorn
    """
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)

def start_app():
    """
    Start the FastAPI application in a separate thread.

    This function creates a new thread to run the FastAPI application,
    allowing the main thread to continue execution.

    Example:
        >>> from webview import start_app
        >>> start_app()
        >>> # The app is now running in the background
    """
    thread = Thread(target=run_app, daemon=True)
    thread.start()
    
