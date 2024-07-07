import uvicorn
from .config import config
from threading import Thread
from .page_view import html_updater
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket, Request

app = FastAPI()
templates = Jinja2Templates(directory="webview/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the main HTML page.
    
    Args:
        request (Request): The incoming request object.
        
    Returns:
        TemplateResponse: The rendered HTML template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections.
    
    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    await html_updater.connect_view(websocket)

def run_app():
    """
    Run the FastAPI application using uvicorn
    """
    uvicorn.run(app, host=config.host, port=config.port)

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