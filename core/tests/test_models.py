from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        """
        Тест создания пользователя с минимальными обязательными полями.
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456789",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            is_active=False  # Указываем, что пользователь не активен
        )
        self.assertEqual(user.phone_number, "+992123456789")
        self.assertEqual(user.first_name, "Иван")
        self.assertEqual(user.last_name, "Иванов")
        self.assertEqual(user.middle_name, "")
        self.assertIsNone(user.email)
        self.assertIsNotNone(user.profile_picture)  # Проверяем, что объект существует
        self.assertIsNone(user.profile_picture.name)  # Проверяем, что файл не загружен
        self.assertIsNone(user.gender)
        self.assertIsNone(user.inn)
        self.assertFalse(user.is_active)  # Пользователь не активен до подтверждения email
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Тест создания суперпользователя.
        """
        superuser = CustomUser.objects.create_superuser(
            phone_number="+992123456788",
            first_name="Админ",
            last_name="Админов",
            password="admin123"
        )
        self.assertEqual(superuser.phone_number, "+992123456788")
        self.assertEqual(superuser.first_name, "Админ")
        self.assertEqual(superuser.last_name, "Админов")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)  # Суперпользователь активен по умолчанию

    def test_generate_confirmation_code(self):
        """
        Тест генерации кода подтверждения.
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            password="password123"
        )
        user.generate_confirmation_code()
        self.assertEqual(len(user.confirmation_code), 6)  # Код должен быть 6-значным
        self.assertIsNotNone(user.confirmation_code_created_at)

    def test_is_confirmation_code_valid(self):
        """
        Тест проверки действительности кода подтверждения.
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            password="password123"
        )
        user.generate_confirmation_code()
        self.assertTrue(user.is_confirmation_code_valid(user.confirmation_code))  # Код действителен

        # Проверка истечения срока действия кода
        user.confirmation_code_created_at = timezone.now() - timezone.timedelta(hours=2)
        user.save()
        self.assertFalse(user.is_confirmation_code_valid(user.confirmation_code))  # Код истек

    def test_user_str_representation(self):
        """
        Тест строкового представления пользователя.
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            password="password123"
        )
        self.assertEqual(str(user), "Иванов Иван (+992123456787)")

    def test_user_full_name(self):
        """
        Тест метода get_full_name().
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
            password="password123"
        )
        self.assertEqual(user.get_full_name(), "Иванов Иван Иванович")

    def test_user_full_name_without_middle_name(self):
        """
        Тест метода get_full_name() без отчества.
        """
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            password="password123"
        )
        self.assertEqual(user.get_full_name(), "Иванов Иван")

    def test_user_phone_number_validation(self):
        """
        Тест валидации номера телефона.
        """
        # Корректный номер телефона
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            email="test@test.example",
            password="password123"
        )
        self.assertEqual(user.email, "test@test.example")

        # Некорректный номер телефона
        user = CustomUser(
            phone_number="+99212345",
            first_name="Иван",
            last_name="Иванов",
            email="test2@test.example",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("Номер телефона должен быть в формате: '+992XXYYYYYY'.", str(context.exception))

    def test_user_inn_validation(self):
        """
        Тест валидации ИНН.
        """
        # Корректный ИНН
        user = CustomUser.objects.create_user(
            phone_number="+992123456787",
            first_name="Иван",
            last_name="Иванов",
            inn="123456789012",
            password="password123"
        )
        self.assertEqual(user.inn, "123456789012")

        # Некорректный ИНН (меньше 12 цифр)
        user = CustomUser(
            phone_number="+992123456788",
            first_name="Иван",
            last_name="Иванов",
            inn="123",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("ИНН должен состоять из 12 цифр.", str(context.exception))

        # Некорректный ИНН (больше 12 цифр)
        user = CustomUser(
            phone_number="+992123456789",
            first_name="Иван",
            last_name="Иванов",
            inn="1234567890123",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("ИНН должен состоять из 12 цифр.", str(context.exception))

    def test_user_email_uniqueness(self):
        """
        Тест уникальности email.
        """
        CustomUser.objects.create_user(
            phone_number="+992123456789",
            email="test@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123"
        )
        user = CustomUser(
            phone_number="+992123456788",
            email="test@example.com",
            first_name="Петр",
            last_name="Петров",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("Пользователь с таким email уже существует.", str(context.exception))

    def test_user_phone_number_uniqueness(self):
        """
        Тест уникальности номера телефона.
        """
        CustomUser.objects.create_user(
            email="test1@example.com",
            first_name="Иван",
            last_name="Иванов",
            phone_number="+992123456789",
            password="password123"
        )
        user = CustomUser(
            email="test2@example.com",
            first_name="Петр",
            last_name="Петров",
            phone_number="+992123456789",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("Пользователь с таким номером телефона уже существует.", str(context.exception))

    def test_user_inn_uniqueness(self):
        """
        Тест уникальности ИНН.
        """
        CustomUser.objects.create_user(
            phone_number="+992123456789",
            email="test1@example.com",
            first_name="Иван",
            last_name="Иванов",
            inn="123456789012",
            password="password123"
        )
        user = CustomUser(
            phone_number="+992123456789",
            email="test2@example.com",
            first_name="Петр",
            last_name="Петров",
            inn="123456789012",
            password="password123"
        )
        with self.assertRaises(ValidationError) as context:
            user.full_clean()
        self.assertIn("Пользователь с таким ИНН уже существует.", str(context.exception))