from django.test import TestCase
from a_base.models import Service, ServicePlace
from django.utils import translation
from rest_framework.test import APIRequestFactory, APITestCase
from a_base.serializers import ServiceSerializer
from django.urls import reverse
from rest_framework import status
from a_base.views import ServiceViewSet
from django.contrib.auth import get_user_model

User = get_user_model()

class ServicePlaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовое место услуги с переводами
        cls.service_place = ServicePlace.objects.create(
            name_ru="На дому",
            name_tg="Дар хона",
        )

    def test_model_creation(self):
        """Тест создания модели с переводами"""
        self.assertEqual(ServicePlace.objects.count(), 1)
        self.assertEqual(self.service_place.name_ru, "На дому")
        self.assertEqual(self.service_place.name_tg, "Дар хона")
        self.assertEqual(self.service_place.name, "На дому")

    def test_unique_name_constraint(self):
        """Тест уникальности названия места проведения услуги"""
        with self.assertRaises(Exception):
            ServicePlace.objects.create(
                name_ru="На дому",
                name_tg="Дар хона"
            )
    
    def test_str_representation(self):
        """Тест строкового представления"""
        translation.activate('ru')
        self.assertEqual(str(self.service_place), "На дому")
        
        translation.activate('tg')
        self.assertEqual(str(self.service_place), "Дар хона")

    def test_translation_fields_created(self):
        """Тест что поля перевода созданы"""
        self.assertTrue(hasattr(self.service_place, 'name_ru'))
        self.assertTrue(hasattr(self.service_place, 'name_tg'))

    def test_russian_translation(self):
        """Тест русской версии"""
        translation.activate('ru')
        self.assertEqual(self.service_place.name, "На дому")

    def test_tajik_translation(self):
        """Тест таджикской версии"""
        translation.activate('tg')
        self.assertEqual(self.service_place.name, "Дар хона")

    def test_fallback_to_russian(self):
        """Тест fallback на русский при неизвестном языке"""
        translation.activate('en')
        self.assertEqual(self.service_place.name, "На дому")

    def test_empty_translation(self):
        """Тест с пустыми переводами"""
        service_place = ServicePlace.objects.create(
            name_ru="Онлайн",
        )
        
        translation.activate('tg')
        self.assertEqual(service_place.name, "Онлайн")  # fallback на ru


class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовую услугу с переводами

        cls.service_place = ServicePlace.objects.create(
            name_ru="На дому",
            name_tg="Дар хона",
        )
                
        cls.service = Service.objects.create(
            service_place=cls.service_place,
            name_ru="Консультация врача",
            name_tg="Машварати пизишк",
            description_ru="Первичная консультация специалиста",
            description_tg="Машварати ибтидоии мутахассис"
        )

    def test_model_creation(self):
        """Тест создания модели с переводами"""
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(self.service.service_place.name_ru, "На дому")
        self.assertEqual(self.service.service_place.name_tg, "Дар хона")
        self.assertEqual(self.service.name_ru, "Консультация врача")
        self.assertEqual(self.service.name_tg, "Машварати пизишк")
        self.assertEqual(self.service.description_ru, "Первичная консультация специалиста")
        self.assertEqual(self.service.description_tg, "Машварати ибтидоии мутахассис")
        

    def test_str_representation(self):
        """Тест строкового представления"""
        translation.activate('ru')
        self.assertEqual(str(self.service), "Консультация врача")
        
        translation.activate('tg')
        self.assertEqual(str(self.service), "Машварати пизишк")

    def test_translation_fields_created(self):
        """Тест что поля перевода созданы"""
        self.assertTrue(hasattr(self.service, 'name_ru'))
        self.assertTrue(hasattr(self.service, 'name_tg'))
        self.assertTrue(hasattr(self.service, 'description_ru'))
        self.assertTrue(hasattr(self.service, 'description_tg'))

    def test_russian_translation(self):
        """Тест русской версии"""
        translation.activate('ru')
        self.assertEqual(self.service.name, "Консультация врача")
        self.assertEqual(self.service.description, "Первичная консультация специалиста")

    def test_tajik_translation(self):
        """Тест таджикской версии"""
        translation.activate('tg')
        self.assertEqual(self.service.name, "Машварати пизишк")
        self.assertEqual(self.service.description, "Машварати ибтидоии мутахассис")

    def test_fallback_to_russian(self):
        """Тест fallback на русский при неизвестном языке"""
        translation.activate('en')
        self.assertEqual(self.service.name, "Консультация врача")
        self.assertEqual(self.service.description, "Первичная консультация специалиста")

    def test_empty_translation(self):
        """Тест с пустыми переводами"""
        service = Service.objects.create(
            service_place=self.service_place,
            name_ru="Анализы",
            description_ru="Лабораторные исследования"
        )
        
        translation.activate('tg')
        self.assertEqual(service.name, "Анализы")  # fallback на ru
        self.assertEqual(service.description, "Лабораторные исследования")


class ServiceSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        # Создаем тестовую услугу с переводами

        cls.service_place = ServicePlace.objects.create(
            name_ru="На дому",
            name_tg="Дар хона"
        )

        cls.service_place2 = ServicePlace.objects.create(
            name_ru="Онлайн",
            name_tg="Онлайн"
        )

        cls.service = Service.objects.create(
            service_place=cls.service_place,
            name_ru="Консультация",
            name_tg="Машварат",
            description_ru="Описание консультации",
            description_tg="Тавсифи машварат"
        )

    def setUp(self):
        self.request = self.factory.get('/')
        
    def test_serializer_fields(self):
        """Проверяем наличие всех полей в сериализаторе"""
        serializer = ServiceSerializer(instance=self.service)
        self.assertEqual(set(serializer.data.keys()), {'id', 'name', 'description', 'service_place', 'price'})

    def test_russian_translation(self):
        """Проверяем вывод на русском языке"""
        translation.activate('ru')
        serializer = ServiceSerializer(instance=self.service, context={'request': self.request})
        self.assertEqual(serializer.data['service_place']["name"], "На дому")
        self.assertEqual(serializer.data['name'], "Консультация")
        self.assertEqual(serializer.data['description'], "Описание консультации")

    def test_tajik_translation(self):
        """Проверяем вывод на таджикском языке"""
        translation.activate('tg')
        serializer = ServiceSerializer(instance=self.service, context={'request': self.request})
        self.assertEqual(serializer.data['service_place']["name"], "Дар хона")
        self.assertEqual(serializer.data['name'], "Машварат")
        self.assertEqual(serializer.data['description'], "Тавсифи машварат")

    def test_fallback_to_russian(self):
        """Проверяем fallback на русский при неизвестном языке"""
        translation.activate('en')
        serializer = ServiceSerializer(instance=self.service, context={'request': self.request})
        self.assertEqual(serializer.data['service_place']["name"], "На дому")
        self.assertEqual(serializer.data['name'], "Консультация")
        self.assertEqual(serializer.data['description'], "Описание консультации")

    def test_create_service(self):
        """Тест создания услуги через сериализатор"""
        data = {
            'service_place_id': self.service_place2.id,
            'name_ru': 'Анализы',
            'name_tg': 'Таҳлилҳо',
            'description_ru': 'Лабораторные анализы',
            'description_tg': 'Таҳлилҳои лабораторӣ',
            'price': 1000.00
        }
        serializer = ServiceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        service = serializer.save()
        self.assertEqual(service.service_place.name_ru, 'Онлайн')
        self.assertEqual(service.service_place.name_tg, 'Онлайн')
        self.assertEqual(service.name_ru, 'Анализы')
        self.assertEqual(service.name_tg, 'Таҳлилҳо')
        self.assertEqual(service.description_ru, 'Лабораторные анализы')
        self.assertEqual(service.description_tg, 'Таҳлилҳои лабораторӣ')

    def test_create_service_with_partial_translations(self):
        """Тест создания с частичными переводами"""
        data = {
            'service_place_id': self.service_place.id,
            'name_ru': 'УЗИ',
            'description_ru': 'Ультразвуковое исследование',
            'price': '800.00'
        }
        serializer = ServiceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        service = serializer.save()
        self.assertEqual(service.service_place.name_ru, 'На дому')
        self.assertEqual(service.service_place.name_tg, 'Дар хона')
        self.assertEqual(service.name_ru, 'УЗИ')
        self.assertEqual(service.name_tg, 'УЗИ')  # Должен взять из ru
        self.assertEqual(service.description_ru, 'Ультразвуковое исследование')
        self.assertEqual(service.description_tg, 'Ультразвуковое исследование')

    def test_update_service(self):
        """Тест обновления услуги"""
        data = {
            'name_tg': 'Нав Машварат',
            'description_ru': 'Новое описание'
        }
        serializer = ServiceSerializer(instance=self.service, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        service = serializer.save()
        self.assertEqual(service.name_ru, 'Консультация')  # Не изменилось
        self.assertEqual(service.name_tg, 'Нав Машварат')  # Обновилось
        self.assertEqual(service.description_ru, 'Новое описание')  # Обновилось
        self.assertEqual(service.description_tg, 'Тавсифи машварат')  # Не изменилось

    def test_serializer_without_request(self):
        """Тест работы сериализатора без request в контексте"""
        translation.activate('ru')
        serializer = ServiceSerializer(instance=self.service)
        self.assertEqual(serializer.data['name'], "Консультация")
        
        translation.activate('tg')
        serializer = ServiceSerializer(instance=self.service)
        self.assertEqual(serializer.data['name'], "Машварат")


class ServiceViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
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

        cls.service_place1 = ServicePlace.objects.create(
            name_ru="На дому",
            name_tg="Дар хона"
        )

        cls.service_place2 = ServicePlace.objects.create(
            name_ru="Онлайн",
            name_tg="Онлайн"
        )
        
        # Создаем тестовые услуги
        cls.service1 = Service.objects.create(
            service_place=cls.service_place1,
            name_ru="Консультация врача",
            name_tg="Машварати пизишк",
            description_ru="Первичная консультация",
            description_tg="Машварати ибтидои",
            price="800.00"
        )
        cls.service2 = Service.objects.create(
            service_place=cls.service_place2,
            name_ru="Анализы крови",
            name_tg="Таҳлили хун",
            description_ru="Лабораторные исследования",
            description_tg="Таҳқиқоти лабораторӣ",
            price="1800.00"
        )

    def setUp(self):
        self.list_url = reverse('service-list')
        self.detail_url = reverse('service-detail', args=[self.service1.id])

    # Тесты списка
    def test_list_services(self):
        """Получение списка услуг"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_language_ru(self):
        """Проверка русского языка в списке"""
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.data[0]['service_place']['name'], "На дому")
        self.assertEqual(response.data[0]['name'], "Консультация врача")
        self.assertEqual(response.data[0]['description'], "Первичная консультация")

    def test_list_language_tg(self):
        """Проверка таджикского языка в списке"""
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data[0]['service_place']['name'], "Дар хона")
        self.assertEqual(response.data[0]['name'], "Машварати пизишк")
        self.assertEqual(response.data[0]['description'], "Машварати ибтидои")

    # Тесты детального просмотра
    def test_retrieve_service(self):
        """Получение одной услуги"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_language_ru(self):
        """Проверка русского языка в детальном просмотре"""
        response = self.client.get(
            self.detail_url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.data['service_place']['name'], "На дому")
        self.assertEqual(response.data['name'], "Консультация врача")

    def test_retrieve_language_tg(self):
        """Проверка таджикского языка в детальном просмотре"""
        response = self.client.get(
            self.detail_url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data['service_place']['name'], "Дар хона")
        self.assertEqual(response.data['name'], "Машварати пизишк")

    # Тесты создания
    def test_create_service_admin(self):
        """Создание услуги администратором"""
        self.client.force_authenticate(user=self.admin)
        
        data = {
            'service_place_id': self.service_place1.id,
            'name_ru': 'УЗИ',
            'name_tg': 'Сонография',
            'description_ru': 'Ультразвуковое исследование',
            'description_tg': 'Таҳқиқи ултрасадо',
            'price': '1200.00',
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 3)
        self.assertEqual(response.data['name'], 'УЗИ')  # Проверяем язык из заголовка

    def test_create_service_user(self):
        """Попытка создания услуги обычным пользователем"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            self.list_url,
            {'service_place_id': self.service_place1.id, 'name_ru': 'Тест', 'description_ru': 'Тест', 'price': '890.00'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Тесты обновления
    def test_update_service_admin(self):
        """Обновление услуги администратором"""
        self.client.force_authenticate(user=self.admin)
        
        data = {
            'name_tg': 'Нав Машварат',
            'description_ru': 'Новое описание'
        }
        
        response = self.client.patch(
            self.detail_url,
            data,
            format='json',
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service1.refresh_from_db()
        self.assertEqual(self.service1.name_tg, 'Нав Машварат')
        self.assertEqual(self.service1.description_ru, 'Новое описание')
        # Проверяем что ответ на таджикском
        self.assertEqual(response.data['name'], 'Нав Машварат')

    # Тесты удаления
    def test_delete_service_admin(self):
        """Удаление услуги администратором"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 1)

    # Тесты языка
    def test_activate_language_header(self):
        """Тест активации языка из заголовка"""
        view = ServiceViewSet()
        request = self.factory.get('/')
        
        # Проверяем установку языка из заголовка
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'tg'
        view.activate_language_from_header(request)
        self.assertEqual(translation.get_language(), 'tg')
        
        # Проверяем fallback при отсутствии заголовка
        del request.META['HTTP_ACCEPT_LANGUAGE']
        view.activate_language_from_header(request)
        self.assertEqual(translation.get_language(), 'ru')

    def test_invalid_language_header(self):
        """Тест с некорректным языком в заголовке"""
        response = self.client.get(
            self.list_url,
            HTTP_ACCEPT_LANGUAGE='invalid'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должен fallback на русский
        self.assertEqual(response.data[0]['name'], "Консультация врача")