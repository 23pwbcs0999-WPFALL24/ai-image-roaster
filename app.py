

import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io

# ── 1. Load the API key from .env ──────────────────────────────
load_dotenv()                                   # reads .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    # grab the key

# ── 2. Configure Gemini ────────────────────────────────────────
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# ── 3. Page config (must be the very first Streamlit call) ─────
st.set_page_config(
    page_title="AI Vision Roast System",
    page_icon="🔥",
    layout="centered",
)


# ── 4. Custom CSS – dark & spicy aesthetic ─────────────────────
st.markdown("""
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@400;600;700&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* ── App Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Main container card ── */
.main-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,200,0,0.2);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    margin-top: 1rem;
}

/* ── Title ── */
.roast-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 3.8rem;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #ff6b35, #ffd700, #ff6b35);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    text-align: center;
    margin-bottom: 0;
}
@keyframes shimmer {
    0%   { background-position: 0%   }
    100% { background-position: 200% }
}

/* ── Subtitle ── */
.roast-subtitle {
    text-align: center;
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    margin-top: 0.3rem;
    margin-bottom: 1.5rem;
    letter-spacing: 0.5px;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ffd700;
    margin-bottom: 0.4rem;
}

/* ── Upload box override ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(255,200,0,0.35) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(255,107,53,0.7) !important;
}

/* ── Image preview frame ── */
.preview-frame {
    border: 2px solid rgba(255,200,0,0.3);
    border-radius: 14px;
    overflow: hidden;
    margin-top: 0.8rem;
    box-shadow: 0 4px 24px rgba(255,107,53,0.15);
}

/* ── Roast output box ── */
.roast-box {
    background: linear-gradient(135deg, rgba(255,107,53,0.12), rgba(255,215,0,0.08));
    border: 1px solid rgba(255,200,0,0.4);
    border-left: 4px solid #ff6b35;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
    color: #fff;
    font-size: 1.1rem;
    line-height: 1.75;
    animation: fadeIn 0.6s ease;
}
@keyframes fadeIn {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Flame emoji bounce ── */
.flame {
    display: inline-block;
    animation: bounce 0.7s infinite alternate;
}
@keyframes bounce {
    from { transform: translateY(0);   }
    to   { transform: translateY(-5px); }
}

/* ── Generate button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #ff6b35, #e63946) !important;
    color: white !important;
    font-family: 'Bebas Neue', cursive !important;
    font-size: 1.35rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    margin-top: 1rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(255,107,53,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,107,53,0.6) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Error / info boxes ── */
.stAlert {
    border-radius: 10px !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.25);
    font-size: 0.75rem;
    margin-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── 5. Helper: generate roast using Gemini ─────────────────────
def generate_roast(image: Image.Image) -> str:
    """
    Sends the PIL image to Gemini and returns a funny roast string.
    Falls back to a placeholder if the API key is missing.
    """

    # ── Fallback mode: no API key configured ──
    if not GEMINI_API_KEY:
        return (
            "🔥 Looks like someone forgot to add their GEMINI_API_KEY to the .env file. "
            "Even this roast machine can't work on empty fuel! Add your key and try again, "
            "champ. 😄"
        )

    # ── Build a stronger prompt for funnier, sharper, but safe roasts ──────
    prompt = """
You are an elite roast comedian writing for a live crowd.

Analyze this image carefully and produce ONE high-quality roast that feels original.

Requirements:
- Keep it to exactly 3 lines.
- Each line should be a punchline, not explanation.
- Be specific to visible details in the image (pose, background, outfit, objects, vibe, timing).
- Use one clever analogy and one unexpected comparison.
- Tone: playful, witty, confident, and memorable.
- Avoid generic lines like "bro thinks" or "main character energy" unless truly relevant.


Return only the roast text.
    """

    # ── Use a verified working Gemini Flash model for this API key ──────
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        [prompt, image],
        generation_config={
            "temperature": 1.25,
            "top_p": 0.92,
            "max_output_tokens": 220,
        },
    )

    return response.text.strip()


# ══════════════════════════════════════════════════════════════
#  6. UI LAYOUT
# ══════════════════════════════════════════════════════════════

# ── Title block ───────────────────────────────────────────────
st.markdown('<div class="roast-title">🔥 AI VISION ROAST 🔥</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="roast-subtitle">'
    'Upload any image &nbsp;·&nbsp; Let the AI drag it &nbsp;·&nbsp; Laugh (or cry) &nbsp;😂'
    '</div>',
    unsafe_allow_html=True,
)

# ── Divider ───────────────────────────────────────────────────
st.divider()

# ── API key warning banner (only shows if .env key is missing) ─
if not GEMINI_API_KEY:
    st.warning(
        "⚠️ **No API Key found.**  \n"
        "Create a `.env` file with `GEMINI_API_KEY=your_key_here` to enable real roasts.  \n"
        "The app still runs in **demo / placeholder mode**.",
        icon="⚠️",
    )

# ── Upload section ────────────────────────────────────────────
st.markdown('<div class="section-label">📁 Step 1 — Upload Your Image</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Drop an image here or click to browse",
    type=["jpg", "jpeg", "png", "webp", "gif"],
    label_visibility="collapsed",   # hide default label (we have our own)
)

# ── Preview + Roast section ───────────────────────────────────
if uploaded_file is not None:

    # Read image bytes into PIL
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Convert RGBA/P mode images to RGB (Gemini needs RGB/JPEG)
    if image.mode in ("RGBA", "P", "LA"):
        image = image.convert("RGB")

    # ── Image Preview ──────────────────────────────────────────
    st.markdown('<div class="section-label" style="margin-top:1.2rem;">🖼️ Step 2 — Preview</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])   # center the image
    with col2:
        st.image(image, use_container_width=True, caption=f"📸 {uploaded_file.name}")

    # ── Image metadata ─────────────────────────────────────────
    width, height = image.size
    st.caption(f"📐 {width} × {height} px  ·  Mode: {image.mode}")

    # ── Generate button ────────────────────────────────────────
    st.markdown('<div class="section-label" style="margin-top:1rem;">🎤 Step 3 — Get Roasted</div>', unsafe_allow_html=True)

    if st.button("🔥 GENERATE ROAST", use_container_width=True):

        with st.spinner("🤔 Gemini is judging your image..."):
            try:
                roast_text = generate_roast(image)

                # ── Display result ─────────────────────────────
                st.markdown("---")
                st.markdown('<div class="section-label">🎯 The Verdict</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="roast-box">💬 {roast_text}</div>',
                    unsafe_allow_html=True,
                )

                # Fun reaction row
                st.markdown("")
                rcol1, rcol2, rcol3 = st.columns(3)
                with rcol1:
                    st.markdown("**😂 Too Real?**")
                with rcol2:
                    st.markdown("**🔥 Upload Another!**")
                with rcol3:
                    st.markdown("**🤖 Powered by Gemini**")

            except Exception as e:
                # Friendly error messages for common issues
                error_msg = str(e)
                if "API_KEY" in error_msg.upper() or "401" in error_msg or "403" in error_msg:
                    st.error(
                        "🔑 **Invalid or missing API key.**  \n"
                        "Check that `GEMINI_API_KEY` in your `.env` file is correct.",
                        icon="🔑",
                    )
                elif "SAFETY" in error_msg.upper() or "blocked" in error_msg.lower():
                    st.warning(
                        "🛡️ **Gemini's safety filter blocked this image.**  \n"
                        "Try a different image — some content can't be roasted!",
                        icon="🛡️",
                    )
                elif "quota" in error_msg.lower() or "429" in error_msg:
                    st.error(
                        "⏳ **API quota exceeded.**  \n"
                        "You've hit your Gemini free-tier limit. Wait a minute and try again.",
                        icon="⏳",
                    )
                else:
                    st.error(f"❌ **Something went wrong:** {error_msg}", icon="❌")

else:
    # Placeholder when nothing is uploaded yet
    st.info(
        "👆 Upload an image above to get started.  \n"
        "Accepted formats: **JPG, PNG, WEBP, GIF**",
        icon="📷",
    )

# ── Footer ─────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">Built with ❤️ + Streamlit + Google Gemini · '
    'Roasts are AI-generated and meant to be funny, not harmful.</div>',
    unsafe_allow_html=True,
)
