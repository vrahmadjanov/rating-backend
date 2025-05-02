from django.test import TestCase
from django.utils.translation import activate
from a_base.models import ExperienceLevel
from django.utils import translation
from rest_framework.test import APIRequestFactory, APIClient
from a_base.serializers import ExperienceLevelSerializer
from django.conf import settings
from django.urls import reverse
from rest_framework import status


class ExperienceLevelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.experience_level = ExperienceLevel.objects.create(
            level="1-3 года",
            level_ru="1-3 года",
            level_tg="1-3 сол"
        )

    def test_model_creation(self):
        """Тест создания модели"""
        self.assertEqual(ExperienceLevel.objects.count(), 1)
        self.assertEqual(self.experience_level.level, "1-3 года")

    def test_model_str_representation(self):
        """Тест строкового представления модели"""
        self.assertEqual(str(self.experience_level), "1-3 года")

    def test_unique_constraint(self):
        """Тест уникальности уровня"""
        with self.assertRaises(Exception):
            ExperienceLevel.objects.create(
                level="1-3 года",
                level_ru="1-3 года",
                level_tg="1-3 сол"
            )

    def test_translation_ru(self):
        """Тест русского перевода"""
        activate('ru')
        self.experience_level.level_ru = "1-3 года (рус)"
        self.experience_level.save()
        self.assertEqual(self.experience_level.level, "1-3 года (рус)")

    def test_translation_tg(self):
        """Тест таджикского перевода"""
        activate('tg')
        self.experience_level.level_tg = "1-3 сол (тг)"
        self.experience_level.save()
        self.assertEqual(self.experience_level.level, "1-3 сол (тг)")


class ExperienceLevelSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные один раз для всех тестов
        cls.level = ExperienceLevel.objects.create(
            level="1-3 года",
            level_ru="1-3 года (рус)",
            level_tg="1-3 сол (тг)"
        )
        cls.factory = APIRequestFactory()

    def setUp(self):
        # Сбрасываем язык перед каждым тестом
        translation.deactivate_all()

    def test_serializer_fields(self):
        """Тест наличия правильных полей в сериализаторе"""
        serializer = ExperienceLevelSerializer(instance=self.level)
        self.assertEqual(set(serializer.data.keys()), {'id', 'level'})

    def test_serializer_ru_translation(self):
        """Тест сериализатора с русским языком"""
        translation.activate('ru')
        serializer = ExperienceLevelSerializer(instance=self.level)
        self.assertEqual(serializer.data['level'], "1-3 года (рус)")

    def test_serializer_tg_translation(self):
        """Тест сериализатора с таджикским языком"""
        translation.activate('tg')
        serializer = ExperienceLevelSerializer(instance=self.level)
        self.assertEqual(serializer.data['level'], "1-3 сол (тг)")

    def test_serializer_fallback_language(self):
        """Тест fallback языка в сериализаторе"""
        # Устанавливаем язык, для которого нет перевода
        translation.activate('en')
        
        # Проверяем, что используется fallback (в данном случае русский)
        serializer = ExperienceLevelSerializer(instance=self.level)
        self.assertEqual(serializer.data['level'], "1-3 года (рус)")

    def test_serializer_with_request_context(self):
        """Тест сериализатора с переданным языком в контексте запроса"""
        request = self.factory.get('/')
        translation.activate('tg')
        serializer = ExperienceLevelSerializer(
            instance=self.level,
            context={'request': request}
        )
        self.assertEqual(serializer.data['level'], "1-3 сол (тг)")

    def test_serializer_no_translation(self):
        """Тест случая, когда нет перевода и fallback"""
        # Создаем объект без переводов
        no_translation_level = ExperienceLevel.objects.create(level="No translation")
        
        translation.activate('fr')  # Язык без перевода и без fallback
        serializer = ExperienceLevelSerializer(instance=no_translation_level)
        self.assertEqual(serializer.data['level'], "No translation")

    def test_serializer_with_custom_fallback(self):
        """Тест с пользовательским fallback языком"""
        # Сохраняем оригинальные настройки
        original_fallback = settings.FALLBACK_LANGUAGES
        
        try:
            # Устанавливаем пользовательский fallback
            settings.FALLBACK_LANGUAGES = {'fr': 'tg'}
            translation.activate('fr')
            
            serializer = ExperienceLevelSerializer(instance=self.level)
            self.assertEqual(serializer.data['level'], "1-3 сол (тг)")
        finally:
            # Восстанавливаем оригинальные настройки
            settings.FALLBACK_LANGUAGES = original_fallback

    def test_fallback_language(self):
        """Тест fallback языка, если перевод отсутствует"""
        activate('en')  # Язык без перевода
        self.assertEqual(self.level.level, "1-3 года (рус)")


class ExperienceLevelViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.api_client = APIClient()
        cls.factory = APIRequestFactory()
        cls.list_url = reverse('experience_level-list')
        
        # Создаем тестовые данные
        cls.level1 = ExperienceLevel.objects.create(
            level="1-3 года",
            level_ru="1-3 года (рус)",
            level_tg="1-3 сол (тг)"
        )
        cls.level2 = ExperienceLevel.objects.create(
            level="4-6 лет",
            level_ru="4-6 лет (рус)",
            level_tg="4-6 сол (тг)"
        )

    def setUp(self):
        # Сбрасываем язык перед каждым тестом
        translation.deactivate_all()

    def test_list_with_language_header(self):
        """Тест списка с языком из заголовка"""
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['level'], "1-3 сол (тг)")
        self.assertEqual(response.data[1]['level'], "4-6 сол (тг)")
        
        # Проверяем, что язык действительно активирован
        self.assertEqual(translation.get_language(), 'tg')

    def test_retrieve_with_language_header(self):
        """Тест детального просмотра с языком из заголовка"""
        url = reverse('experience_level-detail', args=[self.level1.id])
        response = self.client.get(
            url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['level'], "1-3 года (рус)")
        self.assertEqual(translation.get_language(), 'ru')

    def test_language_fallback(self):
        """Тест fallback языка при неизвестном языке в заголовке"""
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='fr'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['level'], "1-3 года (рус)")

    def test_permissions_read_only(self):
        """Тест прав доступа для неавторизованного пользователя (read only)"""
        # GET разрешен
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # POST запрещен
        response = self.client.post(self.list_url, {
            'level': '7-10 лет',
            'level_ru': '7-10 лет (рус)',
            'level_tg': '7-10 сол (тг)'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_permissions(self):
        """Тест прав доступа для администратора"""
        # Здесь нужно имитировать администратора
        # Предположим, что у вас есть метод is_admin в пользователе
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin = User.objects.create_superuser(
            phone_number='+992123456789',
            password='testpass123',
            first_name='Admin',
            date_of_birth='1990-01-01',
        )

        self.api_client.force_authenticate(user=admin)
        
        # POST должен быть разрешен для администратора
        response = self.api_client.post(self.list_url, {
            'level': '7-10 лет',
            'level_ru': '7-10 лет (рус)',
            'level_tg': '7-10 сол (тг)'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activate_language_method(self):
        """Тест метода activate_language_from_header"""
        from a_base.views import ExperienceLevelViewSet
        
        # Создаем фейковый запрос с заголовком
        request = self.factory.get('/', HTTP_ACCEPT_LANGUAGE='tg')
        view = ExperienceLevelViewSet()
        view.request = request
        
        # Вызываем метод
        view.activate_language_from_header(request)
        
        # Проверяем результат
        self.assertEqual(translation.get_language(), 'tg')

    def test_activate_language_default(self):
        """Тест метода activate_language_from_header с заголовком по умолчанию"""
        from a_base.views import ExperienceLevelViewSet
        
        # Создаем запрос без заголовка
        request = self.factory.get('/')
        view = ExperienceLevelViewSet()
        view.request = request
        
        # Вызываем метод
        view.activate_language_from_header(request)
        
        # Проверяем, что используется язык по умолчанию ('ru')
        self.assertEqual(translation.get_language(), 'ru')