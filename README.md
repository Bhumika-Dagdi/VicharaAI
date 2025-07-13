# 🤖 VicharaAI v2.0

**VicharaAI** is an intelligent, modular personal assistant built with **Python** and **Streamlit**. It features real-time voice recognition, smart file management, location tracking, emergency defense mode, multilingual tools, document interaction, and more — all inside an elegant UI.

---

## 🚀 Features

### 🎙️ Voice Assistant
- Real-time voice-to-text using microphone input.
- Keyword-based **defense mode**: triggers alerts, SMS, and location fetch.
- Automatically logs actions and interactions.

### 🗂️ Smart File Manager
- Upload, rename, delete, move/copy files between folders.
- Filter by file type, size, or name.
- Preview formats: `TXT`, `PDF`, `CSV`, `JSON`, `DOCX`, `JPG`, `PNG`, `JPEG`.
- Admin-only access via password.
- Download support, folder creation, and image conversion (PNG ⇄ JPG).

### 📧 Communication Tools
- Send:
  - ✅ Email (SMTP)
  - ✅ Anonymous Email
  - ✅ WhatsApp messages
  - ✅ Anonymous WhatsApp messages
  - ✅ SMS
  - ✅ Automated Calls
- Powered by `Twilio` API and WhatsApp automation tools.

### 📍 Location Tracker
- Get public IP-based city, state, country, and coordinates.
- Displays current map location using `st.map`.

### 🔮 Hybrid Horoscope Predictor
- Predict horoscope based on Zodiac, mood, and age.
- Fuses ML-based prediction with live API horoscope feed.

### 📦 Utility Tools
- Language translation (multilingual via `translate` library).
- QR code generator.
- Chat with uploaded PDFs/CSVs using context-aware Q&A.

### 🛡️ Emergency Defense Mode
- Toggleable emergency system.
- On keyword trigger:
  - Detects keyword
  - Fetches your location
  - Sends **SMS with location + timestamp**
  - Logs alert to the system

---

## 🧪 Tech Stack

| Layer         | Tools/Libs                                   |
|---------------|----------------------------------------------|
| Frontend      | `Streamlit`, `PIL`, `Matplotlib`             |
| Voice         | `SpeechRecognition`, `PyAudio`               |
| Chat          | `OpenAI API`                                 |
| Communication | `Twilio`, `SMTP`, `pywhatkit`                |
| System Access | `os`, `shutil`, `psutil`                     |
| ML/Logic      | `scikit-learn`, `pandas`, `joblib`           |
| Others        | `docx`, `pdfplumber`, `base64`, `requests`   |

---

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/Bhumika-Dagdi/VicharaAI.git
   cd VicharaAI
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up credentials**

   Create a .env or config.py and add:
   ```bash
   CONFIG = {
    'twilio': {
        'account_sid': 'YOUR_SID',
        'auth_token': 'YOUR_TOKEN',
        'sms_number': '+1XXXXXXXXXX',
        'emergency_contact': '+91XXXXXXXXXX'
    }
   }

   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

### **🧠 Architecture Overview**
```bash
📁 VicharaAI/
│
├── app.py                     # Main Streamlit UI & routing
├── config.py 
├── .env                        # Secrets and credentials
├── requirements.txt           # Dependencies
├── uploaded_files/            # File uploads managed by user
│
├── utils/
│   ├── voice_assistant.py     # Voice control, alert detection
│   ├── logger.py              # Logging actions
│   ├── location_tracker.py    # Location detection
│   ├── constants.py           # Alert keyword list
│   ├── whatsapp_tools.py      # WhatsApp/SMS/call modules
│   ├── email_tools.py         # Email & anonymous email
│   ├── qr_tools.py            # QR code generation
│   ├── translate_tools.py     # Language translator
│   ├── document_chat.py       # PDF/CSV Q&A
│   ├── pdf_tools.py           # PDF utilities
│   ├── file_manager.py        # Advanced file manager logic
│   └── horoscope_predictor.py # Hybrid ML + API predictor

```

### **🔐 Security**

- Admin access protected with password prompt.

- .gitignore includes sensitive paths like .env, uploaded_files/, __pycache__/, etc.

- GitHub secret scanning will block pushes with hardcoded API keys — move credentials to .env or config.py.

### **👩‍💻 Author**

Bhumika Dagdi

Final Year B.Tech CS(AI) – SKIT, Jaipur

📫 [LinkedIn](linkedin.com/in/bhumika-dagdi) • [GitHub](github.com/Bhumika-Dagdi)
