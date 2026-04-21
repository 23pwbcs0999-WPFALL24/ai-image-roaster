# 🔥 AI Vision Roast System

> Upload any image → let Google Gemini roast it → laugh (or cry).

A fun student demo project built with **Python + Streamlit + Google Gemini**.

---

## 📁 Project Structure

```
ai_vision_roast/
├── app.py              ← Main application (all UI + logic)
├── requirements.txt    ← Python packages to install
├── .env.example        ← Template for your API key
├── .env                ← YOUR real key goes here (never commit!)
├── .gitignore          ← Keeps .env out of Git
└── README.md           ← This file
```

---

## ⚙️ How It Works

```
User uploads image
       │
       ▼
Streamlit reads it with PIL (Pillow)
       │
       ▼
Image + custom prompt → sent to Gemini 2.5 Flash (vision model)
       │
       ▼
Gemini analyses image content and generates a funny, safe roast
       │
       ▼
Roast text displayed back in the Streamlit UI
```

**Key components:**
| File / Library        | Role                                      |
|-----------------------|-------------------------------------------|
| `streamlit`           | Builds the entire web UI                  |
| `google-generativeai` | Calls Gemini API for image understanding  |
| `Pillow (PIL)`        | Reads/converts uploaded image files       |
| `python-dotenv`       | Safely loads `GEMINI_API_KEY` from `.env` |

---

## 🚀 Setup Instructions (Windows + VS Code)

### Step 1 — Get a Free Gemini API Key

1. Go to → **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (it looks like `AIzaSy...`)

---

### Step 2 — Set Up the Project

Open your terminal (PowerShell or VS Code Terminal) and run:

```bash
# Navigate to where you want the project
cd C:\Users\YourName\Projects

# Create a new folder and enter it
mkdir ai_vision_roast
cd ai_vision_roast
```

Copy all project files into this folder.

---

### Step 3 — Create & Activate a Virtual Environment

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
venv\Scripts\Activate.ps1

# OR if using Command Prompt (cmd.exe)
venv\Scripts\activate.bat

# You should now see (venv) in your prompt
```

> 💡 If PowerShell gives a security error, run:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs: `streamlit`, `google-generativeai`, `Pillow`, `python-dotenv`

---

### Step 5 — Add Your API Key

```bash
# Copy the example file
copy .env.example .env
```

Open `.env` in VS Code and replace the placeholder:

```
GEMINI_API_KEY=AIzaSyYourRealKeyHere
```

Save the file. **Never share or commit this file!**

---

### Step 6 — Run the App

```bash
streamlit run app.py
```

Your browser will automatically open to:
```
http://localhost:8501
```

---

## 🧪 Testing Steps

1. **Upload a photo** — try a selfie, a food pic, a pet, a messy desk
2. Click **"🔥 GENERATE ROAST"**
3. Watch Gemini analyse the image and drop a witty roast
4. Upload another image and repeat!

**Test edge cases:**
- Try a PNG with transparency → app converts it to RGB automatically
- Run without a `.env` file → app shows a helpful warning and demo mode
- Upload an unusual file type → uploader restricts to safe formats

---

## 🛡️ Safety & Content Policy

The prompt sent to Gemini explicitly instructs it to:
- ✅ Be funny and playful
- ✅ Roast the situation, style, or vibes
- ❌ Never be racist, sexist, or hateful
- ❌ Never attack someone's physical appearance or identity
- ❌ Never produce sexual or abusive content

Gemini also has its own built-in safety filters as a second layer.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Make sure your `(venv)` is active and you ran `pip install -r requirements.txt` |
| `Invalid API Key` | Double-check the key in your `.env` file (no spaces, no quotes) |
| `quota exceeded` | You hit the free-tier limit; wait 1 minute or upgrade your Gemini plan |
| App won't open | Try `http://localhost:8501` manually in your browser |
| PowerShell execution error | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## 💡 Ideas to Extend This Project

- Add a **roast intensity slider** (mild → savage)
- Save roasts to a **history log** (SQLite or CSV)
- Add a **share to Twitter** button
- Support **video frames** or **webcam capture**
- Add **multiple roast styles** (Shakespearean, Gen-Z, Corporate)

---

*Built with ❤️ using Streamlit + Google Gemini · For demo and educational purposes only.*
