from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import translation
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from django.utils import translation

from a_base.models import Specialty
from a_base.serializers import SpecialtySerializer
from a_base.views import SpecialtyViewSet

from django.contrib.auth import get_user_model

User = get_user_model()

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

class SpecialtyAdminAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем администратора
        self.admin = User.objects.create_user(
            phone_number='+992123456789',
            password='testpass123',
            first_name='Admin',
            date_of_birth='1990-01-01',
            is_staff=True,
        )
        # Аутентифицируем клиент как администратор
        self.client.force_authenticate(user=self.admin)
        
        # Тестовая специальность
        self.specialty = Specialty.objects.create(
            name='Терапевт',
            name_ru='Терапевт',
            name_tg='Табиби амрози дарунӣ'
        )
        self.url_list = reverse('specialty-list')
        self.url_detail = reverse('specialty-detail', args=[self.specialty.id])

    def test_admin_can_create_specialty(self):
        """Тест создания специальности администратором"""
        data = {
            'name': 'Невролог',
            'name_ru': 'Невролог',
            'name_tg': 'Асабшинос'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Specialty.objects.count(), 2)
        
        # Получаем свежие данные из БД
        new_specialty = Specialty.objects.get(id=response.data['id'])
        self.assertEqual(new_specialty.name_ru, 'Невролог')
        self.assertEqual(new_specialty.name_tg, 'Асабшинос')

    def test_admin_can_update_specialty(self):
        """Тест обновления специальности администратором"""
        data = {
            'name_ru': 'Обновленный терапевт',
            'name_tg': 'Табиби нав'
        }
        response = self.client.put(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.specialty.refresh_from_db()
        self.assertEqual(self.specialty.name_ru, 'Обновленный терапевт')
        self.assertEqual(self.specialty.name_tg, 'Табиби нав')

    def test_admin_can_partially_update_specialty(self):
        """Тест частичного обновления специальности администратором"""
        data = {
            'name_tg': 'Табиби нав'
        }
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.specialty.refresh_from_db()
        self.assertEqual(self.specialty.name_tg, 'Табиби нав')
        # Проверяем что русское название не изменилось
        self.assertEqual(self.specialty.name_ru, 'Терапевт')

    def test_admin_can_delete_specialty(self):
        """Тест удаления специальности администратором"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Specialty.objects.count(), 0)

    def test_language_specific_updates(self):
        """Тест обновления с учетом языка"""
        # Обновляем только русское название
        data_ru = {'name_ru': 'Кардиолог'}
        response_ru = self.client.patch(self.url_detail, data_ru)
        self.specialty.refresh_from_db()
        self.assertEqual(self.specialty.name_ru, 'Кардиолог')
        self.assertEqual(self.specialty.name_tg, 'Табиби амрози дарунӣ')
        
        # Обновляем только таджикское название
        data_tg = {'name_tg': 'Дилшинос'}
        response_tg = self.client.patch(self.url_detail, data_tg)
        self.specialty.refresh_from_db()
        self.assertEqual(self.specialty.name_ru, 'Кардиолог')
        self.assertEqual(self.specialty.name_tg, 'Дилшинос')

    def test_serializer_output_after_update(self):
        """Тест вывода сериализатора после обновления"""
        # Обновляем данные
        update_data = {
            'name_ru': 'Офтальмолог',
            'name_tg': 'Чашмпизишк'
        }
        self.client.put(self.url_detail, update_data)
        
        # Проверяем вывод на русском
        response_ru = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response_ru.data['name'], 'Офтальмолог')
        
        # Проверяем вывод на таджикском
        response_tg = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response_tg.data['name'], 'Чашмпизишк')


class SpecialtyAdminPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем обычного пользователя (не админа)
        self.user = User.objects.create_user(
            phone_number='+992987654321',
            password='userpass123',
            first_name='User',
            date_of_birth='1995-01-01'
        )
        self.client.force_authenticate(user=self.user)
        
        self.specialty = Specialty.objects.create(
            name_ru='Педиатр',
            name_tg='Педиатр'
        )
        self.url_list = reverse('specialty-list')
        self.url_detail = reverse('specialty-detail', args=[self.specialty.id])

    def test_non_admin_cannot_create(self):
        """Тест что обычный пользователь не может создавать"""
        data = {'name_ru': 'Хирург', 'name_tg': 'Ҷарроҳ'}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_update(self):
        """Тест что обычный пользователь не может обновлять"""
        data = {'name_ru': 'Обновленный'}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_delete(self):
        """Тест что обычный пользователь не может удалять"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)