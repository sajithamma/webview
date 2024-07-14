import time, io
import asyncio, base64
from webview import Webview
from pydub import AudioSegment

async def process_audio(audio_bytes):
    # This function will be called whenever new audio data is received
    print(f"Received {len(audio_bytes)} bytes of audio data")
    # Here you can process the audio data as needed
    # For example, you could save it to a file, analyze it, etc.

async def updater():
    i=0
    while True:
        await Webview.update_view(f"<h2>This is update number {i}</h2>")
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
    Webview.start_webview()
    Webview.configure(log_level="critical")

    # Start listening for audio with the callback
    await Webview.start_listening(process_audio)
    print("Started listening for audio...")

    # Update view a few times
    task = asyncio.create_task(updater())
    time.sleep(60)

    # Stop listening for audio
    await Webview.stop_listening()
    print("Stopped listening for audio...")

    # Play some audio (replace with actual audio data)
    sample_audio_data = mp3_to_base64_wav("sample4.mp3")
    await Webview.play_audio(sample_audio_data)
    print("Playing audio...")

    await asyncio.gather(task)


if __name__ == "__main__":
    asyncio.run(main())