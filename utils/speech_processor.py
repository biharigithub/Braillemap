import os
import asyncio
import edge_tts  # Microsoft Edge TTS library

# Folder to save audio files
AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

async def generate_tts(text, lang_code, filename):
    filepath = os.path.join(AUDIO_FOLDER, filename)
    communicate = edge_tts.Communicate(text, lang_code)
    await communicate.save(filepath)
    return filepath

def text_to_speech(text, language):
    """
    Convert text to speech and return the relative URL of the audio file.
    Supports English (en-US) and Hindi (hi-IN).
    """
    filename = "tts_output.mp3"
    lang_code = "hi-IN" if language.lower() == "hindi" else "en-US"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_tts(text, lang_code, filename))
    return f"/static/audio/{filename}"
