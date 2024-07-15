import time, io
import asyncio, base64
from webview import webview
from pydub import AudioSegment

async def updater():
    i=0
    while True:
        await webview.async_update_view(f"<h2>This is update number {i}</h2>")
        await asyncio.sleep(1)
        i+=1

def mp3_to_base64_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    wav_data = buffer.getvalue()
    base64_wav = base64.b64encode(wav_data).decode('utf-8')
    return f"data:audio/wav;base64,{base64_wav}"

async def main():
    webview.start_webview()
    webview.configure(log_level="critical")
    
    task = asyncio.create_task(updater())
    
    audio_1 = mp3_to_base64_wav("sample_audio1.mp3")
    audio_id = await webview.async_play_audio(audio_1)
    print("Audio with id", audio_id, "is playing")
    
    audio_2 = mp3_to_base64_wav("sample_audio2.mp3")
    audio_id = await webview.async_play_audio(audio_2, delay=3) # Add an 5 second delay in audio playback 
    print("Audio with id", audio_id, "is playing")
    
    await asyncio.sleep(120)
  
  
if __name__=='__main__':  
    asyncio.run(main())