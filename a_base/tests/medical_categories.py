from django.test import TestCase
from django.utils.translation import activate
from django.utils import translation
from rest_framework.test import APIRequestFactory
from a_base.models import MedicalCategory
from a_base.serializers import MedicalCategorySerializer

class MedicalCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем фиксированные медицинские категории
        cls.first_category = MedicalCategory.objects.create(
            name="первая",
            name_tg="аввал"  # таджикский перевод для "первая"
        )
        cls.second_category = MedicalCategory.objects.create(
            name="вторая",
            name_tg="дуввум"  # таджикский перевод для "вторая"
        )
        cls.highest_category = MedicalCategory.objects.create(
            name="высшая",
            name_tg="олий"  # таджикский перевод для "высшая"
        )

    def test_only_three_categories_exist(self):
        """Проверяем, что существует ровно 3 категории"""
        self.assertEqual(MedicalCategory.objects.count(), 3)
        categories = list(MedicalCategory.objects.values_list('name_ru', flat=True))
        self.assertListEqual(categories, ['первая', 'вторая', 'высшая'])

    def test_category_names_are_correct(self):
        """Проверяем правильность названий категорий"""
        self.assertEqual(self.first_category.name_ru, "первая")
        self.assertEqual(self.second_category.name_ru, "вторая")
        self.assertEqual(self.highest_category.name_ru, "высшая")

    def test_unique_constraint(self):
        """Проверяем уникальность названий категорий"""
        with self.assertRaises(Exception):
            MedicalCategory.objects.create(name="первая")

    def test_verbose_names(self):
        """Проверяем правильность verbose_name"""
        self.assertEqual(MedicalCategory._meta.verbose_name, "Медицинская категория")
        self.assertEqual(MedicalCategory._meta.verbose_name_plural, "Медицинские категории")

    def test_str_representation(self):
        """Проверяем строковое представление"""
        self.assertEqual(str(self.first_category), "первая")
        self.assertEqual(str(self.highest_category), "высшая")

    def test_russian_translations(self):
        """Проверяем русские названия (основной язык)"""
        activate('ru')
        self.assertEqual(self.first_category.name, "первая")
        self.assertEqual(self.second_category.name, "вторая")
        self.assertEqual(self.highest_category.name, "высшая")

    def test_tajik_translations(self):
        """Проверяем таджикские переводы"""
        activate('tg')
        self.assertEqual(self.first_category.name_tg, "аввал")
        self.assertEqual(self.second_category.name_tg, "дуввум")
        self.assertEqual(self.highest_category.name_tg, "олий")

    def test_translation_fallback(self):
        """Проверяем fallback на русский при отсутствии перевода"""
        activate('en')  # Язык без перевода
        self.assertEqual(self.first_category.name, "первая")
        self.assertEqual(self.second_category.name, "вторая")
        self.assertEqual(self.highest_category.name, "высшая")

class MedicalCategorySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        # Создаем тестовые категории с переводами
        cls.category = MedicalCategory.objects.create(
            name_ru="Первая категория",
            name_tg="Категорияи аввал"
        )

    def setUp(self):
        self.request = self.factory.get('/')
        
    def test_serializer_fields(self):
        """Проверяем наличие всех полей в сериализаторе"""
        serializer = MedicalCategorySerializer(instance=self.category)
        self.assertEqual(set(serializer.data.keys()), {'id', 'name'})

    def test_russian_translation(self):
        """Проверяем вывод на русском языке"""
        translation.activate('ru')
        serializer = MedicalCategorySerializer(instance=self.category, context={'request': self.request})
        self.assertEqual(serializer.data['name'], "Первая категория")

    def test_tajik_translation(self):
        """Проверяем вывод на таджикском языке"""
        translation.activate('tg')
        serializer = MedicalCategorySerializer(instance=self.category, context={'request': self.request})
        self.assertEqual(serializer.data['name'], "Категорияи аввал")

    def test_fallback_to_russian(self):
        """Проверяем fallback на русский при неизвестном языке"""
        translation.activate('en')  # Язык без перевода
        serializer = MedicalCategorySerializer(instance=self.category, context={'request': self.request})
        self.assertEqual(serializer.data['name'], "Первая категория")

    def test_serializer_with_multiple_objects(self):
        """Проверяем работу сериализатора с queryset"""
        MedicalCategory.objects.create(name_ru="Вторая", name_tg="Дуввум")
        queryset = MedicalCategory.objects.all()
        
        translation.activate('ru')
        serializer = MedicalCategorySerializer(queryset, many=True, context={'request': self.request})
        self.assertEqual(len(serializer.data), 2)
        self.assertEqual(serializer.data[0]['name'], "Первая категория")
        self.assertEqual(serializer.data[1]['name'], "Вторая")

