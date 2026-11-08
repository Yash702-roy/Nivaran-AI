
from faster_whisper import WhisperModel


# Load the lightweight model once
_model = None


def load_speech_model():
    global _model

    if _model is None:
        _model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )

    return _model


def transcribe_audio(audio_path):
    """Transcribe an audio file locally without an API key."""

    model = load_speech_model()

    segments, info = model.transcribe(
        audio_path,
        beam_size=1
    )

    transcript = " ".join(
        segment.text.strip() for segment in segments
    ).strip()

    return transcript
