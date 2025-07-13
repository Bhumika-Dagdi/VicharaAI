import streamlit as st
from utils.voice_assistant import listen_and_respond
from utils.logger import log_action
from utils.location_tracker import get_location_info
from utils.constants import ALERT_KEYWORDS
from utils.email_tools import send_email, send_fake_email
from utils.whatsapp_tools import send_whatsapp, send_sms, auto_call, send_whatsapp_anon
from utils.scrapper_tools import search_response_with_serpapi
from utils.qr_tools import generate_qr_code
from utils.translate_tools import language_translator
from utils.system_monitor import system_monitor_viz, read_ram
from utils.document_chat import chat_with_file_serpapi
from utils.file_manager import file_manager
from utils.pdf_tools import pdf_toolkit
from utils.horoscope_predictor import predict_horoscope
import datetime
from config import CONFIG
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="VicharaAI", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .icon-card {
        padding: 1.5rem;
        margin: 0.5rem;
        border-radius: 1.2rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: 0.3s ease-in-out;
    }
    .icon-card:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
        transform: scale(1.05);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Restart Application
if st.button("\U0001F504 Restart App"):
    st.rerun()

# --- Quick Action Sidebar Widgets ---
with st.sidebar:
    st.markdown("## ⚡ Quick Actions")

    # Emergency Mode Toggle
    st.toggle("\U0001F6E1️ Defense Mode", key="defense_mode")

    # Theme toggle (optional visual customization)
    theme = st.toggle("\U0001F3A8 Theme", key="theme")

    # Google Search Quick Tool
    query = st.text_input("\U0001F50D Quick Search", placeholder="Search with Google")
    if query:
        st.info(f"Top results for: {query}")
        results = search_response_with_serpapi(query)
        for i, result in enumerate(results, 1):
            st.markdown(f"{i}. [{result.get('title')}]({result.get('link')})")

def icon_navbar():
    st.markdown("<h1 style='text-align:center;'>\U0001F9E0 Welcome to VicharaAI</h1>", unsafe_allow_html=True)
    cols = st.columns(6)
    if cols[0].button("\U0001F3E0 Home"):
        st.session_state["page"] = "home"
    if cols[1].button("\U0001F399️ Voice"):
        st.session_state["page"] = "voice"
    if cols[2].button("\U0001F5C2️ File Manager"):
        st.session_state["page"] = "file_manager"
    if cols[3].button("\U0001F4E7 Comms"):
        st.session_state["page"] = "comms"
    if cols[4].button("\U0001F52E Horoscope"):
        st.session_state["page"] = "horoscope"
    if cols[5].button("\U0001F4CD Location"):
        st.session_state["page"] = "location"

icon_navbar()

if st.session_state["page"] == "home":
    st.subheader("\U0001F4CB Dashboard Overview")
    st.info("System & Resource Usage Overview")
    read_ram(st)
    system_monitor_viz()

elif st.session_state["page"] == "voice":
    st.subheader("\U0001F399️ Voice Assistant")
    if st.button("\U0001F3A7 Start Listening"):
        transcript, is_alert = listen_and_respond()
        st.write("\U0001F5E3️ You said:", transcript)
        if is_alert:
            st.error("\U0001F6A8 Alert keyword detected!")
            for keyword in ALERT_KEYWORDS:
                if keyword.lower() in transcript.lower():
                    alert_body = f"\U0001F6A8 [ALERT] Keyword: {keyword}\nTranscript: {transcript}\nTime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

                    if st.session_state.get("defense_mode", False):
                        st.warning("\U0001F6E1️ Defense Mode Active – Sending Location & SMS Alert")
                        location_data = get_location_info()
                        location_msg = ""
                        if "error" not in location_data:
                            location_msg = (
                                f"\n\U0001F4CD Location: {location_data.get('city')}, {location_data.get('state')}, {location_data.get('country')}"
                                f"\n\U0001F6F0️ Coordinates: {location_data.get('latlng')}"
                                f"\n\U0001F4BB IP: {location_data.get('ip')}"
                            )
                        else:
                            location_msg = "\n⚠️ Location: Could not be determined."
                        alert_body += location_msg

                        try:
                            from twilio.rest import Client
                            client = Client(CONFIG['twilio']['account_sid'], CONFIG['twilio']['auth_token'])
                            client.messages.create(
                                body=alert_body,
                                from_=CONFIG['twilio']['sms_number'],
                                to=CONFIG['twilio']['emergency_contact']
                            )
                            st.success("\U0001F4E8 Emergency SMS sent successfully!")
                        except Exception as e:
                            st.error("❌ Failed to send SMS alert.")
                            st.text(str(e))
                    else:
                        st.info("\U0001F512 Defense Mode is OFF – No SMS sent.")

                    st.warning(alert_body)
                    break
        else:
            st.info("\U0001F3A4 Voice received but no alert keyword triggered.")

elif st.session_state["page"] == "file_manager":
    file_manager()

elif st.session_state["page"] == "comms":
    st.header("\U0001F4E7 Communication Tools")
    with st.expander("\U0001F4F1 Send WhatsApp Message"):
        send_whatsapp(st)
    with st.expander("\U0001F4E7 Send Email"):
        send_email(st)
    with st.expander("\U0001F4E7 Send Anonymous Email"):
        send_fake_email(st)
    with st.expander("\U0001F4F1 Send Anonymous WhatsApp"):
        send_whatsapp_anon(st)
    with st.expander("\U0001F4F2 Send SMS"):
        send_sms(st)
    with st.expander("\U0001F4DE Make a Call"):
        auto_call(st)

elif st.session_state["page"] == "horoscope":
    predict_horoscope()

elif st.session_state["page"] == "location":
    st.subheader("\U0001F4CD Location Info")
    location = get_location_info()
    if "error" not in location:
        st.write("Location:", location)
        try:
            lat, lon = map(float, location.get("latlng", [0, 0]))
            st.map(data={"lat": [lat], "lon": [lon]})
        except:
            st.warning("Location data incomplete for map.")
    else:
        st.error("Failed to fetch location info.")

# === Footer ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
            border-radius: 10px; color: white; margin-top: 2rem;">
    <p>Built with ❤️ by Bhumika Dagdi • VicharaAI v2.0</p>
</div>
""", unsafe_allow_html=True)