from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from django.utils import translation
from rest_framework import status
from a_base.models import MedicalCategory
from a_base.views import MedicalCategoryViewSet

from django.contrib.auth import get_user_model

User = get_user_model()

class MedicalCategoryViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.admin = User.objects.create_superuser(
            phone_number='+992123456789',
            password='testpass123',
            first_name='Admin',
            date_of_birth='1990-01-01',
        )
        cls.user = User.objects.create_user(
            phone_number='+992000000000',
            password='testpass123',
            first_name='TestUser',
            date_of_birth='1990-01-01',
        )
        
        # Создаем медицинские категории с переводами
        cls.category1 = MedicalCategory.objects.create(
            name="Первая категория",
            name_ru="Первая категория",
            name_tg="Категорияи аввал"
        )
        cls.category2 = MedicalCategory.objects.create(
            name="Вторая категория",
            name_ru="Вторая категория",
            name_tg="Категорияи дуввум"
        )

    def setUp(self):
        self.factory = APIRequestFactory()
        self.list_url = reverse('medical_category-list')
        self.detail_url = reverse('medical_category-detail', args=[self.category1.id])

    def test_list_returns_all_categories(self):
        """Проверяем получение списка категорий"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_language_header_works(self):
        """Проверяем работу заголовка Accept-Language"""
        # Проверка русского языка
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.data[0]['name'], "Первая категория")

        # Проверка таджикского языка
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data[0]['name'], "Категорияи аввал")

        # Проверка fallback на русский для неизвестного языка
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response.data[0]['name'], "Первая категория")

    def test_retrieve_works_with_language(self):
        """Проверяем получение одной категории с учетом языка"""
        # Русский язык
        response = self.client.get(
            self.detail_url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.data['name'], "Первая категория")

        # Таджикский язык
        response = self.client.get(
            self.detail_url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data['name'], "Категорияи аввал")

    def test_permissions_for_anonymous_user(self):
        """Проверяем права доступа для анонимного пользователя"""
        # GET разрешены
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST запрещен
        response = self.client.post(self.list_url, {'name_ru': 'Новая'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_regular_user(self):
        """Проверяем права доступа для обычного пользователя"""
        self.client.force_authenticate(self.user)
        
        # GET разрешены
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST запрещен
        response = self.client.post(self.list_url, {'name_ru': 'Новая'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_for_admin(self):
        """Проверяем права доступа для администратора"""
        self.client.force_authenticate(self.admin)
        
        # GET разрешены
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # POST разрешен
        response = self.client.post(
            self.list_url,
            {'name_ru': 'Новая', 'name_tg': 'Нав'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category(self):
        """Проверяем создание новой категории администратором"""
        self.client.force_authenticate(self.admin)
        
        data = {
            'name_ru': 'Высшая категория',
            'name_tg': 'Категорияи олий'
        }
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalCategory.objects.count(), 3)
        self.assertEqual(
            MedicalCategory.objects.last().name_ru,
            'Высшая категория'
        )

    def test_update_category(self):
        """Проверяем обновление категории администратором"""
        self.client.force_authenticate(self.admin)
        
        data = {
            'name_ru': 'Обновленная первая',
            'name_tg': 'Категорияи нав'
        }
        response = self.client.put(self.detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name_ru, 'Обновленная первая')
        self.assertEqual(self.category1.name_tg, 'Категорияи нав')

    def test_delete_category(self):
        """Проверяем удаление категории администратором"""
        self.client.force_authenticate(self.admin)
        
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalCategory.objects.count(), 1)