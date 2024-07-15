import asyncio
import browsers as br
from .config import config
from threading import Thread
from pyppeteer import launch
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
from .page_view import html_updater, audio_player
from webview.scripts.html_updater import html_updater_script
from webview.scripts.audio_player import audio_player_script


page, browser = None, None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # if browsers := list(br.browsers()):
    #     br.launch(browsers[0].get("browser_type"), url=f"http://{config.host}:{config.port}/")
    yield


app = FastAPI(lifespan=lifespan)
AUDIO_PLAYER_ENDPOINT = "ws-audio-player"
HTML_UPDATER_ENDPOINT = "ws-html-updater"


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
            [=[html_updater_script]=]
            [=[audio_player_script]=]
        </script>
    </body>
    </html>"""
    html = html.replace("[=[html_updater_script]=]", html_updater_script)
    html = html.replace("[=[audio_player_script]=]", audio_player_script)
    html = html.replace("[=[host]=]", config.host)
    html = html.replace("[=[title]=]", config.title)
    html = html.replace("[=[port]=]", str(config.port))
    html = html.replace("[=[html_updater_endpoint]=]", HTML_UPDATER_ENDPOINT)
    html = html.replace("[=[audio_player_endpoint]=]", AUDIO_PLAYER_ENDPOINT)
    return HTMLResponse(html)

@app.websocket(f"/{HTML_UPDATER_ENDPOINT}")
async def html_updater_socket(websocket: WebSocket):
    """
    Handle WebSocket connections.
    
    Args:
        websocket (WebSocket): The WebSocket connection object.
    """
    try:
        await html_updater.connect(websocket)
    except Exception as e:
        if config.debug:
            print(f"Client browser disconnected from html updater socket: {str(e)}")
        
@app.websocket(f"/{AUDIO_PLAYER_ENDPOINT}")
async def audio_playback_socket(websocket: WebSocket):
    try:
        await audio_player.connect(websocket)
    except Exception as e:
        if config.debug:
            print(f"Client browser disconnected from audio playback socket: {str(e)}")

async def start_browser():
    global browser, page
    browser = await launch(
        headless=False, 
        args=config.get_browser_args(),
        ignoreDefaultArgs=['--enable-automation']
    )
    page = await browser.pages()
    page = page[0]
    await page.setViewport({'width': 0, 'height': 0})
    await page.goto(f"http://{config.host}:{config.port}/")
    await page.evaluate('''document.body.style.overflow='hidden';''')

def run_app():
    """
    Run the FastAPI application using uvicorn
    """
    import uvicorn
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
    asyncio.create_task(start_browser())
    
