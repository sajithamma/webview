import asyncio, json, uuid
from .config import Config
from .utils import ensure_event_loop
from fastapi import WebSocket, WebSocketDisconnect


class HTMLUpdater:
    def __init__(self):
        self.config = None
        self.change_detected = True
        self.client: WebSocket = None
        self.html_content = ""
        
    def bind_config(self, config: Config):
        self.config=config 

    def update_view(self, new_html: str):
        loop = ensure_event_loop()
        loop.run_until_complete(self.async_update_view(new_html))
        
    async def async_update_view(self, new_html: str): 
        if self.client:
            await self.client.send_text(new_html)
            if self.config and self.config.debug:
                print("Webview: View updated")
        elif self.config and self.config.debug:
            print("Webview: Client is not available for UI updates")
           
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to html updater")
        try:
            while True:
                await websocket.receive_text()
        finally:
            self.client = None
  
     
            
class AudioPlayer:
    
    def __init__(self):
        self.config = None
        self.client: WebSocket = None
        self.audio_queue = asyncio.Queue()
        self.pending_audios = {}
        
    def bind_config(self, config: Config):
        self.config=config    
        
    def play_audio(self, audio_data: str, delay: float) -> str:
        loop = ensure_event_loop()
        return loop.run_until_complete(self.async_play_audio(audio_data, delay))   
         
    async def async_play_audio(self, audio_data: str, delay: float) -> str:
        audio_id = str(uuid.uuid4())
        if self.client:
            await self.audio_queue.put((audio_id, audio_data, delay))
            self.pending_audios[audio_id] = True
        while True:
            if audio_id not in self.pending_audios:
                return audio_id
            
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to audio player")
        try:
            while True:
                audio_id, audio_data, delay = await self.audio_queue.get()
                await websocket.send_text(json.dumps({
                    "type": "audio",
                    "id": audio_id,
                    "data": audio_data,
                    "delay": delay
                }))
                message = await websocket.receive_text()
                data = json.loads(message)
                
                if data['type'] == 'playback_complete':
                    if self.config and self.config.debug:
                        print(f"Audio playback completed for ID: {data['id']}")
                    del self.pending_audios[data['id']]
        finally:
            self.client = None


html_updater = HTMLUpdater()
audio_player = AudioPlayer()
