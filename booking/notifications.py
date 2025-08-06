import os
import smtplib
from email.message import EmailMessage
import requests

def send_email(to_addr: str, subject: str, body: str):
    """
    Отправляет Email через SMTP.
    Если сервер поддерживает STARTTLS — шифруем соединение и логинимся,
    иначе отправляем без шифрования (например, локальный Debug-сервер).
    """
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT") or 0)
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")

    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port) as smtp:
        if smtp.has_extn("starttls"):
            smtp.starttls()
            if user and pwd:
                smtp.login(user, pwd)
        smtp.send_message(msg)

    print(f"Email sent to {to_addr}")


def send_sms(phone: str, body: str):
    """
    Заглушка для отправки SMS. Вместо print() можно вызвать реальный API через requests.
    """
    print(f"SMS to {phone}: {body}")
