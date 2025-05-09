from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from core.serializers import CustomUserPrivateSerializer, CustomUserPublicSerializer
from a_base.models import (
    Region, District, Advantage, Subscription,
    ExperienceLevel, Service, ServicePlace, Gender
)

User = get_user_model()

class CustomUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.api_client = APIClient()

        self.gender_male = Gender.objects.create(
            name="Мужской",
            name_ru="Мужской",
            name_tg="Мард"
        )
        self.gender_female = Gender.objects.create(
            name="Женский",
            name_ru="Женский",
            name_tg="Зан"
        )
        # Регионы и районы
        self.region_dushanbe = Region.objects.create(
            code='01',
            name='Душанбе', 
            name_ru="Душанбе", 
            name_tg="Душанбе"
            )
        self.region_sogd = Region.objects.create(
            code='03',
            name='Согдийская область', 
            name_ru="Согдийская область", 
            name_tg="Вилояти Суғд"
            )
        self.district_shokh = District.objects.create(
            name='Шохмансур',
            name_ru="Шохмансур",
            name_tg="Шоҳмансур",
            region=self.region_dushanbe
            )
        self.district_khujand = District.objects.create(
            name='Худжанд', 
            name_ru="Худжанд", 
            name_tg="Хуҷанд",
            region=self.region_sogd
            )
        
        # Преимущества и подписки
        self.advantage1 = Advantage.objects.create(
            name_ru='Поиск врачей', 
            name_tg='Ҷустуҷӯи духтурҳо'
        )
        self.advantage2 = Advantage.objects.create(
            name_ru='Без рекламы', 
            name_tg='Бе реклама'
        )

        self.premium_sub = Subscription.objects.create(
            name_ru='Премиум',
            name_tg='Премиум',
            description_ru='Полный доступ',
            description_tg='Дастрасии пурра',
            price=999.00,
            duration_days=30,
        )
        self.premium_sub.advantages.add(self.advantage1, self.advantage2)

        self.standard_sub = Subscription.objects.create(
            name='Стандартная',
            name_ru='Стандартная',
            name_tg='Стандартӣ',
            price=799,
            description='Стандартная подписка',
            duration_days=30
        )
        self.standard_sub.advantages.add(self.advantage1, self.advantage2)
        
        self.basic_sub = Subscription.objects.create(
            name='Базовая',
            name_ru='Базовая',
            name_tg='Асосӣ',
            price=299,
            description='Базовая подписка',
            duration_days=30
        )
        self.basic_sub.advantages.add(self.advantage1, self.advantage2)

        # Тестовый пользователь с премиальной подпиской
        self.user1 = User.objects.create_user(
            phone_number='+992000000010',
            password='testpass123',
            first_name='Пациент Тестовый',
            last_name='Тестовый Пациент',
            date_of_birth='1990-01-01',
            district=self.district_shokh,
            subscription=self.premium_sub,
        )
        self.user1.activate_subscription()

        # Тестовый пользователь со стандартной подпиской
        self.user2 = User.objects.create_user(
            phone_number='+992000000100',
            password='testpass123',
            first_name='Пациент Тестовый',
            last_name='Тестовый Пациент',
            date_of_birth='1990-01-01',
            district=self.district_khujand,
            subscription=self.standard_sub,
        )
        self.user2.activate_subscription()

        # Администратор
        self.admin_user = User.objects.create_user(
            phone_number='+992000000011',
            password='testpass123',
            first_name='Администратор',
            last_name='Тестовый Администратор',
            date_of_birth='1990-01-01',
            is_staff=True,
            is_superuser=True,
        )

        self.district_list_url = reverse('district-list')
        self.register_url = reverse('register')
        self.token_url = reverse('token')
        self.user_list_url = reverse('user-list')
        self.user1_detail_url = reverse('user-detail', kwargs={"pk": self.user1.id})
        self.user2_detail_url = reverse('user-detail', kwargs={"pk": self.user2.id})

    def test_admin_user(self):
        """Проверка администратора получение всех пользователей"""
        admin_auth_data = {
            'phone_number': '+992000000011',
            'password': 'testpass123'
        }

        response = self.api_client.post(self.token_url, admin_auth_data, format='json')
        access_token = response.data['access']
        response = self.api_client.get(self.user_list_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_districts(self):
        """Любой пользователь может получить список районов"""
        response = self.api_client.get(self.district_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Проверяем, что район Душанбе присутствует в списке"""
        district_ids = [district['id'] for district in response.data]
        self.assertIn(self.region_dushanbe.id, district_ids)

    def test_register_users(self):
        """Любой пользователь может зарегистрироваться"""
        response = self.api_client.get(self.district_list_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователя своего района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пользователь',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_token(self):
        """Пользователь должен иметь возможность авторизироваться после регистрации"""
        response = self.api_client.get(self.district_list_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователя своего района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пользователь',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.token_url, auth_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_own_user_object(self):
        """Пользователь получает только свой профиль пользователя"""
        response = self.api_client.get(self.district_list_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователя своего района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пользователь',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.token_url, auth_data, format='json')

        access_token = response.data['access']
        response = self.api_client.get(self.user_list_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Пользователь')

        """Попытка получить доступ к своему профилю через явную передачю id"""
        user_detail = reverse('user-detail', kwargs={"pk": response.data[0]['id']})
        response = self.api_client.get(user_detail, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Пользователь')

        """Попытка получить доступ к чужому профилю"""
        response = self.api_client.get(self.user1_detail_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """Попытка получить профиль пользователя администратором"""
        admin_auth_data = {
            'phone_number': '+992000000011',
            'password': 'testpass123'
        }

        response = self.api_client.post(self.token_url, admin_auth_data, format='json')
        access_token = response.data['access']

        # Зарегистрированный пользователь
        response = self.api_client.get(user_detail, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.api_client.get(self.user1_detail_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.api_client.get(self.user2_detail_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_data(self):
        """Только владелец профиля пациента и администратор могут вносить изменения в данные профиля"""
        response = self.api_client.get(self.district_list_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователя своего района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пользователь',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.token_url, auth_data, format='json')
        access_token = response.data['access']

        update_data = {
            'last_name': 'Обновленный',
            'inn': '123456789',
            'gender_id': self.gender_male.id,
        }

        response = self.api_client.get(self.user_list_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        user_id = response.data[0]["id"]
        user_detail_url = reverse('user-detail', kwargs={'pk': user_id})

        # Попытка пользователя отредактировать чужой профиль пользователя
        response = self.api_client.patch(self.user1_detail_url, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Попытка пользователя отредактировать профиль без авторизации
        response = self.api_client.patch(user_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.api_client.patch(user_detail_url, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['last_name'], 'Обновленный')
        self.assertEqual(response.data['gender']['id'], self.gender_male.id)