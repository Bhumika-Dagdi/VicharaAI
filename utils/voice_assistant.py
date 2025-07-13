import os
import datetime
import speech_recognition as sr
import streamlit as st
from serpapi import GoogleSearch
from config import CONFIG
from utils.logger import log_action
from utils.constants import ALERT_KEYWORDS

# --- Google Search via SerpAPI ---
def search_response_with_serpapi(query):
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY") or CONFIG["serpapi"]["api_key"]
    })
    results = search.get_dict().get("organic_results", [])
    return results[:3]

# --- Listen from Microphone ---
def listen_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            st.info("🎤 Listening... Please speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            command = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {command}")
            log_action(f"Voice command recognized: {command}")
            return command.lower()

        except sr.UnknownValueError:
            st.warning("❌ Couldn't understand your voice. Please try again.")
            log_action("Voice command not recognized")
        except sr.RequestError as e:
            st.error(f"⚠️ Could not request results; {e}")
            log_action(f"Voice recognition error: {e}")

    except sr.WaitTimeoutError:
        st.warning("⌛ Listening timed out while waiting for phrase.")
        log_action("Voice command listening timed out")

    return None

# --- Route to Action ---
def route_command(command, st):
    if not command:
        st.warning("🛑 No valid command to process.")
        return

    if "whatsapp" in command and "send" in command:
        st.info("📱 Opening WhatsApp sender...")
        from utils.whatsapp_tools import send_whatsapp
        send_whatsapp(st)

    elif "email" in command and "send" in command:
        st.info("📧 Opening Email tool...")
        from utils.email_tools import send_email
        send_email(st)

    elif "system" in command or "ram" in command or "monitor" in command:
        st.info("🖥️ Showing system monitor...")
        from utils.system_monitor import system_monitor_viz
        system_monitor_viz()

    elif "ssh" in command or "remote" in command:
        st.info("🧑‍💻 Opening SSH command tool...")
        from utils.ssh_tools import execute_ssh_command
        st.warning("🔐 Please enter SSH credentials manually in the Home tab.")

    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        st.info(f"🔍 Searching Google for: {query}")
        results = search_response_with_serpapi(query)
        for i, result in enumerate(results, 1):
            st.markdown(f"**{i}. [{result.get('title')}]({result.get('link')})**")

    else:
        st.warning("🤷‍♀️ Sorry, I didn't recognize that command.")
        log_action(f"Unknown command: {command}")

# --- Streamlit Wrapper ---
def listen_and_respond():
    st.info("🎙️ Listening for your voice command...")
    command = listen_command()
    if command:
        st.write(f"🗣️ You said: `{command}`")
        is_alert = any(kw in command.lower() for kw in ALERT_KEYWORDS)
        if not is_alert:
            route_command(command, st)
        return command, is_alert
        
    else:
        st.warning("🚫 No valid command detected.")
        return None, False