from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from doctors.models import Doctor
from a_base.models import District, Region, Subscription, Advantage

User = get_user_model()

class DoctorViewSetTestCase(APITestCase):
    def setUp(self):
        self.api_client = APIClient()
        # Создаем тестовые регионы и районы
        self.region1 = Region.objects.create(
            code='01',
            name='Регион 1', 
            name_ru="Регион 1 (рус)", 
            name_tg="Регион 1 (tj)"
            )
        self.region2 = Region.objects.create(
            code='02',
            name='Регион 2', 
            name_ru="Регион 1 (рус)", 
            name_tg="Регион 1 (tj)"
            )
        self.district1 = District.objects.create(
            name='Район 1', 
            name_ru="Район 1 (рус)", 
            name_tg="Район 1 (tj)", 
            region=self.region1
            )
        self.district2 = District.objects.create(
            name='Район 2', 
            name_ru="Район 1 (рус)", 
            name_tg="Район 1 (tj)", 
            region=self.region2
            )

        # Создаем подписки
        
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
            price=799.00,
            duration_days=30,
            is_active=True
        )
        self.premium_sub.advantages.add(self.advantage1, self.advantage2)

        self.standard_sub = Subscription.objects.create(
            name='Стандартная',
            name_ru='Стандартная',
            name_tg='Стандартная',
            price=800,
            description='Стандартная подписка',
            duration_days=30
        )
        self.standard_sub.advantages.add(self.advantage1, self.advantage2)
        
        self.basic_sub = Subscription.objects.create(
            name='Базовая',
            name_ru='Базовая',
            name_tg='Базовая',
            price=200,
            description='Базовая подписка',
            duration_days=30
        )
        self.basic_sub.advantages.add(self.advantage1, self.advantage2)

        # Создаем пользователей
        self.admin = User.objects.create_superuser(
            phone_number='+992123456789',
            password='testpass123',
            first_name='Admin',
            date_of_birth='1990-01-01',
        )
        
        self.doctor_user1 = User.objects.create_user(
            phone_number='+992000000000',
            password='testpass123',
            first_name='Доктор',
            date_of_birth='1990-01-01',
            last_name='Иванов',
            district=self.district1,
            subscription=self.premium_sub
        )
        self.doctor_user1.activate_subscription()
        
        self.doctor_user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='Доктор2',
            date_of_birth='1990-01-01',
            last_name='Иванов2',
            district=self.district2,
            subscription=self.standard_sub
        )
        self.doctor_user2.activate_subscription()
        
        self.regular_user = User.objects.create_user(
            phone_number='+992000000002',
            password='testpass123',
            first_name='Пользователь',
            date_of_birth='1990-01-01',
            last_name='Обычный',
            district=self.district1,
            subscription=self.basic_sub
        )
        self.regular_user.activate_subscription()
        
        self.no_sub_user = User.objects.create_user(
            phone_number='+992000000003',
            password='testpass123',
            first_name='Пользователь',
            date_of_birth='1990-01-01',
            last_name='Без подписки',
        )

        # Создаем врачей
        self.doctor1 = Doctor.objects.create(
            user=self.doctor_user1,
            about='Опытный врач из региона 1'
        )
        
        self.doctor2 = Doctor.objects.create(
            user=self.doctor_user2,
            about='Врач из региона 2'
        )

        # URL для тестирования
        self.list_url = reverse('doctor-list')
        self.detail_url = reverse('doctor-detail', args=[self.doctor1.id])

    def test_unauthenticated_access(self):
        """Неаутентифицированные пользователи не имеют доступа"""
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.api_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_access(self):
        """Администраторы имеют полный доступ"""
        self.api_client.force_authenticate(user=self.admin)
        
        # Проверка списка
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Проверка деталей
        response = self.api_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверка редактирования
        update_data = {'about_ru': 'Обновленная информация (ru)', 'about_tg': 'Обновленная информация (tg)'}
        response = self.api_client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor1.refresh_from_db()
        self.assertEqual(self.doctor1.about_ru, 'Обновленная информация (ru)')

    def test_doctor_owner_access(self):
        """Врач может редактировать свой профиль"""
        self.api_client.force_authenticate(user=self.doctor_user1)
        
        # Проверка редактирования
        update_data = {'about_ru': 'Новое описание владельца (ru)', 'about_tg': 'Новое описание владельца (tg)'}
        response = self.api_client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor1.refresh_from_db()
        self.assertEqual(self.doctor1.about, 'Новое описание владельца (ru)')
        
        # Попытка редактировать чужой профиль
        other_doctor_url = f'/api/doctors/{self.doctor2.id}/'
        response = self.api_client.patch(other_doctor_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_premium_subscription_access(self):
        """Пользователи с премиум подпиской видят всех врачей"""
        self.api_client.force_authenticate(user=self.regular_user)
        self.regular_user.subscription = self.premium_sub
        self.regular_user.save()
        
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_standard_subscription_access(self):
        """Пользователи со стандартной подпиской видят врачей своего региона"""
        self.api_client.force_authenticate(user=self.regular_user)
        self.regular_user.subscription = self.standard_sub
        self.regular_user.district = self.district1
        self.regular_user.save()
        
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.doctor1.id)

    def test_basic_subscription_access(self):
        """Пользователи с базовой подпиской видят врачей своего региона"""
        self.api_client.force_authenticate(user=self.regular_user)
        self.regular_user.subscription = self.basic_sub
        self.regular_user.district = self.district1
        self.regular_user.save()
        
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.doctor1.id)

    def test_no_subscription_access(self):
        """Пользователи без подписки не видят врачей"""
        self.api_client.force_authenticate(user=self.no_sub_user)
        
        response = self.api_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_regular_user_read_only(self):
        """Обычные пользователи могут только читать"""
        self.api_client.force_authenticate(user=self.regular_user)
        self.regular_user.subscription = self.premium_sub
        self.regular_user.save()
        
        # Чтение разрешено
        response = self.api_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Редактирование запрещено
        update_data = {'about': 'Попытка изменения'}
        response = self.api_client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)