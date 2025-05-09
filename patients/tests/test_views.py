from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from patients.models import Patient
from doctors.models import Doctor
from a_base.models import (
    Region, District, Advantage, Subscription, Gender
)

User = get_user_model()

class PatientAPIViewTestCase(APITestCase):
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
        self.region1 = Region.objects.create(
            code='01',
            name='Душанбе', 
            name_ru="Душанбе", 
            name_tg="Душанбе"
            )
        self.region2 = Region.objects.create(
            code='03',
            name='Согдийская область', 
            name_ru="Согдийская область", 
            name_tg="Вилояти Суғд"
            )
        self.district1 = District.objects.create(
            name='Шохмансур',
            name_ru="Шохмансур",
            name_tg="Шоҳмансур",
            region=self.region1
            )
        self.district2 = District.objects.create(
            name='Худжанд', 
            name_ru="Худжанд", 
            name_tg="Хуҷанд",
            region=self.region2
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

        # Доктора из разных регионов
        self.doctor_user1 = User.objects.create_user(
            phone_number='+992000000000',
            password='testpass123',
            first_name='Доктор',
            last_name='Душанбинский',
            date_of_birth='1990-01-01',
            district=self.district1,
        )
        self.doctor_dushanbe = Doctor.objects.create(
            user=self.doctor_user1,
            about='Опытный врач из региона Душанбе'
        )
        
        self.doctor_user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='Доктор',
            last_name='Худжандский',
            date_of_birth='1990-01-01',
            district=self.district2,
        )
        self.doctor_khujand = Doctor.objects.create(
            user=self.doctor_user2,
            about='Опытный врач из Согдийского региона'
        )

        # Тестовый пациент с премиальной подпиской
        self.patient_user1 = User.objects.create_user(
            phone_number='+992000000010',
            password='testpass123',
            first_name='Пациент Тестовый',
            last_name='Тестовый Пациент',
            date_of_birth='1990-01-01',
            district=self.district1,
            subscription=self.premium_sub,
        )
        self.patient_user1.activate_subscription()
        self.patient_dushanbe = Patient.objects.create(
            user=self.patient_user1,
        )

        # Тестовый пациент со стандартной подпиской
        self.patient_user2 = User.objects.create_user(
            phone_number='+992000000100',
            password='testpass123',
            first_name='Пациент Тестовый',
            last_name='Тестовый Пациент',
            date_of_birth='1990-01-01',
            district=self.district2,
            subscription=self.standard_sub,
        )
        self.patient_user2.activate_subscription()
        self.patient_khujand = Patient.objects.create(
            user=self.patient_user2,
        )

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

        self.get_districts_url = reverse('district-list')
        self.gender_list_url = reverse('gender-list')
        self.register_url = reverse('register')
        self.get_token_url = reverse('token')
        self.user_list_url = reverse('user-list')
        self.doctor_list = reverse('doctor-list')
        self.patient_list = reverse('patient-list')
        self.patient_detail = reverse('patient-detail', kwargs={'pk': self.patient_dushanbe.id})

    def test_admin_user(self):
        """Проверка администратора на присутствие необходимых полей"""
        admin_auth_data = {
            'phone_number': '+992000000011',
            'password': 'testpass123'
        }

        response = self.api_client.post(self.get_token_url, admin_auth_data, format='json')
        access_token = response.data['access']
        response = self.api_client.get(self.user_list_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_districts(self):
        """Любой пользователь может получить список районов"""
        response = self.api_client.get(self.get_districts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        district_ids = [district['id'] for district in response.data]
        
        # Проверяем, что ID нашего региона есть в списке
        self.assertIn(self.region1.id, district_ids)

    def test_register_patients(self):
        """Любой пользователь может зарегистрироваться"""
        response = self.api_client.get(self.get_districts_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователем района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пациент',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auto_basic_subscription(self):
        """Каждый пользователь при регистрации получает базовую подписку в подарок"""
        response = self.api_client.get(self.get_districts_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователем района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пациент',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        patient = User.objects.get(first_name='Пациент')
        self.assertTrue(patient.has_active_subscription)
        self.assertEqual(patient.subscription, self.basic_sub)

    def test_get_token(self):
        """Пользователь должен иметь возможность авторизироваться после регистрации"""
        response = self.api_client.get(self.get_districts_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователем района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пациент',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.get_token_url, auth_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Пользователь получает врача из своего региона"""
        access_token = response.data['access']
        response = self.api_client.get(self.doctor_list, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['user']['last_name'], self.doctor_dushanbe.user.last_name)

    def test_get_own_user_object(self):
        """Пользователь получает только свой профиль пациента"""
        response = self.api_client.get(self.get_districts_url, HTTP_ACCEPT_LANGUAGE='ru')

        # Иммитация выбора пользователем района проживания
        for district in response.data:
            if district["name"] == "Шохмансур":
                shokh_district_id = district["id"]

        register_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789',
            'first_name': 'Пациент',
            'date_of_birth': '2002-08-08',
            'district': shokh_district_id,
        }
        response = self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.get_token_url, auth_data, format='json')

        access_token = response.data['access']
        response = self.api_client.get(self.patient_list, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['first_name'], 'Пациент')

        """Попытка получить доступ к своему профилю через явную передачю id"""
        patient_detail = reverse('patient-detail', kwargs={"pk": response.data[0]['id']})
        response = self.api_client.get(patient_detail, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'Пациент')

        """Попытка получить доступ к чужому профилю"""
        response = self.api_client.get(self.patient_detail, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """Попытка получить все 3 профиля пациентов администратором"""
        admin_auth_data = {
            'phone_number': '+992000000011',
            'password': 'testpass123'
        }

        response = self.api_client.post(self.get_token_url, admin_auth_data, format='json')
        access_token = response.data['access']
        response = self.api_client.get(self.patient_list, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        """Попытка получить доступ к этому же профилю владельцем"""
        self.api_client.force_authenticate(self.patient_user1)
        response = self.api_client.get(self.patient_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'Пациент Тестовый')

    def test_update_user_data(self):
        """Только владелец профиля пациента и администратор могут вносить изменения в данные профиля пользователя"""
        response = self.api_client.get(self.get_districts_url)

        # Иммитация выбора пользователем района проживания
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

        self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }
        response = self.api_client.post(self.get_token_url, auth_data, format='json')
        access_token = response.data['access']
 
        response = self.api_client.get(self.gender_list_url)

        # Иммитация выбора пользователем гендера
        for gender in response.data:
            if gender["name"] == "Мужской":
                male_gender_id = gender["id"]

        update_data = {
            'last_name': 'Обновленный профиль пользователя',
            'inn': '123456789',
            'gender_id': male_gender_id,
        }

        response = self.api_client.get(self.user_list_url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        user_id = response.data[0]["id"]
        user_detail_url = reverse('user-detail', kwargs={'pk': user_id})

        response = self.api_client.patch(user_detail_url, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['last_name'], 'Обновленный профиль пользователя')
        self.assertEqual(response.data['gender']['id'], self.gender_male.id)
        self.assertEqual(response.data['gender']['name'], self.gender_male.name)

    def test_update_patient_data(self):
        """Только владелец профиля пациента и администратор могут вносить изменения в данные профиля пациента"""
        response = self.api_client.get(self.get_districts_url)

        # Иммитация выбора пользователем района проживания
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

        self.api_client.post(self.register_url, register_data, format='json')

        auth_data = {
            'phone_number': '+992123456789',
            'password': '+992123456789'
        }

        response = self.api_client.post(self.get_token_url, auth_data, format='json')
        access_token = response.data['access']
 
        response = self.api_client.get(self.gender_list_url)

        for gender in response.data:
            if gender["name"] == "Женский":
                female_gender_id = gender["id"]

        response = self.api_client.get(self.patient_list, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_ACCEPT_LANGUAGE='tg')
        patient_id = response.data[0]["id"]
        patient_detail_url = reverse('patient-detail', kwargs={'pk': patient_id})

        update_data = {
            'user': {
                'first_name': 'Пользователь',
                'last_name': 'Обновленный',
            },
            'gender_id': female_gender_id,
            'actual_address': 'Актуальный адрес',
            'registration_address': 'Адрес регистрации',
        }

        # Попытка обновить свой профиль 
        response = self.api_client.patch(patient_detail_url, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['gender']['id'], female_gender_id)

        self.assertEqual(response.data['user']['last_name'], 'Обновленный')
        self.assertEqual(response.data['actual_address'], 'Актуальный адрес')

        # Попытка обновить чужой профиль
        response = self.api_client.patch(self.patient_detail, update_data, HTTP_AUTHORIZATION=f'Bearer {access_token}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Попытка обновить свой профиль без авторизации
        response = self.api_client.patch(patient_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)