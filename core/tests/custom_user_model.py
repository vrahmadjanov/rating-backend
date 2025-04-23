from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import CustomUser
from a_base.models import City, Region
from subscriptions.models import Subscription

class CustomUserModelTest(TestCase):
    def setUp(self):
        """Создаем тестовые данные для всех тестов"""
        self.region = Region.objects.create(name="Душанбе")
        self.city = City.objects.create(name="Душанбе", region=self.region)
        self.subscription = Subscription.objects.create(
            name="Премиум",
            duration_days=30,
            price=1000
        )
        
        # Основной тестовый пользователь
        self.user_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'date_of_birth': '1990-01-01',
            'phone_number': '+992123456789',
            'city': self.city,
        }
        
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Тест создания пользователя с обязательными полями"""
        self.assertEqual(self.user.first_name, 'Иван')
        self.assertEqual(self.user.last_name, 'Иванов')
        self.assertEqual(self.user.phone_number, '+992123456789')
        self.assertEqual(self.user.date_of_birth, '1990-01-01')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.email_verified)

    def test_phone_number_validation(self):
        """Тест валидации номера телефона"""
        # Неправильный формат номера
        with self.assertRaises(ValidationError):
            user = CustomUser(
                first_name='Петр',
                last_name='Петров',
                date_of_birth='1990-01-01',
                phone_number='992123456789'  # отсутствует +
            )
            user.full_clean()
            
        # Слишком короткий номер
        with self.assertRaises(ValidationError):
            user = CustomUser(
                first_name='Петр',
                last_name='Петров',
                date_of_birth='1990-01-01',
                phone_number='+99212345678'  # 12 символов вместо 13
            )
            user.full_clean()

    def test_inn_validation(self):
        """Тест валидации ИНН"""
        # Правильный ИНН
        self.user.inn = '123456789'
        self.user.full_clean()
        
        # Неправильная длина ИНН
        with self.assertRaises(ValidationError):
            self.user.inn = '12345678'
            self.user.full_clean()
            
        # Нечисловые символы в ИНН
        with self.assertRaises(ValidationError):
            self.user.inn = '1234a6789'
            self.user.full_clean()

    def test_get_full_name_property(self):
        """Тест свойства get_full_name"""
        # С отчеством
        self.assertEqual(self.user.get_full_name, 'Иванов Иван Иванович')
        
        # Без отчества
        self.user.middle_name = None
        self.assertEqual(self.user.get_full_name, 'Иванов Иван')

    def test_gender_choices(self):
        """Тест выбора пола"""
        self.user.gender = CustomUser.Gender.MALE
        self.assertEqual(self.user.gender, 'M')
        self.assertEqual(self.user.get_gender_display(), 'Мужской')
        
        self.user.gender = CustomUser.Gender.FEMALE
        self.assertEqual(self.user.gender, 'F')
        self.assertEqual(self.user.get_gender_display(), 'Женский')

    def test_confirmation_code_methods(self):
        """Тест методов для работы с кодом подтверждения"""
        # Генерация кода
        self.user.generate_confirmation_code()
        self.assertEqual(len(self.user.confirmation_code), 6)
        self.assertIsNotNone(self.user.confirmation_code_created_at)
        
        # Проверка кода
        code = self.user.confirmation_code
        self.assertTrue(self.user.is_confirmation_code_valid(code))
        
        # Проверка просроченного кода
        self.user.confirmation_code_created_at = timezone.now() - timedelta(hours=2)
        self.assertFalse(self.user.is_confirmation_code_valid(code))

    def test_subscription_methods(self):
        """Тест методов подписки"""
        # Активация подписки
        self.user.subscription = self.subscription
        self.user.subscription_start_date = timezone.now()
        self.user.activate_subscription()
        
        # Проверка даты окончания подписки
        expected_end_date = self.user.subscription_start_date + timedelta(days=30)
        self.assertEqual(self.user.subscription_end_date, expected_end_date)
        
        # Проверка активной подписки
        self.assertTrue(self.user.has_active_subscription)
        
        # Проверка неактивной подписки (после истечения срока)
        self.user.subscription_end_date = timezone.now() - timedelta(days=1)
        self.assertFalse(self.user.has_active_subscription)
        
        # Проверка отсутствия подписки
        self.user.subscription = None
        self.assertFalse(self.user.has_active_subscription)

    def test_unique_constraints(self):
        """Тест уникальности phone_number и inn"""
        # Проверка уникальности phone_number
        with self.assertRaises(Exception):  # IntegrityError или ValidationError
            CustomUser.objects.create_user(
                first_name='Дубликат',
                last_name='Тест',
                date_of_birth='1990-01-01',
                phone_number=self.user.phone_number  # Дублируем номер
            )
        
        # Проверка уникальности inn
        if self.user.inn:
            with self.assertRaises(Exception):
                new_user = CustomUser(
                    first_name='Дубликат',
                    last_name='Тест',
                    date_of_birth='1990-01-01',
                    phone_number='+992987654321',
                    inn=self.user.inn
                )
                new_user.full_clean()

    def test_required_fields(self):
        """Тест обязательных полей"""
        # Пропущен first_name (REQUIRED_FIELDS)
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                phone_number='+992987654321',
                # Пропущен first_name
            )
        
        # Пропущен date_of_birth (REQUIRED_FIELDS)
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='+992987654322',
                first_name='Тест',
                # Пропущен date_of_birth
            )
            user.full_clean()

    def test_email_field(self):
        """Тест поля email (необязательное)"""
        # Создание без email
        user = CustomUser.objects.create_user(
            first_name='Без',
            last_name='Email',
            date_of_birth='1990-01-01',
            phone_number='+992111111111',
            city=self.city
        )
        self.assertIsNone(user.email)
        
        # Создание с email
        user.email = 'test@example.com'
        user.full_clean()  # Должно пройти без ошибок

    def test_str_representation(self):
        """Тест строкового представления пользователя"""
        self.assertEqual(str(self.user), 'Иванов Иван Иванович (+992123456789)')
        
        # Без отчества
        self.user.middle_name = None
        self.assertEqual(str(self.user), 'Иванов Иван (+992123456789)')