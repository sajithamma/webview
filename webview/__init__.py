import time
from .app import start_app
from .config import config, Config
from .page_view import html_updater, HTMLUpdater, audio_player, AudioPlayer

class WebView:
    """
    WebView class for managing the web-based user interface.

    This class provides a high-level interface for configuring, starting,
    and updating a web-based view. It encapsulates the configuration and
    HTML updating functionality, offering a simplified API for users.

    Attributes:
        config (Config): Configuration object for the WebView.
        html_updater (HTMLUpdater): Object responsible for updating the HTML content.
        audio_player (AudioPlayer): Object responsible for handling audio playback.

    Example:
        >>> from webview import WebView
        >>> WebView.configure(host="localhost", port=5000, debug=True)
        >>> WebView.start_webview()
        >>> WebView.update_view("<h1>Hello, World!</h1>")
    """
    def __init__(self, config: Config, html_updater: HTMLUpdater, audio_player: AudioPlayer):
        """
        Initialize a WebView instance.

        Args:
            config (Config): Configuration object for the WebView.
            html_updater (HTMLUpdater): Object responsible for updating the HTML content.
            audio_player (AudioPlayer): Object responsible for handling audio playback.
        """
        self.config  = config
        self.html_updater = html_updater
        self.audio_player = audio_player

    def configure(self, title="Webview App", host: str="127.0.0.1", port: int=8080, debug: bool=True, log_level: str="warning", kiosk_mode=False, orientation="landscape", window_size=None):
        """
        Configure the WebView settings.

        Args:
            title (str, optional): The title to be shown on the browser tab.
            host (str, optional): The host address for the server.
            port (int, optional): The port number for the server.
            debug (bool, optional): Whether to enable debug mode.
            log_level (str, optional): The logging verbosity for the fastapi server.
            headless (bool, optional): Whether to run the browser in headless mode.
            kiosk_mode (bool): Whether to start the browser in kiosk mode. Default to False.
            orientation (str): Sets the orientation to either "landscape" or "portrait". Note that forcing orientation might not work on all systems and might require additional setup.
            window_size (tuple): Sets a specific window size (width and height).
            
        Example:
            >>> WebView.configure(title="Webview App", host="0.0.0.0", port=3000, debug=False)
        """
        self.config.set(title, host, port, debug, log_level, kiosk_mode, orientation, window_size)
    
    def update_view(self, html: str):
        """
        Update the HTML content of the WebView.

        This method can be called from a synchronous context.

        Args:
            html (str): The new HTML content to set.

        Example:
            >>> Webview.update_view("<div>New content</div>")
        """
        self.html_updater.update_view(html)
        
    async def async_update_view(self, html: str):
        """
        Asynchronously update the HTML content of the WebView.

        This method should be called from an asynchronous context.

        Args:
            html (str): The new HTML content to set.

        Example:
            >>> import asyncio
            >>> async def update():
            ...     await Webview.async_update_view("<div>Async update</div>")
            >>> asyncio.run(update())
        """
        await self.html_updater.async_update_view(html)
        
    def play_audio(self, audio_data: str, delay: float=None) -> str:
        """
        Play audio data in the WebView.

        This method can be called from a synchronous context.

        Args:
            audio_data (str): The audio data to play.
            delay (float): A delay to start the audio play.

        Returns:
            str: The unique ID of the audio task.

        Example:
            >>> audio_id = WebView.play_audio("your_audio_data_here")
        """
        return self.audio_player.play_audio(audio_data, delay)
        
    async def async_play_audio(self, audio_data: str, delay: float=None) -> str:
        """
        Asynchronously play audio data in the WebView.

        This method should be called from an asynchronous context.

        Args:
            audio_data (str): The audio data to play.
            delay (float): A delay to start the audio play.

        Returns:
            str: The unique ID of the audio task.

        Example:
            >>> import asyncio
            >>> async def play():
            ...     audio_id = await WebView.async_play_audio("your_audio_data_here")
            >>> asyncio.run(play())
        """
        return await self.audio_player.async_play_audio(audio_data, delay)
    
    def wait_until_finish_play(self):
        """
        Wait until the current audio playback finishes.

        This method can be called from a synchronous context.

        Example:
            >>> WebView.wait_until_finish_play()
        """
        self.audio_player.wait_until_finish_play()
    
    async def async_wait_until_finish_play(self):
        """
        Asynchronously wait until the current audio playback finishes.

        This method should be called from an asynchronous context.

        Example:
            >>> import asyncio
            >>> async def wait():
            ...     await WebView.async_wait_until_finish_play()
            >>> asyncio.run(wait())
        """
        await self.audio_player.async_wait_until_finish_play()
    
    def start_webview(self) -> bool:
        """
        Start the WebView application.

        This method starts the FastAPI application in a separate thread and
        waits for 2 seconds to allow the server to initialize.

        Returns:
            bool: True if the WebView was successfully started.

        Example:
            >>> success = Webview.start_webview()
            >>> print("WebView started successfully" if success else "Failed to start WebView")
        """
        if self.config.debug:
            print("Webview: Starting the webview server...")
        start_app()
        time.sleep(2)
        print(f"Webview: Webview server started, you can view it at http://{self.config.host}:{self.config.port}/")
        return True


webview = WebView(
    config=config, 
    html_updater=html_updater, 
    audio_player=audio_player,
)