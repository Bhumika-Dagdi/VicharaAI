import pywhatkit
from twilio.rest import Client
from utils.logger import log_action
from config import CONFIG

def send_whatsapp(st):
    st.subheader("📱 Send WhatsApp Message")
    number = st.text_input("Phone Number (+91...)", key="whatsapp_number")
    message = st.text_area("Message", key="whatsapp_message")

    if st.button("Send WhatsApp"):
        try:
            pywhatkit.sendwhatmsg_instantly(number, message, tab_close=True, close_time=3)
            st.success("✅ WhatsApp Message Sent!")
            log_action(f"WhatsApp sent to {number}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            log_action(f"WhatsApp error: {str(e)}")

def send_whatsapp_anon(st):
    st.subheader("📱 Send Anonymous WhatsApp Message")
    number = st.text_input("Phone Number", key="anon_whatsapp_number")
    message = st.text_area("Message", key="anon_whatsapp_message")

    if st.button("Send Anonymous WhatsApp"):
        try:
            client = Client(CONFIG['twilio']['account_sid'], CONFIG['twilio']['auth_token'])
            client.messages.create(body=message, from_=CONFIG['twilio']['whatsapp_number'], to=f"whatsapp:+91{number}")
            st.success("✅ Anonymous WhatsApp Sent!")
            log_action(f"Anonymous WhatsApp sent to {number}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            log_action(f"Anon WhatsApp error: {str(e)}")

def send_sms(st):
    st.subheader("📲 Send SMS")
    to_num = st.text_input("To Number (+91...)", key="sms_to_number")
    msg = st.text_area("Message", key="sms_message")

    if st.button("Send SMS"):
        if not to_num.startswith("+91") or len(to_num) != 13:
            st.warning("📵 Enter a valid Indian phone number starting with +91")
            return

        try:
            client = Client(CONFIG['twilio']['account_sid'], CONFIG['twilio']['auth_token'])
            message = client.messages.create(
                body=msg,
                from_=CONFIG['twilio']['sms_number'],
                to=to_num
            )
            st.success("✅ SMS sent!")
            log_action(f"SMS sent to {to_num}")
        except Exception as e:
            st.error(f"❌ SMS Error: {str(e)}")
            log_action(f"SMS error: {str(e)}")


def auto_call(st):
    st.subheader("📞 Make a Call")
    to_num = st.text_input("To Number (+91...)", key="call_to_number")

    if st.button("Make Call"):
        if not to_num.startswith("+91") or len(to_num) != 13:
            st.warning("📵 Enter a valid Indian phone number starting with +91")
            return

        try:
            client = Client(CONFIG['twilio']['account_sid'], CONFIG['twilio']['auth_token'])
            call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                from_=CONFIG['twilio']['sms_number'],
                to=to_num
            )
            st.success("✅ Call initiated!")
            log_action(f"Call made to {to_num}")
        except Exception as e:
            st.error(f"❌ Call Error: {str(e)}")
            log_action(f"Call error: {str(e)}")

