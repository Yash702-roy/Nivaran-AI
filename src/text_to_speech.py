
import asyncio
import os
import tempfile
import edge_tts


async def generate_audio(text, output_path, voice):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )
    await communicate.save(output_path)


def generate_speech_file(text, language="hi"):
    if not text or not text.strip():
        raise ValueError("Text is empty.")

    if language == "hi":
        voice = "hi-IN-SwaraNeural"
    else:
        voice = "en-IN-NeerjaNeural"

    fd, audio_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        asyncio.run(
            generate_audio(text, audio_path, voice)
        )

        if os.path.getsize(audio_path) == 0:
            raise RuntimeError("Generated audio file is empty.")

        return audio_path

    except Exception:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise
