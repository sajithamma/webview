import asyncio
from webview import webview
from webview.utils import read_and_encode_mp3

async def updater():
    i=0
    while True:
        await webview.async_update_view(f"<h2>This is update number {i}</h2>")
        await asyncio.sleep(1)
        i+=1

async def main():
    webview.start_webview()
    webview.configure(log_level="critical")
    
    task = asyncio.create_task(updater())
    
    # Plays a sample audio in the browser
    audio_1 = read_and_encode_mp3("sample/sample_audio1.mp3")
    audio_id = await webview.async_play_audio(audio_1)
    print("Audio with id", audio_id, "is playing")
    
    # Plays a second sample audio after a 5 second delay
    audio_2 = read_and_encode_mp3("sample/sample_audio2.mp3")
    audio_id = await webview.async_play_audio(audio_2, delay=3) 
    print("Audio with id", audio_id, "is playing")
    
    await asyncio.sleep(120)
  
  
if __name__=='__main__':  
    asyncio.run(main())