
import os
import tempfile

import streamlit as st
from src.speech_to_text import transcribe_audio


st.title("Nivaran AI - Local Voice Input")

audio = st.audio_input("Record your question")

if audio is not None:
    st.audio(audio)

    if st.button("Convert Speech to Text"):
        temp_path = None

        try:
            # Save recording temporarily as a WAV file
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp_file:
                temp_file.write(audio.getvalue())
                temp_path = temp_file.name

            with st.spinner("Transcribing locally..."):
                transcript = transcribe_audio(temp_path)

            if transcript:
                st.success("Speech recognized!")
                st.write("Your question:", transcript)
            else:
                st.warning("No speech was detected. Please try again.")

        except Exception as error:
            st.error(f"Transcription failed: {error}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
