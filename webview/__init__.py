import time, asyncio
from .app import start_app
from .config import config, Config
from .page_view import html_updater, HTMLUpdater

class WebView:
    """
    WebView class for managing the web-based user interface.

    This class provides a high-level interface for configuring, starting,
    and updating a web-based view. It encapsulates the configuration and
    HTML updating functionality, offering a simplified API for users.

    Attributes:
        config (Config): Configuration object for the WebView.
        html_updater (HTMLUpdater): Object responsible for updating the HTML content.

    Example:
        >>> from webview import Webview
        >>> Webview.configure(host="localhost", port=5000, debug=True)
        >>> Webview.start_webview()
        >>> asyncio.run(Webview.update_view("<h1>Hello, World!</h1>"))
    """
    def __init__(self, config: Config, html_updater: HTMLUpdater):
        """
        Initialize a WebView instance.

        Args:
            config (Config): Configuration object for the WebView.
            html_updater (HTMLUpdater): Object responsible for updating the HTML content.
        """
        self.config  = config
        self.html_updater = html_updater

    def configure(self, title="Webview App", host: str="127.0.0.1", port: int=8080, debug: bool=True, log_level: str="warning"):
        """
        Configure the WebView settings.

        Args:
            title (str): The title to be shown on the browser tab.
            host (str, optional): The host address for the server. Defaults to "127.0.0.1".
            port (int, optional): The port number for the server. Defaults to 8080.
            debug (bool, optional): Whether to enable debug mode. Defaults to True.
            log_level (str, optional): The logging verbosity for the FastAPI server.
            
        Example:
            >>> from webview import Webview
            >>> Webview.configure(title="My App", host="0.0.0.0", port=3000, debug=False)
        """
        self.config.set(title, host, port, debug, log_level)
    
    def start_webview(self) -> bool:
        """
        Start the WebView application.

        This method starts the FastAPI application in a separate thread and
        waits for 2 seconds to allow the server to initialize.

        Returns:
            bool: True if the WebView was successfully started.

        Example:
            >>> from webview import Webview
            >>> success = Webview.start_webview()
            >>> print("WebView started successfully" if success else "Failed to start WebView")
        """
        if self.config.debug:
            print("Webview: Starting the webview server...")
        start_app()
        time.sleep(2)
        print(f"Webview: Webview server started, you can view it at http://{self.config.host}:{self.config.port}/")
        return True
    
    async def update_view(self, html: str):
        """
        Asynchronously update the HTML content of the WebView.

        Args:
            html (str): The new HTML content to set.

        Example:
            >>> import asyncio
            >>> from webview import Webview
            >>> async def update():
            ...     await Webview.update_view("<h1>New Content</h1>")
            >>> asyncio.run(update())
        """
        await self.html_updater.async_update_view(html)

    async def start_listening(self, callback):
        """
        Start listening for audio input from the browser.

        This method sends a command to the browser to start recording audio
        and sets up a callback function to process the incoming audio data.

        Args:
            callback (callable): An asynchronous function that will be called
                                 with the audio data as it's received.

        Example:
            >>> import asyncio
            >>> from webview import Webview
            >>> async def process_audio(audio_bytes):
            ...     print(f"Received {len(audio_bytes)} bytes of audio")
            >>> async def main():
            ...     await Webview.start_listening(process_audio)
            ...     await asyncio.sleep(10)  # Listen for 10 seconds
            ...     await Webview.stop_listening()
            >>> asyncio.run(main())
        """
        await self.html_updater.start_listening(callback)
        
    async def stop_listening(self):
        """
        Stop listening for audio input from the browser.

        This method sends a command to the browser to stop recording audio.

        Example:
            >>> import asyncio
            >>> from webview import Webview
            >>> async def main():
            ...     await Webview.start_listening(lambda x: None)
            ...     await asyncio.sleep(5)  # Listen for 5 seconds
            ...     await Webview.stop_listening()
            >>> asyncio.run(main())
        """
        await self.html_updater.stop_listening()
    
    async def play_audio(self, audio: str):
        """
        Play audio in the browser.

        This method sends audio data to the browser for playback.

        Args:
            audio (str): A base64-encoded string of the audio data to play.

        Example:
            >>> import asyncio
            >>> from webview import Webview
            >>> async def play_sample_audio():
            ...     sample_audio = "data:audio/wav;base64,UklGRjIAAABXQVZFZm10IBIAAAABAAEAQB8AAEAfAAABAAgAZGF0YRAAAAAAAAAAAAAAAAAAAAAAAA=="
            ...     await Webview.play_audio(sample_audio)
            >>> asyncio.run(play_sample_audio())
        """
        await self.html_updater.play_audio(audio)

Webview = WebView(config=config, html_updater=html_updater)