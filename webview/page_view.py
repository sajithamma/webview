import asyncio
from .config import Config
from fastapi import WebSocket, WebSocketDisconnect


class HTMLUpdater:
    """
    HTMLUpdater class for managing and updating the WebView content.

    This class handles the HTML content of the WebView, manages WebSocket
    connections, and provides methods for updating the view.

    Attributes:
        change_detected (bool): Indicates if a change in the HTML content has been made.
        html_content (str): The current HTML content of the WebView.
        client (WebSocket): The WebSocket client connection.
        config (Config): The configuration object for the WebView.

    Example:
        >>> from webview import webview, config
        >>> config.set(debug=True)
        >>> webview.bind_config(config)
        >>> webview.update_view("<h1>Hello, World!</h1>")
    """
    def __init__(self):
        self.config = None
        self.change_detected = True
        self.client: WebSocket = None
        self.html_content = ""
        
    def bind_config(self, config: Config):
        """
        Bind a configuration object to the HTMLUpdater.

        Args:
            config (Config): The configuration object to bind.

        Example:
            >>> from webview import webview, config
            >>> config.set(debug=True)
            >>> webview.bind_config(config)
        """
        self.config=config 

    def update_view(self, new_html: str):
        """
        Update the HTML content of the WebView.

        This method can be called from a synchronous context.

        Args:
            new_html (str): The new HTML content to set.

        Example:
            >>> from webview import webview
            >>> webview.update_view("<h1>New Content</h1>")
        """
        self.html_content = new_html
        self.change_detected = True
        self.__try_send_update__()
        
    async def async_update_view(self, new_html: str): 
        """
        Asynchronously update the HTML content of the WebView.

        This method should be called from an asynchronous context.

        Args:
            new_html (str): The new HTML content to set.

        Example:
            >>> import asyncio
            >>> from webview import webview
            >>> async def update():
            ...     await webview.async_update_view("<h1>Async Update</h1>")
            >>> asyncio.run(update())
        """
        self.html_content = new_html
        self.change_detected = True
        await self.__send_update__()
        
    def __try_send_update__(self):
        """
        Attempt to send an update to the client.

        This method handles both synchronous and asynchronous contexts.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            loop.create_task(self.__send_update__())
        else:
            loop.run_until_complete(self.__send_update__())
        
    async def __send_update__(self):
        """
        Send an update to the connected WebSocket client.
        """
        if self.client:
            await self.client.send_text(self.html_content)
            if self.config and self.config.debug:
                print("Webview: View updated")
        elif self.config and self.config.debug:
            print("Webview: Client is not available for UI updates")
            

    async def connect_view(self, websocket: WebSocket):
        """
        Handle a new WebSocket connection.

        This method is called when a new WebSocket connection is established.

        Args:
            websocket (WebSocket): The WebSocket connection object.
        """
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected")
        try:
            while True:
                if self.change_detected:
                    await websocket.send_text(self.html_content)
                    self.change_detected = False
                await websocket.receive_text()
        finally:
            self.client = None

html_updater = HTMLUpdater()