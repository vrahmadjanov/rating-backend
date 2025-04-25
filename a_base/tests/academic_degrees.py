from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import translation

from a_base.models import AcademicDegree
from a_base.serializers import AcademicDegreeSerializer


class AcademicDegreeModelTest(TestCase):
    def setUp(self):
        self.degree_data = {
            'name': 'Доктор медицинских наук',
            'name_ru': 'д.м.н.',
            'name_tg': 'д.и.т.'
        }
        self.degree = AcademicDegree.objects.create(**self.degree_data)

    def test_academic_degree_creation(self):
        """Тестирование создания модели AcademicDegree"""
        self.assertEqual(AcademicDegree.objects.count(), 1)
        self.assertEqual(str(self.degree), self.degree_data['name_ru'])


class AcademicDegreeSerializerTest(TestCase):
    def setUp(self):
        self.degree_data = {
            'name': 'Кандидат медицинских наук',
            'name_ru': 'к.м.н.',
            'name_tg': 'н.и.т.'
        }
        self.degree = AcademicDegree.objects.create(**self.degree_data)
        self.serializer = AcademicDegreeSerializer(instance=self.degree)

    def test_serializer_contains_expected_fields(self):
        """Тестирование полей сериализатора"""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name'})

    def test_name_translation(self):
        """Тестирование перевода имени в сериализаторе"""
        # Тестирование русского языка
        translation.activate('ru')
        serializer_ru = AcademicDegreeSerializer(instance=self.degree)
        self.assertEqual(serializer_ru.data['name'], self.degree_data['name_ru'])

        # Тестирование английского языка
        translation.activate('tg')
        serializer_tg = AcademicDegreeSerializer(instance=self.degree)
        self.assertEqual(serializer_tg.data['name'], self.degree_data['name_tg'])

        # Тестирование fallback языка
        translation.activate('fr')  # Несуществующий язык, должен fallback на 'ru'
        serializer_fr = AcademicDegreeSerializer(instance=self.degree)
        self.assertEqual(serializer_fr.data['name'], self.degree_data['name_ru'])


class AcademicDegreeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.degree_data = {
            'name': 'Доцент',
            'name_ru': 'Доцент',
            'name_tg': 'Дотсент'
        }
        self.degree = AcademicDegree.objects.create(**self.degree_data)
        self.list_url = reverse('academic_degree-list')
        self.detail_url = reverse('academic_degree-detail', kwargs={'pk': self.degree.pk})

    def test_list_academic_degrees(self):
        """Тестирование списка научных степеней"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_academic_degree(self):
        """Тестирование получения одной научной степени"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.degree_data['name'])

    def test_language_header(self):
        """Тестирование заголовка языка"""
        # Русский язык
        response_ru = self.client.get(
            self.detail_url, 
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response_ru.data['name'], self.degree_data['name_ru'])

        # Таджикский язык
        response_tg = self.client.get(
            self.detail_url, 
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response_tg.data['name'], self.degree_data['name_tg'])

        # Неподдерживаемый язык (должен вернуть fallback - русский)
        response_fr = self.client.get(
            self.detail_url, 
            HTTP_ACCEPT_LANGUAGE='fr'
        )
        self.assertEqual(response_fr.data['name'], self.degree_data['name'])

    def test_default_language(self):
        """Тестирование языка по умолчанию (когда нет заголовка)"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data['name'], self.degree_data['name'])

    def test_permissions(self):
        """Тестирование прав доступа"""
        # Чтение разрешено всем
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Создание запрещено не-админам
        response = self.client.post(self.list_url, {'name': 'Новая степень'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обновление запрещено не-админам
        response = self.client.patch(self.detail_url, {'name': 'Обновленная степень'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)