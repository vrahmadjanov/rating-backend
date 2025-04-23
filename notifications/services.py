# services.py
import requests
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def send_email(recipient_email, subject, message, is_html=False):
    """
    Отправляет email указанному получателю.

    Аргументы:
        recipient_email (str): Email адрес получателя.
        subject (str): Тема письма.
        message (str): Текст письма (может быть HTML).
        is_html (bool): Если True, сообщение считается HTML. По умолчанию False.

    Возвращает:
        bool: True, если email успешно отправлен, иначе False.
    """
    try:
        # Создаем MIME-сообщение
        email_message = MIMEMultipart("alternative")
        email_message["From"] = settings.EMAIL_HOST_USER  # Отправитель
        email_message["To"] = recipient_email             # Получатель
        email_message["Subject"] = subject                # Тема письма

        # Добавляем текстовую версию письма
        if is_html:
            # Если сообщение HTML, добавляем его как HTML-часть
            html_part = MIMEText(message, "html")
            email_message.attach(html_part)
        else:
            # Если сообщение обычное, добавляем его как текстовую часть
            text_part = MIMEText(message, "plain")
            email_message.attach(text_part)

        # Устанавливаем соединение с SMTP-сервером
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()  # Включаем защиту TLS
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Авторизация
            server.send_message(email_message)  # Отправка письма

        return True
    except Exception as e:
        # Логируем ошибку, если отправка не удалась
        print(f"Ошибка при отправке email: {e}")
        return False


def send_sms_aero(to, text):
    url = 'https://gate.smsaero.ru/v2/sms/send'
    auth = (settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
    data = {
        'number': to,          # Номер получателя
        'text': text,          # Текст сообщения
        'sign': settings.SMSAERO_FROM,  # Имя отправителя
        'channel': 'DIRECT',   # Канал отправки (DIRECT для SMS)
    }

    try:
        response = requests.post(url, json=data, auth=auth)
        response.raise_for_status()  # Проверка на ошибки
        return response.json()       # Возврат ответа от API
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при отправке SMS: {str(e)}")
    
