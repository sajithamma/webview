import time
from webview import Webview

Webview.start_webview()
Webview.configure(log_level="critical")

i=0
while True:
    i+=1
    Webview.update_view(f"<h2>This is update number {i}</h2>")
    time.sleep(1)