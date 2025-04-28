from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status

from clinics.models import ClinicType, Clinic
from a_base.models import District, Region, Subscription
from clinics.serializers import ClinicSerializer, ClinicTypeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ClinicTypeModelTest(TestCase):
    def test_clinic_type_creation(self):
        """Тестирование создания типа клиники"""
        clinic_type = ClinicType.objects.create(name="Больница", name_ru="Больница", name_tg="Беморхона")
        self.assertEqual(clinic_type.name, "Больница")
        self.assertEqual(clinic_type.name_ru, "Больница")
        self.assertEqual(clinic_type.name_tg, "Беморхона")
        self.assertEqual(str(clinic_type), "Больница")
        
    def test_unique_name_constraint(self):
        """Тест уникальности названия типа клиники"""
        ClinicType.objects.create(name="Поликлиника")
        with self.assertRaises(Exception):
            ClinicType.objects.create(name="Поликлиника")


class ClinicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = Region.objects.create(name="Область А", name_ru="Область А", name_tg="Ноҳияи А")
        cls.district = District.objects.create(region=cls.region, name="Район А", name_ru="Район А", name_tg="Нохияи А")
        cls.clinic_type = ClinicType.objects.create(name="Госпиталь", name_ru="Госпиталь", name_tg="Госпитал")

    def test_clinic_creation(self):
        """Тестирование создания клиники"""
        clinic = Clinic.objects.create(
            name="Городская больница",
            name_ru="Городская больница",
            name_tg="Беморхонаи шаҳрӣ",
            clinic_type=self.clinic_type,
            address="ул. Центральная 1",
            address_ru="ул. Центральная 1",
            address_tg="кӯчаи Марказӣ 1",
            district=self.district,
            phone_number="+992123456789"
        )
        self.assertEqual(clinic.name, "Городская больница")
        self.assertEqual(clinic.name_ru, "Городская больница")
        self.assertEqual(clinic.name_tg, "Беморхонаи шаҳрӣ")
        self.assertEqual(clinic.clinic_type, self.clinic_type)
        self.assertEqual(clinic.district, self.district)
        
    def test_phone_number_validation(self):
        """Тест валидации номера телефона"""
        with self.assertRaises(ValidationError):
            clinic = Clinic(
                name="Тестовая клиника",
                clinic_type=self.clinic_type,
                address="ул. Тестовая",
                district=self.district,
                phone_number="123456"  # неверный формат
            )
            clinic.full_clean()


class ClinicTypeSerializerTest(TestCase):
    def setUp(self):
        self.clinic_type_data = {
            'name': 'Больница',
            'name_ru': 'Больница',
            'name_tg': 'Беморхона'
        }
        self.clinic_type = ClinicType.objects.create(**self.clinic_type_data)

    @override_settings(LANGUAGE_CODE='ru')
    def test_serializer_with_ru_language(self):
        """Тест сериализатора с русским языком"""
        serializer = ClinicTypeSerializer(self.clinic_type)
        self.assertEqual(serializer.data['name'], 'Больница')

    @override_settings(LANGUAGE_CODE='tg')
    def test_serializer_with_tg_language(self):
        """Тест сериализатора с таджикским языком"""
        serializer = ClinicTypeSerializer(self.clinic_type)
        self.assertEqual(serializer.data['name'], 'Беморхона')

    @override_settings(LANGUAGE_CODE='en')
    def test_serializer_with_fallback_language(self):
        """Тест сериализатора с fallback языком (когда перевод отсутствует)"""
        serializer = ClinicTypeSerializer(self.clinic_type)
        self.assertEqual(serializer.data['name'], 'Больница')  # Должен вернуть русскую версию как fallback


class ClinicSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = Region.objects.create(name="Область А", name_ru="Область А", name_tg="Ноҳияи А")
        cls.district = District.objects.create(region=cls.region, name="Район А", name_ru="Район А", name_tg="Нохияи А")
        cls.clinic_type = ClinicType.objects.create(name="Госпиталь", name_ru="Госпиталь", name_tg="Госпитал")
        
        cls.clinic_data = {
            'name': 'Городская больница',
            'name_ru': 'Городская больница',
            'name_tg': 'Беморхонаи шаҳрӣ',
            'clinic_type': cls.clinic_type,
            'address': 'ул. Центральная 1',
            'address_ru': 'ул. Центральная 1',
            'address_tg': 'кӯчаи Марказӣ 1',
            'district': cls.district,
            'phone_number': '+992123456789'
        }
        cls.clinic = Clinic.objects.create(**cls.clinic_data)

    @override_settings(LANGUAGE_CODE='ru')
    def test_serializer_with_ru_language(self):
        """Тест сериализатора клиники с русским языком"""
        serializer = ClinicSerializer(self.clinic)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Городская больница')
        self.assertEqual(data['address'], 'ул. Центральная 1')
        self.assertEqual(data['clinic_type']['name'], 'Госпиталь')
        self.assertEqual(data['district']['name'], 'Район А')

    @override_settings(LANGUAGE_CODE='tg')
    def test_serializer_with_tg_language(self):
        """Тест сериализатора клиники с таджикским языком"""
        serializer = ClinicSerializer(self.clinic)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Беморхонаи шаҳрӣ')
        self.assertEqual(data['address'], 'кӯчаи Марказӣ 1')
        self.assertEqual(data['clinic_type']['name'], 'Госпитал')
        self.assertEqual(data['district']['name'], 'Нохияи А')

    @override_settings(LANGUAGE_CODE='en')
    def test_serializer_with_fallback_language(self):
        """Тест сериализатора клиники с fallback языком"""
        serializer = ClinicSerializer(self.clinic)
        data = serializer.data
        
        # Должен вернуть русскую версию как fallback
        self.assertEqual(data['name'], 'Городская больница')
        self.assertEqual(data['address'], 'ул. Центральная 1')
        self.assertEqual(data['clinic_type']['name'], 'Госпиталь')
        self.assertEqual(data['district']['name'], 'Район А')


class ClinicAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.region = Region.objects.create(name="Область А", name_ru="Область А", name_tg="Ноҳияи А")
        cls.district = District.objects.create(region=cls.region, name="Район А", name_ru="Район А", name_tg="Нохияи А")
        cls.clinic_type = ClinicType.objects.create(name="Госпиталь", name_ru="Госпиталь", name_tg="Госпитал")
        
        # Создаем тестовую клинику
        cls.clinic = Clinic.objects.create(
            name="Городская больница",
            name_ru="Городская больница",
            name_tg="Беморхонаи шаҳрӣ",
            clinic_type=cls.clinic_type,
            address="ул. Центральная 1",
            address_ru="ул. Центральная 1",
            address_tg="кӯчаи Марказӣ 1",
            district=cls.district,
            phone_number="+992123456789"
        )

        cls.admin = User.objects.create_user(
            phone_number='+992000000000',
            first_name="admin",
            date_of_birth="2002-08-08",
            password='admin',
            email='admin@example.com',
            is_staff=True
        )
        
        # Создаем тестового пользователя с подпиской
        cls.user = User.objects.create_user(
            phone_number='+992123456789',
            first_name="TestUser",
            date_of_birth="2002-08-08",
            password='testpass123',
            email='test@example.com',
            district=cls.district
        )
        cls.user.subscription = Subscription.objects.create(
            name="Премиум",
            price=1000,
            duration_days=30,
            is_active=True
        )
        cls.user.activate_subscription()
        cls.user.save()

    @override_settings(LANGUAGE_CODE='ru')
    def test_clinic_list_view_ru(self):
        """Тест просмотра множества клиник на русском языке для админа"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f'/api/clinics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(LANGUAGE_CODE='ru')
    def test_clinic_list_view_ru(self):
        """Тест просмотра множества клиник на русском языке"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/clinics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clinic_detail_view_ru(self):
        """Тест детального просмотра клиники на русском языке"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/clinics/{self.clinic.id}/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Городская больница')
        self.assertEqual(response.data['address'], 'ул. Центральная 1')
        self.assertEqual(response.data['clinic_type']['name'], 'Госпиталь')

    def test_clinic_detail_view_tg(self):
        """Тест детального просмотра клиники на таджикском языке"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/clinics/{self.clinic.id}/', HTTP_ACCEPT_LANGUAGE='tg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Беморхонаи шаҳрӣ')
        self.assertEqual(response.data['address'], 'кӯчаи Марказӣ 1')
        self.assertEqual(response.data['clinic_type']['name'], 'Госпитал')

    def test_access_without_subscription(self):
        """Тест доступа без подписки"""
        user_no_sub = User.objects.create_user(
            phone_number='+992123456788',
            first_name="TestUser",
            date_of_birth="2002-08-08",
            password='nopass',
            email='testnopass@example.com'
        )
        self.client.force_authenticate(user=user_no_sub)
        response = self.client.get(f'/api/clinics/{self.clinic.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)