import os
import tempfile
from html import escape
import streamlit as st

from src.rag_pipeline import answer_question
from src.retriever import load_vector_store
from src.speech_to_text import transcribe_audio
from src.text_to_speech import generate_speech_file


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Nivaran AI | Accessible Scheme Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# 2. VISUAL DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --navy: #10264c;
        --blue: #1457d9;
        --blue-dark: #0b3fae;
        --green: #07854f;
        --ink: #14233b;
        --muted: #40516b;
        --line: #d7e4f5;
        --surface: #ffffff;
        --pale-blue: #edf5ff;
        --pale-green: #e8f8ef;
    }

    .stApp {
        background:
          radial-gradient(circle at 85% 5%, rgba(190, 219, 255, .35), transparent 27rem),
          #f5f8fd;
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(245, 248, 253, .92); }
    [data-testid="stMainBlockContainer"] {
        max-width: 1320px;
        padding-top: 1.3rem;
        padding-bottom: 2.5rem;
    }
    html, body, [class*="stApp"] { font-size: 17px; }
    h1, h2, h3, p, label, li, span, div { }
    h1, h2, h3 { color: var(--navy) !important; letter-spacing: -0.025em; }
    h1 { font-size: clamp(2.25rem, 4vw, 3.45rem) !important; line-height: 1.08 !important; font-weight: 850 !important; }
    h2 { font-size: 1.75rem !important; font-weight: 800 !important; }
    h3 { font-size: 1.25rem !important; font-weight: 750 !important; }
    p, label, li { color: var(--ink); line-height: 1.65 !important; }
    [data-testid="stMarkdownContainer"] p { line-height: 1.65; }

    .brand-row {
        display: flex; align-items: center; gap: 14px;
        padding: 8px 0 22px 0;
    }
    .brand-mark {
        width: 62px; height: 62px; border-radius: 19px;
        display: flex; align-items: center; justify-content: center;
        font-size: 34px; background: linear-gradient(145deg, #ffedbd, #fff8e9);
        border: 1px solid #f5d99a; flex-shrink: 0;
    }
    .brand-name { font-size: 2rem; line-height: 1.05; font-weight: 850; color: var(--navy); }
    .brand-sub { font-size: .98rem; color: var(--muted); margin-top: 5px; }
    .top-pill {
        display: inline-block; padding: 9px 15px; border-radius: 999px;
        color: #153d7d; background: #e6f0ff; border: 1px solid #cfe0fb;
        font-size: .9rem; font-weight: 700;
    }
    .hero {
        padding: 30px 30px 27px; border-radius: 28px;
        background: linear-gradient(115deg, #ffffff 0%, #edf5ff 62%, #e3efff 100%);
        border: 1px solid #d7e6fb; box-shadow: 0 12px 34px rgba(25, 68, 128, .07);
        margin: 8px 0 22px;
    }
    .hero-kicker {
        color: #0b6b45; font-size: .88rem; font-weight: 800;
        letter-spacing: .08em; text-transform: uppercase; margin-bottom: 12px;
    }
    .hero-title { font-size: clamp(2rem, 3.8vw, 3.2rem); line-height: 1.12; font-weight: 850; color: var(--navy); letter-spacing: -.04em; }
    .hero-title .accent { color: var(--blue); }
    .hero-copy { font-size: 1.13rem; color: #354965; max-width: 760px; margin-top: 14px; }
    .hero-badges { display: flex; flex-wrap: wrap; gap: 9px; margin-top: 20px; }
    .hero-badge { background: #fff; border: 1px solid #cde0f5; border-radius: 999px; padding: 8px 12px; font-weight: 700; color: #17385f; font-size: .9rem; }
    .hero-art {
        min-height: 220px; height: 100%; border-radius: 23px;
        background: linear-gradient(155deg, #dbeaff, #f8fbff 60%, #e3f8ed);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; border: 1px solid #d2e2f7; padding: 20px;
    }
    .hero-emoji { font-size: 4.8rem; line-height: 1.3; }
    .hero-art-title { font-size: 1.18rem; font-weight: 800; color: var(--navy); }
    .hero-art-copy { font-size: .95rem; color: #40516b; margin-top: 5px; }
    .section-label { font-size: 1.4rem; font-weight: 800; color: var(--navy); margin: 10px 0 5px; }
    .section-help { color: var(--muted); margin-bottom: 14px; }
    .feature-card {
        border: 1px solid var(--line); background: white; border-radius: 19px;
        padding: 18px 17px; min-height: 116px; box-shadow: 0 5px 17px rgba(22, 58, 105, .045);
    }
    .feature-icon { font-size: 1.8rem; margin-bottom: 7px; }
    .feature-title { color: var(--navy); font-weight: 800; font-size: 1.02rem; }
    .feature-copy { color: var(--muted); font-size: .88rem; margin-top: 4px; line-height: 1.45; }
    .panel {
        background: white; border: 1px solid var(--line); border-radius: 22px;
        padding: 22px; box-shadow: 0 7px 24px rgba(22, 58, 105, .05);
        height: 100%;
    }
    .panel-heading { color: var(--navy); font-size: 1.35rem; font-weight: 850; margin-bottom: 5px; }
    .panel-copy { color: var(--muted); font-size: .95rem; margin-bottom: 15px; }
    .answer-box {
        background: linear-gradient(120deg, #eef7ff, #f0fbf5);
        border: 1px solid #cce7e8; border-radius: 16px; padding: 19px;
        color: #14233b; font-size: 1.07rem; line-height: 1.75;
    }
    .source-item {
        padding: 12px 14px; border-radius: 13px; border: 1px solid #dce8f6;
        background: #f6f9fe; margin: 8px 0; color: #172d4e;
    }
    .step {
        display: flex; gap: 12px; align-items: flex-start; margin: 12px 0;
        color: var(--ink); line-height: 1.5;
    }
    .step-num {
        min-width: 32px; height: 32px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        background: #e5efff; color: #1249b7; font-weight: 850;
    }
    .footer-box {
        background: #10264c; color: white; border-radius: 18px; padding: 20px 22px;
        margin-top: 24px;
    }
    .footer-title { color: white; font-weight: 800; font-size: 1.12rem; }
    .footer-copy { color: #e1eafa; font-size: .9rem; margin-top: 5px; }
    .stButton > button, .stFormSubmitButton > button {
        min-height: 54px; border-radius: 13px; font-size: 1.02rem;
        font-weight: 800; border: 2px solid #174caa; transition: none;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1768ed, #1048bd); color: white;
        border: 2px solid #1048bd;
    }
    .stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible,
    input:focus-visible, textarea:focus-visible, select:focus-visible,
    button:focus-visible, [tabindex]:focus-visible {
        outline: 4px solid #ffbf00 !important; outline-offset: 4px !important;
    }
    input, textarea { font-size: 1rem !important; min-height: 48px; }
    [data-testid="stAudio"] { width: 100%; }
    [data-testid="stAlert"] { border-radius: 13px; font-size: 1rem; }
    footer { visibility: hidden; }
    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"] { padding-left: 1rem; padding-right: 1rem; }
        .hero { padding: 22px 18px; }
        .brand-name { font-size: 1.55rem; }
        .hero-emoji { font-size: 3.6rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 3. BRAND HEADER + HERO
# --------------------------------------------------
st.markdown(
    """
    <div class="brand-row">
      <div class="brand-mark" aria-hidden="true">🤝</div>
      <div>
        <div class="brand-name">Nivaran AI</div>
        <div class="brand-sub">Government Scheme Assistant</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([1.7, 1], gap="large")
with hero_left:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Accessible information • Inclusive India</div>
          <div class="hero-title">Government schemes,<br><span class="accent">made easier for everyone.</span></div>
          <div class="hero-copy">
            Ask about government schemes, benefits and services in simple language.
            Type your question or speak in Hindi or English, then listen to the answer.
          </div>
          <div class="hero-badges">
            <span class="hero-badge">♿ Accessibility-minded</span>
            <span class="hero-badge">🎙️ Voice enabled</span>
            <span class="hero-badge">🇮🇳 Hindi & English</span>
            <span class="hero-badge">📄 Document-based answers</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown(
        """
        <div class="hero-art" role="img" aria-label="Inclusive support for different abilities">
          <div class="hero-emoji" aria-hidden="true">🧑‍🦯 🦻 ♿</div>
          <div class="hero-art-title">Information without barriers</div>
          <div class="hero-art-copy">Designed with clear language, voice access and readable controls.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# 4. LOAD VECTOR DATABASE AND MODELS
# --------------------------------------------------
@st.cache_resource
def load_resources():
    return load_vector_store()


try:
    with st.spinner("Loading government scheme documents. Please wait."):
        index, chunks, model = load_resources()
except Exception:
    st.error(
        "The document database could not be loaded. Please check the terminal "
        "or contact the project administrator."
    )
    st.stop()

# --------------------------------------------------
# 5. SESSION STATE + HELPERS
# --------------------------------------------------
defaults = {
    "last_answer": None,
    "last_sources": [],
    "last_question": "",
    "last_transcript": "",
    "audio_path": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def remove_saved_audio():
    old_path = st.session_state.audio_path
    if old_path and os.path.exists(old_path):
        try:
            os.remove(old_path)
        except OSError:
            pass
    st.session_state.audio_path = None


def get_answer(query):
    query = (query or "").strip()
    if not query:
        st.warning("Please enter or record a question.")
        return

    with st.spinner("Searching the documents and preparing your answer..."):
        result = answer_question(
            query=query,
            index=index,
            chunks=chunks,
            model=model,
        )

    remove_saved_audio()
    st.session_state.last_question = query
    st.session_state.last_answer = result.get("answer", "No answer was generated.")
    st.session_state.last_sources = result.get("sources", [])


# --------------------------------------------------
# 6. FEATURE STRIP
# --------------------------------------------------
st.markdown('<div class="section-label">A simpler way to find support</div>', unsafe_allow_html=True)
st.markdown('<div class="section-help">Start with your question. Nivaran AI searches the available scheme documents for relevant information.</div>', unsafe_allow_html=True)

feature_cols = st.columns(4, gap="medium")
features = [
    ("🎙️", "Ask by voice", "Speak instead of typing"),
    ("🔎", "Find information", "Search scheme documents"),
    ("🔊", "Listen to answers", "Hear the response aloud"),
    ("📚", "Check sources", "See supporting documents"),
]
for col, (icon, title, copy) in zip(feature_cols, features):
    with col:
        st.markdown(
            f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
            f'<div class="feature-title">{title}</div><div class="feature-copy">{copy}</div></div>',
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# 7. ASK PANEL
# --------------------------------------------------
st.markdown("")
ask_col, guide_col = st.columns([1.65, 1], gap="large")

with ask_col:
    st.markdown('<div class="panel-heading">💬 Ask Nivaran AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-copy">Choose your preferred answer language, then type or record your question.</div>', unsafe_allow_html=True)

    answer_language = st.selectbox(
        "Language for spoken answers",
        options=["Hindi", "English"],
        index=0,
        help="This selects the voice used to read the answer. It does not translate the answer text.",
        key="answer_language",
    )
    speech_language = {"Hindi": "hi", "English": "en"}[answer_language]

    tab_text, tab_voice = st.tabs(["⌨️ Ask by text", "🎙️ Ask by voice"])

    with tab_text:
        with st.form("text_question_form", clear_on_submit=False):
            question = st.text_area(
                "Your question",
                placeholder="Example: What is the purpose of the UDID project?",
                height=105,
                key="text_question",
                help="Ask one clear question about a government scheme.",
            )
            text_submit = st.form_submit_button(
                "🔎  Get an answer",
                type="primary",
                use_container_width=True,
            )
        if text_submit:
            try:
                get_answer(question)
            except Exception:
                st.error("Sorry, the answer could not be generated. Please try again.")

    with tab_voice:
        st.write("Record your question in Hindi or English.")
        audio = st.audio_input("Record your question", key="voice_question_audio")
        if audio is not None and st.button(
            "🎧  Transcribe and get answer",
            key="voice_submit",
            type="primary",
            use_container_width=True,
        ):
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(audio.getvalue())
                    temp_path = temp_file.name

                with st.spinner("Recognizing your spoken question..."):
                    transcript = transcribe_audio(temp_path)

                if not transcript or not transcript.strip():
                    st.warning("No speech was recognized. Please record again in a quiet environment.")
                else:
                    st.session_state.last_transcript = transcript
                    get_answer(transcript)
            except Exception:
                st.error("Voice processing failed. Please try recording again.")
            finally:
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

with guide_col:
    st.markdown('<div class="panel-heading">🧭 How to use</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-copy">Three simple steps to get started.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="step"><div class="step-num">1</div><div><b>Ask a question</b><br>Type it or record your voice.</div></div>
        <div class="step"><div class="step-num">2</div><div><b>Choose a voice language</b><br>Select Hindi or English for spoken output.</div></div>
        <div class="step"><div class="step-num">3</div><div><b>Read or listen</b><br>Review the answer and its source documents.</div></div>
        <hr style="border:0;border-top:1px solid #d7e4f5;margin:18px 0;">
        <div style="font-weight:800;color:#10264c;margin-bottom:6px;">Example questions</div>
        <div style="color:#40516b;font-size:.94rem;line-height:1.8;">
          • What is the UDID project?<br>
          • Which benefits are mentioned in this document?<br>
          • What documents are required?
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# 8. RECOGNIZED QUESTION
# --------------------------------------------------
if st.session_state.last_transcript:
    st.info(f"Recognized voice question: {st.session_state.last_transcript}")

# --------------------------------------------------
# 9. ANSWER + SPEECH + SOURCES
# --------------------------------------------------
if st.session_state.last_answer:
    st.markdown("")
    st.markdown('<div class="panel-heading">📘 Answer from Nivaran AI</div>', unsafe_allow_html=True)
    st.markdown("**Your question**")
    st.write(st.session_state.last_question)
    st.markdown("**Response**")
    st.markdown(
        f'<div class="answer-box">{escape(str(st.session_state.last_answer))}</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        f"🔊  Listen to answer in {answer_language}",
        key="listen_to_answer",
        type="primary",
        use_container_width=True,
    ):
        new_audio_path = None
        try:
            with st.spinner(f"Preparing spoken answer in {answer_language}..."):
                new_audio_path = generate_speech_file(
                    st.session_state.last_answer,
                    language=speech_language,
                )

            if not new_audio_path or not os.path.exists(new_audio_path):
                raise RuntimeError("The audio file was not generated.")

            old_path = st.session_state.audio_path
            st.session_state.audio_path = new_audio_path
            new_audio_path = None

            if old_path and os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass
            st.success("Spoken answer is ready. Use the audio player below.")
        except Exception:
            st.error("Speech generation failed. Check your internet connection and text-to-speech configuration.")
        finally:
            if new_audio_path and os.path.exists(new_audio_path):
                try:
                    os.remove(new_audio_path)
                except OSError:
                    pass

    saved_audio_path = st.session_state.audio_path
    if saved_audio_path and os.path.exists(saved_audio_path):
        try:
            with open(saved_audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mpeg")
        except OSError:
            st.error("The audio could not be played. Generate it again.")

    st.markdown('<div class="panel-heading">📄 Source documents</div>', unsafe_allow_html=True)
    if st.session_state.last_sources:
        for number, source in enumerate(st.session_state.last_sources, start=1):
            source_name = source.get("source", "Government document")
            page_number = source.get("page", "Not specified")
            st.markdown(
                f'<div class="source-item"><b>Source {number}:</b> {escape(str(source_name))} '
                f'<span style="color:#40516b;">• Page {escape(str(page_number))}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No source documents were retrieved for this answer.")

# --------------------------------------------------
# 10. FOOTER / TRUST
# --------------------------------------------------
st.markdown(
    """
    <div class="footer-box">
      <div class="footer-title">🤝 Nivaran AI · Information without barriers</div>
      <div class="footer-copy">
        Built to make government-scheme information easier to explore.
        Answers are based on the documents currently available in this app.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Please verify important eligibility rules, required documents and deadlines "
    "with the relevant government authority. Language selection changes the spoken voice; "
    "it does not automatically translate the answer."
)
