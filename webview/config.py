class Config:
    """
    Configuration class for the WebView application.

    This class manages the configuration settings for the WebView application,
    including the host, port, and debug mode.

    Attributes:
        title (str): The title to be shown on the browser tab.
        host (str): The host address for the server. Defaults to "127.0.0.1".
        port (int): The port number for the server. Defaults to 8080.
        debug (bool): Whether debug mode is enabled. Defaults to False.

    Example:
        >>> from webview import config
        >>> config.set(title="my server", host="localhost", port=5000, debug=True)
        >>> print(config.title, config.host, config.port, config.debug)
        localhost 5000 True
    """
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        self.debug = False
        self.title = "Webview Server"

    def set(self, title=None, host=None, port=None, debug=None):
        """
        Set the configuration parameters for the WebView application.

        Args:
            title (str): The title to be shown on the browser tab.
            host (str, optional): The host address for the server.
            port (int, optional): The port number for the server.
            debug (bool, optional): Whether to enable debug mode.

        Example:
            >>> from webview import config
            >>> config.set(title="my-webview", host="0.0.0.0", port=3000, debug=True)
        """
        if title is not None:
            self.title = title
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug
            
config = Config()