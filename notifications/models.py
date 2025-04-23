from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Получаем модель пользователя, используемую в проекте
User = get_user_model()

class Notification(models.Model):
    """
    Модель для управления уведомлениями, отправляемыми пользователям.
    Поддерживает три типа уведомлений: email, SMS и push-уведомления.
    """

    # Типы уведомлений
    NOTIFICATION_TYPE_CHOICES = (
        ("email", "Email"),  # Уведомление по электронной почте
        ("sms", "SMS"),      # SMS-уведомление
        ("push", "Push"),    # Push-уведомление
    )

    # Получатель уведомления (связь с моделью пользователя)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получатель")

    # Тип уведомления (email, sms, push)
    type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        default="email",
        verbose_name="Тип уведомления"
    )

    # Тема уведомления (используется для email)
    subject = models.CharField(max_length=100, verbose_name="Тема")

    # Текст уведомления (может содержать HTML для email)
    message = models.TextField(blank=True, null=True, verbose_name="Сообщение")

    # Дата и время создания уведомления (автоматически заполняется)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # Статус отправки уведомления (по умолчанию False)
    sended = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)

    def send_email(self):
        """
        Отправляет уведомление в зависимости от его типа.
        Поддерживается только тип 'email'. Для других типов выводится предупреждение.

        Возвращает:
            bool: True, если уведомление успешно отправлено, иначе False.
        """
        if self.type == "email":
            try:
                # Создаем MIME-сообщение
                message = MIMEMultipart("alternative")
                message["From"] = settings.EMAIL_HOST_USER  # Отправитель
                message["To"] = self.recipient.email         # Получатель
                message["Subject"] = self.subject           # Тема письма

                # Добавляем текстовую версию письма
                text_part = MIMEText(self.message, "plain")

                # Добавляем HTML-версию письма
                html_part = MIMEText(self.message, "html")

                # Прикрепляем обе версии к сообщению
                message.attach(text_part)
                message.attach(html_part)

                # Устанавливаем соединение с SMTP-сервером
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls()  # Включаем защиту TLS
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Авторизация
                    server.send_message(message)  # Отправка письма

                # Помечаем уведомление как отправленное
                self.sended = True
                self.save()
                return True
            except Exception as e:
                # Логируем ошибку, если отправка не удалась
                print(f"Ошибка при отправке email: {e}")
                return False
        else:
            # Выводим предупреждение для неподдерживаемых типов
            print(f"Тип уведомления '{self.type}' не поддерживается.")
            return False

    def __str__(self):
        """
        Возвращает строковое представление уведомления.
        Формат: "To: <получатель> | subject: <тема> | type: <тип>"
        """
        return f'To: {self.recipient} | subject: {self.subject} | type: {self.type}'