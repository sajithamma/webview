# webview



## Table of Contents

1. Introduction
2. Features
3. Installation
4. Project Structure
5. How It Works
6. Usage
7. API Reference
8. Examples
9. Contributing
10. License



## Introduction
WebView is a simple but versatile Python library designed to simplify the creation of GUI for your programs using web technologies. It leverages the power and ubiquity of web browsers to provide a consistent and platform-independent UI experience across different operating systems.

Key features and benefits of WebView include:

- Cross-Platform Compatibility: By utilizing web browsers as the rendering engine, WebView ensures consistent behavior across different operating systems, eliminating many platform-specific issues.

- System Resource Abstraction: WebView handles system-dependent operations like audio playback and recording through the browser, providing a unified API that works consistently across various platforms.

- Easy UI Updates: With a straightforward API, you can inject HTML content from anywhere in your program to update the UI dynamically. This allows for flexible and responsive user interfaces that can change based on your application's state or user interactions. 

- Asynchronous and Synchronous Support: WebView offers both asynchronous and synchronous methods for UI updates, audio playback, and recording, allowing integration with various programming paradigms and application architectures.

- Minimal Setup: Get started quickly with minimal configuration, while still having the option to customize settings as needed.

Whether you're building a desktop application, a development tool, or a user interface for a data project, WebView provides an accessible and powerful solution for creating web-based UIs in Python. It bridges the gap between web technologies and Python applications, offering the best of both worlds: the rich capabilities of web interfaces and the simplicity and power of Python programming.

### Note: 
- WebView currently supports only injection of html elements, mostly to display contents as part of you application. It does not support updates to your program logic via UI interaction of the user.
- WebView uses websockets for html updates and audio related actions.
- Currently WebView only supports a single client browser to be connected to it.

Features

- Create and manage web-based user interfaces
- Asynchronous and synchronous API for updating UI content
- Audio playback functionality
- Audio recording with custom processing callback
- Easy configuration and customization
- Support for using both a custom chromium browser or the default system browser
- Built on FastAPI for high performance

Installation

To install the WebView library, use pip:

```bash
pip install git+https://github.com/AswanthManoj/webview.git
```

To install a specific version:

```bash
pip install git+https://github.com/AswanthManoj/webview.git@<version-branch>
```
**Note: currently the versioning is done through branches**



## Project Structure
The WebView library consists of several key components:

1. `__init__.py`: The main entry point of the library, providing the `WebView` class and initializing the global `webview` object.
2. `app.py`: Handles the FastAPI application setup, routing, and WebSocket connections.
3. `config.py`: Manages the configuration settings for the WebView application.
4. `page_view.py`: Implements the core functionality for HTML updates, audio playback, and audio recording. These classes receives the websocket object through `Class.connect(websocket)` then all the socket data controls are done through their corresponding class methods.
5. `utils.py`: Provides utility functions for audio encoding and event loop management.



## How It Works

The WebView library operates by creating a FastAPI server in a separate thread and providing both asynchronous and synchronous interfaces for interaction via websockets. Here's a high-level overview of its operation:

1. When you start the WebView, it initializes a FastAPI server in a background thread.
2. The server sets up WebSocket connections for HTML updates, audio playback, and audio recording.
3. A web page is served to the client (browser) with JavaScript code to handle these WebSocket connections for each interaction.
4. The library provides methods to update the UI, play audio, and control audio recording, which communicate with the client through these WebSocket connections.
5. The UI updates are done through websockets and the received html content through websocket is put inside the main `<div>` container.
6. All operations can be performed synchronously or asynchronously, allowing for flexible integration with various application architectures.



## Usage

Here's a basic example of how to use the WebView library:

```python
import time
from webview import webview
from webview.utils import read_and_encode_mp3

# Configure the WebView with `custom_browser` False means it shows the default browser other wise a chromium based browser from playwright
webview.configure(title="My WebView App", host="localhost", port=8080, debug=True, custom_browser=False)

# Start the WebView
webview.start_webview()

# Update the view with some HTML content
webview.update_view("<h1>Hello, World!</h1>")

# Play an audio file
audio_data = read_and_encode_mp3("path/to/your/audio.mp3")
webview.play_audio(audio_data)

# Start audio recording
def process_audio(audio_bytes):
    print("Received audio data:", len(audio_bytes), "bytes")

# Stop audio recording after 5 seconds
webview.start_recording(process_audio)
time.sleep(5)
webview.stop_recording()
```


## API Reference

#### WebView Class
- `configure(title: str, host: str, port: int, debug: bool, log_level: str, custom_browser: bool)`: Configure the WebView settings.

- `start_webview() -> bool`: Start the WebView application.

- `update_view(html: str)` : Update the HTML content of the WebView.

