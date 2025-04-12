import hashlib
import smtplib
from email.mime.text import MIMEText
from app.config import settings

characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num):
    """ converts hashed value to base62 """
    if num == 0:
        return characters[0]
    base62 = []
    while num > 0:
        num, remainder = divmod(num, 62)
        base62.append(characters[remainder])
    return ''.join(reversed(base62))


def generate_unique_id(long_url, user_id):
    unique_input = f"{long_url}-{user_id}"
    
    hash_object = hashlib.sha256(unique_input.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    short_id = encode_base62(hash_int)[:8]
    return short_id


def send_reset_email(to_email: str, reset_token: str):
    reset_url = f"{settings.base_url}reset-password?token={reset_token}"
    msg = MIMEText(f"Click the link to reset your password:\n\n{reset_url}")
    msg["Subject"] = "Reset Your Password"
    msg["From"] = "crishsarthak@gmail.com"
    msg["To"] = to_email

    # Replace with your actual SMTP details
    smtp_server = settings.smtp_server
    smtp_port = settings.smtp_port
    smtp_user = settings.smtp_user
    smtp_password = settings.smtp_password
    

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
