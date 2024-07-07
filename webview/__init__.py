import time
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
        >>> Webview.update_view("<h1>Hello, World!</h1>")
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
            log_level (str, optional): The logging verbosity for the fastapi server.
            
        Example:
            >>> Webview.configure(title="webview app", host="0.0.0.0", port=3000, debug=False)
        """
        self.config.set(title, host, port, debug, log_level)
    
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


Webview = WebView(config=config, html_updater=html_updater)