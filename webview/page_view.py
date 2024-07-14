from .config import Config
import asyncio, json, base64
from fastapi import WebSocket, WebSocketDisconnect


class HTMLUpdater:
    """
    HTMLUpdater class for managing and updating the WebView content.

    This class handles the HTML content of the WebView, manages WebSocket
    connections, and provides methods for updating the view and handling audio.

    Attributes:
        change_detected (bool): Indicates if a change in the HTML content has been made.
        html_content (str): The current HTML content of the WebView.
        client (WebSocket): The WebSocket client connection.
        config (Config): The configuration object for the WebView.
        is_listening (bool): Indicates if the WebView is currently listening for audio.
        audio_callback (callable): Callback function for handling received audio data.

    Example:
        >>> from webview import webview, config
        >>> config.set(debug=True)
        >>> webview.bind_config(config)
        >>> webview.update_view("<h1>Hello, World!</h1>")
    """
    def __init__(self):
        """
        Initialize the HTMLUpdater instance.

        Sets up initial values for all attributes.
        """
        self.config = None
        self.html_content = ""
        self.is_listening = False
        self.audio_callback = None
        self.change_detected = True
        self.client: WebSocket = None
        
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
        It creates or uses an existing event loop to send the update.

        Note: This is an internal method and should not be called directly.
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

        This method sends the current HTML content to the client if one is connected.
        If debug mode is enabled, it prints status messages.

        Note: This is an internal method and should not be called directly.
        """
        if self.client:
            await self.client.send_text(json.dumps({"type": "html", "data": self.html_content}))
            if self.config and self.config.debug:
                print("Webview: View updated")
        elif self.config and self.config.debug:
            print("Webview: Client is not available for UI updates")

    async def start_listening(self, callback):
        """
        Start listening for audio input from the client.

        This method sends a command to the client to start audio input and sets up
        the callback for handling received audio data.

        Args:
            callback (callable): A function to be called with received audio data.

        Example:
            >>> import asyncio
            >>> from webview import webview
            >>> 
            >>> async def audio_callback(audio_data):
            ...     print(f"Received {len(audio_data)} bytes of audio data")
            >>> 
            >>> async def start_audio_listening():
            ...     await webview.start_listening(audio_callback)
            >>> 
            >>> asyncio.run(start_audio_listening())
        """
        if self.client:
            self.audio_callback = callback
            await self.client.send_text(json.dumps({"type": "command", "data": "start_listening"}))
            self.is_listening = True
            if self.config and self.config.debug:
                print("Webview: Started listening")
        elif self.config and self.config.debug:
            print("Webview: Client is not available to start listening")
            
    async def stop_listening(self):
        """
        Stop listening for audio input from the client.

        This method sends a command to the client to stop audio input and clears
        the audio callback.

        Example:
            >>> import asyncio
            >>> from webview import webview
            >>> 
            >>> async def stop_audio_listening():
            ...     await webview.stop_listening()
            >>> 
            >>> asyncio.run(stop_audio_listening())
        """
        if self.client:
            await self.client.send_text(json.dumps({"type": "command", "data": "stop_listening"}))
            self.is_listening = False
            self.audio_callback = None
            if self.config and self.config.debug:
                print("Webview: Stopped listening")
        elif self.config and self.config.debug:
            print("Webview: Client is not available to stop listening")

    async def play_audio(self, audio_data: str):
        """
        Play audio data through the WebSocket connection.

        This method sends the provided audio data to the client for playback.
        The audio data should be a base64-encoded string of the audio file.

        Args:
            audio_data (str): A base64-encoded string of the audio data to be played.

        Raises:
            RuntimeError: If the WebSocket client is not connected.

        Example:
            >>> import asyncio
            >>> from webview import webview
            >>> 
            >>> async def play_sample_audio():
            ...     # Assume we have a base64-encoded audio string
            ...     sample_audio = "SGVsbG8sIHRoaXMgaXMgYSBzYW1wbGUgYXVkaW8u"
            ...     await webview.play_audio(sample_audio)
            >>> 
            >>> asyncio.run(play_sample_audio())
        """
        if self.client:
            await self.client.send_text(json.dumps({"type": "audio", "data": audio_data}))
            if self.config and self.config.debug:
                print("Webview: Audio sent for playback")
        elif self.config and self.config.debug:
            print("Webview: Client is not available to play audio")


    async def connect_view(self, websocket: WebSocket):
        """
        Handle a new WebSocket connection.

        This method is called when a new WebSocket connection is established.
        It sets up the client connection and handles incoming messages.

        Args:
            websocket (WebSocket): The WebSocket connection object.

        Note: This method is typically called by the WebSocket server framework
        and not directly by the user.

        Example:
            >>> # This would typically be part of your FastAPI app setup
            >>> @app.websocket("/ws")
            >>> async def websocket_endpoint(websocket: WebSocket):
            ...     await webview.connect_view(websocket)
        """
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected")
        try:
            while True:
                if self.change_detected:
                    await websocket.send_text(json.dumps({"type": "html", "data": self.html_content}))
                    self.change_detected = False
                data = await websocket.receive_text()
                message = json.loads(data)
                if message["type"] == "audio":
                    # Handle incoming audio data
                    if self.config and self.config.debug:
                        print("Webview: Received audio data")
                    if self.audio_callback:
                        audio_bytes = base64.b64decode(message["data"])
                        await self.audio_callback(audio_bytes)
        finally:
            self.client = None

html_updater = HTMLUpdater()