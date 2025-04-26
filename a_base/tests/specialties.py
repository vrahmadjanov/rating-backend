from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import translation
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from django.utils import translation

from a_base.models import Specialty
from a_base.serializers import SpecialtySerializer
from a_base.views import SpecialtyViewSet

class SpecialtyModelTest(TestCase):
    def setUp(self):
        self.specialty_data = {
            'name_ru': 'Кардиолог',
            'name_tg': 'Кардиолог'
        }
        self.specialty = Specialty.objects.create(**self.specialty_data)

    def test_specialty_creation(self):
        """Тест создания специальности"""
        self.assertEqual(Specialty.objects.count(), 1)
        self.assertEqual(self.specialty.name_ru, self.specialty_data['name_ru'])
        self.assertEqual(self.specialty.name_tg, self.specialty_data['name_tg'])

    def test_unique_constraint(self):
        """Тест уникальности названия специальности"""
        with self.assertRaises(Exception):
            Specialty.objects.create(name_ru=self.specialty_data['name_ru'])

    def test_verbose_names(self):
        """Тест verbose names"""
        meta = Specialty._meta
        self.assertEqual(meta.verbose_name, 'Специальность')
        self.assertEqual(meta.verbose_name_plural, 'Специальности')

    def test_str_representation(self):
        """Тест строкового представления"""
        translation.activate('ru')
        self.assertEqual(str(self.specialty), self.specialty_data['name_ru'])
        translation.activate('tg')
        self.assertEqual(str(self.specialty), self.specialty_data['name_tg'])


class SpecialtySerializerTest(TestCase):
    def setUp(self):
        self.specialty = Specialty.objects.create(
            name='Терапевт',
            name_ru='Терапевт',
            name_tg='Табиби амрози дарунӣ'
        )
        self.factory = APIRequestFactory()

    def test_serializer_fields(self):
        """Тест полей сериализатора"""
        serializer = SpecialtySerializer(instance=self.specialty)
        self.assertEqual(set(serializer.data.keys()), {'id', 'name'})

    def test_name_translation(self):
        """Тест перевода названия в сериализаторе"""
        request = self.factory.get('/')
        
        # Явно устанавливаем русский язык для запроса
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'ru'
        translation.activate('ru')
        serializer = SpecialtySerializer(instance=self.specialty, context={'request': request})
        self.assertEqual(serializer.data['name'], 'Терапевт')

        # Таджикский язык
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'tg'
        translation.activate('tg')
        serializer = SpecialtySerializer(instance=self.specialty, context={'request': request})
        self.assertEqual(serializer.data['name'], 'Табиби амрози дарунӣ')

        # Fallback на русский для неизвестного языка
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'en'
        translation.activate('en')
        serializer = SpecialtySerializer(instance=self.specialty, context={'request': request})
        self.assertEqual(serializer.data['name'], 'Терапевт')


class SpecialtyViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.specialty1 = Specialty.objects.create(
            name_ru='Хирург',
            name_tg='Ҷарроҳ'
        )
        self.specialty2 = Specialty.objects.create(
            name_ru='Педиатр',
            name_tg='Педиатр'
        )
        self.url_list = reverse('specialty-list')
        self.url_detail = reverse('specialty-detail', args=[self.specialty1.id])

    def test_list_specialties(self):
        """Тест получения списка специальностей"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_language_header(self):
        """Тест обработки заголовка языка"""
        # Русский язык
        response_ru = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response_ru.data['name'], 'Хирург')

        # Таджикский язык
        response_tg = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response_tg.data['name'], 'Ҷарроҳ')

        # Fallback на русский
        response_en = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response_en.data['name'], 'Хирург')

    def test_permissions(self):
        """Тест прав доступа"""
        # POST запрещен для не-админов (ReadOnlyOrAdmin permission)
        response = self.client.post(self.url_list, {
            'name_ru': 'Новая специальность',
            'name_tg': 'Специалияти нав'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SpecialtyAPIIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.specialty = Specialty.objects.create(
            name_ru='Офтальмолог',
            name_tg='Чашмпизишк'
        )
        self.url = reverse('specialty-detail', args=[self.specialty.id])

    def test_full_response_structure(self):
        """Тест полной структуры ответа API"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.specialty.id)
        self.assertEqual(response.data['name'], 'Офтальмолог')

        response_tg = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response_tg.data['name'], 'Чашмпизишк')