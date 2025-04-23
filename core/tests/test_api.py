from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

CustomUser = get_user_model()

class CustomUserAPITest(APITestCase):
    def setUp(self):
        """
        Настройка данных для тестов.
        """
        self.user_data = {
            "phone_number": "+992123456789",
            "first_name": "Иван",
            "last_name": "Иванов",
            "password": "password123"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_user(self):
        """
        Тест регистрации пользователя через API.
        """
        url = reverse("register")  # URL для регистрации
        data = {
            "phone_number": "+992123456789",
            "first_name": "Петр",
            "last_name": "Петров",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        user = CustomUser.objects.get(phone_number="+992123456789")
        self.assertFalse(user.is_active)  # Пользователь не активен до подтверждения email
