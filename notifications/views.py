from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fcm_django.models import FCMDevice
from firebase_admin import messaging
from .services import send_email, send_sms_aero
from rest_framework.permissions import AllowAny

class SendEmail(APIView):
    def post(self, request, *args, **kwargs):
        recipient_email = request.data.get('recipient_email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        is_html = request.data.get('is_html')
        try:
            send_email(recipient_email, subject, message, is_html)
            return Response({'status': 'Email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendSMSView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        message = request.data.get('message')

        if not phone_number or not message:
            return Response({'error': 'Phone number and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = send_sms_aero(phone_number, message)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendPushView(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем заголовок и тело уведомления из запроса
        title = request.data.get('title', 'Тестовое уведомление')
        body = request.data.get('body', 'Это пуш-уведомление из Django')

        # Проверяем, указаны ли title и body
        if not title or not body:
            return Response({'error': 'Title or body not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получаем все устройства (FCMDevice) из базы данных
            devices = FCMDevice.objects.all()

            # Если нет зарегистрированных устройств, возвращаем ошибку
            if not devices.exists():
                return Response({'error': 'No devices found'}, status=status.HTTP_404_NOT_FOUND)

            # Составляем список токенов регистраций устройств
            registration_ids = [device.registration_id for device in devices if device.registration_id]

            # Если нет действительных токенов, возвращаем ошибку
            if not registration_ids:
                return Response({'error': 'No valid registration IDs found'}, status=status.HTTP_400_BAD_REQUEST)

            success_count = 0
            failure_count = 0

            # Отправляем уведомления по одному устройству
            for registration_id in registration_ids:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    token=registration_id,
                )

                try:
                    # Отправка уведомления на одно устройство
                    response = messaging.send(message)
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    # Логирование ошибки (например, вывод в консоль)
                    print(f"Error sending push notification to {registration_id}: {str(e)}")

            return Response({
                'status': 'Notifications sent',
                'success_count': success_count,
                'failure_count': failure_count,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SaveDeviceTokenView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        device_type = request.data.get('type', 'web')  # android, ios, web
        user = request.user if request.user.is_authenticated else None

        if not token:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создаем или обновляем устройство
            device, created = FCMDevice.objects.update_or_create(
                registration_id=token,
                defaults={
                    'type': device_type,
                    'user': user  # Привязываем к пользователю, если он аутентифицирован
                }
            )
            
            message = 'Token created' if created else 'Token updated'
            return Response({'status': message}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)