import asyncio, json, uuid
from .config import Config
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
        self.__run_sync__(self.async_update_view(new_html))
        
    async def async_update_view(self, new_html: str): 
        self.html_content = new_html
        self.change_detected = True
        if self.client:
            await self.client.send_text(self.html_content)
            if self.config and self.config.debug:
                print("Webview: View updated")
        elif self.config and self.config.debug:
            print("Webview: Client is not available for UI updates")
        
    def __run_sync__(self, coro):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(coro)
        else:
            loop.run_until_complete(coro)
           
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.client = websocket
        if self.config and self.config.debug:
            print("Webview: Client has been connected to html updater")
        try:
            while True:
                if self.change_detected:
                    await websocket.send_text(self.html_content)
                    self.change_detected = False
                await websocket.receive_text()
        finally:
            self.client = None
  
     
            
class AudioPlayer:
    
    def __init__(self):
        self.config = None
        self.playing_count = 0
        self.client: WebSocket = None
        self.audio_queue = asyncio.Queue()
        self.finished_event = asyncio.Event()
        
    def bind_config(self, config: Config):
        self.config=config    
        
    def play_audio(self, audio_data: str, delay: float) -> str:
        return self.__run_sync__(self.async_play_audio(audio_data, delay))    
         
    async def async_play_audio(self, audio_data: str, delay: float) -> str:
        audio_id = str(uuid.uuid4())
        await self.audio_queue.put((audio_id, audio_data, delay))
        self.playing_count += 1
        self.finished_event.clear()
        return audio_id
    
    def wait_until_finish_play(self):
        self.__run_sync__(self.async_wait_until_finish_play())        
            
    async def async_wait_until_finish_play(self):
        await self.finished_event.wait()
    
    def __run_sync__(self, coro):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.create_task(coro)
        else:
            return loop.run_until_complete(coro)
    
    async def mark_finished(self, audio_id: str):
        self.playing_count -= 1
        if self.playing_count == 0:
            self.finished_event.set()
            
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
                
                if data['type'] == 'playback_complete' and self.config and self.config.debug:
                    print(f"Audio playback completed for ID: {data['id']}")
                    await self.mark_finished(data['id'])
        finally:
            self.client = None
    
    def clear_audio_queue(self):
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        self.playing_count = 0
        self.finished_event.set()



html_updater = HTMLUpdater()
audio_player = AudioPlayer()


