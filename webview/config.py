class Config:
    """
    Configuration class for the WebView application.

    This class manages the configuration settings for the WebView application,
    including server settings, debug mode, and browser options.

    Attributes:
        title (str): The title to be shown on the browser tab.
        host (str): The host address for the server. Defaults to "127.0.0.1".
        port (int): The port number for the server. Defaults to 8080.
        debug (bool): Whether debug mode is enabled. Defaults to False.
        log_level (str): The logging verbosity for the fastapi server. Defaults to "warning".
        kiosk_mode (bool): Runs the browser in kiosk mode, which is a fullscreen mode without any browser UI.
        orientation (str): Sets the orientation to either "landscape" or "portrait". Note that forcing orientation might not work on all systems and might require additional setup.
        window_size (tuple): Sets a specific window size (width and height).
        
    Example:
        >>> from webview import config
        >>> config.set(title="my server", host="localhost", port=5000, debug=True, kiosk_mode=False)
        >>> print(config.title, config.host, config.port, config.debug, config.kiosk_mode)
        my server localhost 5000 True False
    """
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        self.debug = False
        self.kiosk_mode = False
        self.window_size = None
        self.log_level = "warning"
        self.title = "Webview Server"
        self.orientation = "landscape"
        
    def set(self, title=None, host=None, port=None, debug=None, log_level=None, kiosk_mode=False, orientation=None, window_size=None):
        """
        Set the configuration parameters for the WebView application.

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
            >>> from webview import config
            >>> config.set(title="my-webview", host="0.0.0.0", port=3000, debug=True, kiosk_mode=False)
        """
        if title is not None:
            self.title = title
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug
        if log_level is not None:
            self.log_level = log_level
        if kiosk_mode is not None:
            self.kiosk_mode = kiosk_mode
        if orientation is not None:
            self.orientation = orientation
        if window_size is not None:
            self.window_size = window_size

    def get_browser_args(self):
        """
        Get the browser launch arguments based on the current configuration.

        Returns:
            list: A list of string arguments to be passed to the browser launch function.
        """
        args = [
            '--no-first-run',
            '--start-maximized',
            '--disable-infobars',
            '--no-default-browser-check',
            '--autoplay-policy=no-user-gesture-required'
        ]
        if self.kiosk_mode:
            args.append('--kiosk')
        if self.orientation=='portrait':
            args.extend(['--force-device-scale-factor=1', '--force-device-orientation=portrait'])
        if self.window_size:
            args.append(f'--window-size={self.window_size[0]},{self.window_size[1]}')
        return args

config = Config()