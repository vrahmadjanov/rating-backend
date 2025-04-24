from django.test import TestCase
from modeltranslation.utils import build_localized_fieldname
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from a_base.models import Region, District
from a_base.serializers import RegionSerializer
from django.contrib.auth import get_user_model
from django.utils import translation

User = get_user_model()

class ModelTranslationTest(TestCase):
    def test_translation_fields_created(self):
        """Тест создания полей перевода"""
        for model in [Region, District]:
            for lang in ['ru', 'tg']:
                field_name = build_localized_fieldname('name', lang)
                self.assertTrue(hasattr(model(), field_name))

class RegionModelTest(TestCase):
    def setUp(self):
        self.region_data = {
            'code': '01',
            'name_ru': 'Душанбе',
            'name_tg': 'Душанбе'
        }
        self.region = Region.objects.create(**self.region_data)

    def test_region_creation(self):
        """Тест создания региона с переводами"""
        self.assertEqual(self.region.code, '01')
        self.assertEqual(self.region.name_ru, 'Душанбе')
        self.assertEqual(self.region.name_tg, 'Душанбе')
        self.assertEqual(str(self.region), f'Душанбе ({self.region.id})')

    def test_region_default_language(self):
        """Тест получения значения по умолчанию"""
        translation.activate('ru')
        self.assertEqual(self.region.name, 'Душанбе')
        translation.activate('tg')
        self.assertEqual(self.region.name, 'Душанбе')

class DistrictModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(
            code='01',
            name_ru='Душанбе',
            name_tg='Душанбе'
        )
        self.district = District.objects.create(
            code='01',
            name_ru='Центральный район',
            name_tg='Ноҳияи марказӣ',
            region=self.region
        )

    def test_district_translations(self):
        """Тест языковых версий названия района"""
        self.assertEqual(self.district.name_ru, 'Центральный район')
        self.assertEqual(self.district.name_tg, 'Ноҳияи марказӣ')

class RegionAPITest(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            code='01',
            name_ru= 'Душанбе',
            name_tg= 'Душанбе'
        )
        self.url_list = reverse('region-list')
        self.url_detail = reverse('region-detail', kwargs={'pk': self.region.id})

    def test_get_region_list(self):
        """Тест получения списка регионов"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['code'], '01')
        self.assertEqual(response.data[0]['name'], 'Душанбе')

    def test_language_support(self):
        """Тест работы с разными языками"""
        # Создаем запрос с явным указанием языка
        factory = APIRequestFactory()
        request = factory.get(self.url_list, HTTP_ACCEPT_LANGUAGE='tg')
        
        # Тестируем сериализатор напрямую
        serializer = RegionSerializer(
            instance=[self.region], 
            many=True, 
            context={'request': request}
        )

    def test_get_region_detail(self):
        """Тест получения деталей региона"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], '01')


class DistrictAPITest(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(code='01', name='Душанбе')
        self.district = District.objects.create(
            code='01',
            name_ru='Центральный район',
            name_tg='Ноҳияи марказӣ',
            region=self.region
        )
        self.url_list = reverse('district-list')
        self.url_detail = reverse('district-detail', kwargs={'pk': self.district.id})

    def test_get_district_list(self):
        """Тест получения списка районов"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_district_detail(self):
        """Тест получения деталей района"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['code'], '01')
        self.assertEqual(response.data['name'], 'Центральный район')
        self.assertEqual(response.data['region']['code'], '01')

class LanguageAPITest(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            code='01',
            name_ru='Душанбе',
            name_tg='Душанбе',
        )
        self.url = reverse('region-detail', kwargs={'pk': self.region.id})

    def test_russian_language_response(self):
        """Тест ответа на русском языке"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.data['name'], 'Душанбе')

    def test_tajik_language_response(self):
        """Тест ответа на таджикском языке"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data['name'], 'Душанбе')

    def test_fallback_language(self):
        """Тест резервного языка при отсутствии перевода"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='fr'
        )
        self.assertEqual(response.data['name'], 'Душанбе')
        
class RegionPermissionsTest(APITestCase):
    def setUp(self):
        self.region = Region.objects.create(
            code='01',
            name_ru='Душанбе',
            name_tg='Душанбе'
        )
        self.admin = User.objects.create_user(
            first_name='AdminTestUser',
            date_of_birth='2002-08-08',
            phone_number='+992123456789',
            password='adminpass',
            is_staff=True
        )
        self.user = User.objects.create_user(
            first_name='TestUser',
            date_of_birth='2002-08-08',
            phone_number='+992000000000',
            password='userpass'
        )
        self.url = reverse('region-list')
        self.detail_url = reverse('region-detail', kwargs={'pk': self.region.id})

    def test_anonymous_user_can_read(self):
        """Анонимный пользователь может читать"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_write(self):
        """Анонимный пользователь не может изменять"""
        data = {'code': '02', 'name_ru': 'Согд', 'name_tg': 'Суғд'}
        
        # POST запрос
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # PUT запрос
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # DELETE запрос
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_write(self):
        """Обычный пользователь не может изменять"""
        self.client.force_authenticate(user=self.user)
        data = {'code': '02', 'name_ru': 'Согд', 'name_tg': 'Суғд'}
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