- `async_update_view(html: str)`: Asynchronously update the HTML content of the WebView.

- `play_audio(audio_data: str, delay: float = None) -> str`: Play audio data in the WebView.

- `async_play_audio(audio_data: str, delay: float = None) -> str`: Asynchronously play audio data in the WebView.

- `start_recording(audio_processor: Callable[[bytes], None]) -> bool`: Start recording audio in the WebView.

- `async_start_recording(audio_processor: Callable[[bytes], None]) -> bool`: Asynchronously start recording audio in the WebView.

- `stop_recording() -> bool`: Stop recording audio in the WebView.

- `async_stop_recording() -> bool`: Asynchronously stop recording audio in the WebView.


#### Utility Functions:
`read_and_encode_audio(file_path: str, input_format: str) -> str`: Read an audio file and encode it as a base64 WAV string.

`read_and_encode_mp3(file_path: str) -> str`: Read an MP3 file and encode it as a base64 WAV string.

`read_and_encode_wav(file_path: str) -> str`: Read a WAV file and encode it as a base64 WAV string.

`read_and_encode_ogg(file_path: str) -> str`: Read an OGG file and encode it as a base64 WAV string.

`read_and_encode_flac(file_path: str) -> str`: Read a FLAC file and encode it as a base64 WAV string.

`read_and_encode_aac(file_path: str) -> str`: Read an AAC file and encode it as a base64 WAV string.

`read_and_encode_m4a(file_path: str) -> str`: Read an M4A file and encode it as a base64 WAV string.


## Examples

### Updating the UI

```python
from webview import webview

webview.configure(title="Dynamic Content Example", host="localhost", port=8080)
webview.start_webview()

# Update the view with dynamic content
for i in range(5):
    webview.update_view(f"<h1>Count: {i}</h1>")
    time.sleep(1)
```

### Playing Audio

```python
from webview import webview
from webview.utils import read_and_encode_mp3

webview.configure(title="Audio Player Example", host="localhost", port=8080)
webview.start_webview()

# Play an audio file
audio_data = read_and_encode_mp3("path/to/your/audio.mp3")
webview.play_audio(audio_data)
```

### Recording Audio

```python
from webview import webview

webview.configure(title="Audio Recorder Example", host="localhost", port=8080)
webview.start_webview()

def process_audio(audio_bytes):
    print("Received audio data:", len(audio_bytes), "bytes")

# Start recording
webview.start_recording(process_audio)

# Record for 10 seconds
time.sleep(10)

# Stop recording
webview.stop_recording()
```


## Future Directions
As we continue to develop and enhance the WebView library, we have several exciting features and improvements planned:

1. **React-like Rendering with SSR:** We aim to implement a more efficient rendering system similar to React, utilizing server-side rendering (SSR) through WebSockets. This will allow for partial updates to specific components rather than re-rendering the entire content, resulting in improved performance and a smoother user experience.

2. **Multi-Client Support:** Future versions will include support for multiple client connections, enabling the creation of collaborative applications or multi-user interfaces.

3. **Prebuilt UI Component API:** We plan to introduce a set of prebuilt UI elements such as buttons, containers, and columns, with basic style customization options. This will accelerate development and ensure consistency across applications.

4. **User Interaction-Driven Program Logic:** We're working on implementing mechanisms for controlling program logic through user interactions, creating more dynamic and responsive applications.

5. **Streamlit-Inspired UI Building:** Drawing inspiration from Streamlit, we aim to provide an API for building UIs that doesn't require re-running the entire application for every UI change. This will offer a more efficient and intuitive way to create interactive interfaces.

6. **Python-Based Component System:** We're developing a component-based setup similar to React's JSX, but implemented entirely in Python using primitives like Jinja templating. This will allow for powerful, dynamic UI creation without leaving the Python ecosystem.

7. **Dynamic, Interactive UI Construction:** Instead of traditional static page templates used in SSR, we're moving towards a system can dynamically build interactive UIs with components and updates them through websockets.

8. **Rapid Prototyping:** Our goal is to enable quick prototype development with both front-end and back-end controls using a single, backend-only program logic. This will streamline the development process for many types of applications without needing to know `js`, `html`, `react` or any front-end frameworks.

9. **Custom Component Creation:** We plan to support the creation of custom components in a style similar to React but in a python style, allowing developers to extend the library's capabilities to meet their specific needs.

10. **WebSocket-Driven Updates:** All updates will be handled through WebSockets in a React-like style (but SSR), ensuring efficient, real-time communication between the front-end and back-end.

These future developments will make WebView an even more powerful and flexible tool for creating web-based user interfaces in Python, bridging the gap between traditional web development and Python application development.



## Contributing
Contributions to the WebView library are welcome! Please feel free to submit pull requests, create issues, or suggest new features.



## License
MIT License