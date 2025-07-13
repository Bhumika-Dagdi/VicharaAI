import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from utils.logger import log_action
from config import CONFIG

def send_email(st):
    st.subheader("📧 Send Email")

    receiver = st.text_input("Receiver Email", key="email_receiver")
    subject = st.text_input("Subject", key="email_subject")
    body = st.text_area("Body", key="email_body")

    if st.button("Send Email"):
        try:
            msg = EmailMessage()
            msg["From"] = CONFIG['email']['sender']
            msg["To"] = receiver
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(CONFIG['email']['sender'], CONFIG['email']['app_password'])
                server.send_message(msg)

            st.success("✅ Email Sent Successfully!")
            log_action(f"Email sent to {receiver}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            log_action(f"Email error: {str(e)}")

def send_fake_email(st):
    st.subheader("📧 Send Anonymous Email")
    to = st.text_input("Recipient Email", key="ano_email_to")
    subject = st.text_input("Subject", key="ano_email_subject")
    body = st.text_area("Body", key="ano_email_body")

    if st.button("Send Anonymous Email"):
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = "anonymous@unknown.com"
            msg["To"] = to

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(CONFIG['email']['sender'], CONFIG['email']['app_password'])
                server.sendmail("anonymous@unknown.com", to, msg.as_string())

            st.success("✅ Anonymous Email Sent!")
            log_action(f"Anonymous email sent to {to}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            log_action(f"Anonymous email error: {str(e)}")
