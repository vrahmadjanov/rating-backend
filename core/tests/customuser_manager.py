from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserManagerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'phone_number': '+992123456789',
            'first_name': 'Тест',
            'date_of_birth': '1990-01-01'
        }

    # Тесты create_user
    def test_create_user_with_valid_data(self):
        """Тест создания обычного пользователя с валидными данными"""
        user = CustomUser.objects.create_user(**self.valid_data)
        
        self.assertEqual(user.phone_number, '+992123456789')
        self.assertEqual(user.first_name, 'Тест')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password(None))
        self.assertFalse(user.check_password('wrong_password'))
        self.assertFalse(user.has_usable_password())

    def test_create_user_with_password(self):
        """Тест создания пользователя с паролем"""
        user = CustomUser.objects.create_user(
            **self.valid_data,
            password='testpass123'
        )
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_missing_phone_number(self):
        """Тест создания пользователя без номера телефона"""
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                phone_number='',
                first_name='Тест',
                date_of_birth='1990-01-01'
            )
        self.assertEqual(str(context.exception), 'Пользователь должен иметь номер телефона')

    def test_create_user_missing_first_name(self):
        """Тест создания пользователя без имени"""
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                phone_number='+992123456789',
                # Пропущен first_name
            )

    def test_create_user_with_extra_fields(self):
        """Тест создания пользователя с дополнительными полями"""
        user = CustomUser.objects.create_user(
            **self.valid_data,
            last_name='Тестов',
            email='test@example.com'
        )
        self.assertEqual(user.last_name, 'Тестов')
        self.assertEqual(user.email, 'test@example.com')

    def test_create_user_inactive(self):
        """Тест создания неактивного пользователя"""
        user = CustomUser.objects.create_user(
            **self.valid_data,
            is_active=False
        )
        self.assertFalse(user.is_active)

    # Тесты create_superuser
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = CustomUser.objects.create_superuser(
            phone_number='+992987654321',
            first_name='Админ',
            date_of_birth='1980-01-01'
        )
        
        self.assertEqual(admin.phone_number, '+992987654321')
        self.assertEqual(admin.first_name, 'Админ')
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_missing_required_fields(self):
        """Тест создания суперпользователя без обязательных полей"""
        with self.assertRaises(TypeError):
            CustomUser.objects.create_superuser(
                phone_number='+992987654321',
                # Пропущен first_name
            )

    def test_create_superuser_with_password(self):
        """Тест создания суперпользователя с паролем"""
        admin = CustomUser.objects.create_superuser(
            phone_number='+992987654321',
            first_name='Админ',
            date_of_birth='1980-01-01',
            password='adminpass'
        )
        self.assertTrue(admin.check_password('adminpass'))