from django.test import TestCase
from django.utils.translation import activate
from django.utils import translation
from django.urls import reverse
from a_base.models import Advantage, Subscription
from rest_framework.test import APIClient, APIRequestFactory
from a_base.serializers import SubscriptionSerializer

class AdvantageModelTest(TestCase):
    def setUp(self):
        self.advantage_data = {
            'name_ru': 'Базовый доступ',
            'name_tg': 'Дастрасии асосӣ',
            'description_ru': 'Доступ к базовым функциям',
            'description_tg': 'Дастрасӣ ба функсияҳои асосӣ'
        }
        self.advantage = Advantage.objects.create(**self.advantage_data)

    def test_advantage_creation(self):
        """Тест создания Advantage"""
        self.assertEqual(Advantage.objects.count(), 1)
        self.assertEqual(self.advantage.name_ru, self.advantage_data['name_ru'])
        self.assertEqual(self.advantage.name_tg, self.advantage_data['name_tg'])

    def test_advantage_str_representation(self):
        """Тест строкового представления"""
        activate('ru')
        self.assertEqual(str(self.advantage), self.advantage_data['name_ru'])
        
        activate('tg')
        self.assertEqual(str(self.advantage), self.advantage_data['name_tg'])

    def test_translation_fallback(self):
        """Тест fallback перевода"""
        activate('en')
        self.assertEqual(str(self.advantage), self.advantage_data['name_ru'])


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.advantage1 = Advantage.objects.create(
            name_ru='Поиск врачей', 
            name_tg='Ҷустуҷӯи духтурҳо'
        )
        self.advantage2 = Advantage.objects.create(
            name_ru='Без рекламы', 
            name_tg='Бе реклама'
        )
        
        self.subscription_data = {
            'name_ru': 'Премиум',
            'name_tg': 'Премиум',
            'description_ru': 'Полный доступ',
            'description_tg': 'Дастрасии пурра',
            'price': 799,
            'duration_days': 30,
            'is_active': True
        }
        self.subscription = Subscription.objects.create(**self.subscription_data)
        self.subscription.advantages.add(self.advantage1, self.advantage2)

    def test_subscription_creation(self):
        """Тест создания Subscription"""
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(self.subscription.price, self.subscription_data['price'])
        self.assertEqual(self.subscription.advantages.count(), 2)

    def test_subscription_str_representation(self):
        """Тест строкового представления"""
        activate('ru')
        self.assertEqual(str(self.subscription), self.subscription_data['name_ru'])
        
        activate('tg')
        self.assertEqual(str(self.subscription), self.subscription_data['name_tg'])

    def test_get_advantages_list(self):
        """Тест метода get_advantages_list"""
        activate('ru')
        advantages = self.subscription.get_advantages_list()
        self.assertIn(self.advantage1.name_ru, advantages)
        
        activate('tg')
        advantages = self.subscription.get_advantages_list()
        self.assertIn(self.advantage1.name_tg, advantages)

    def test_price_display(self):
        """Тест отображения цены"""
        self.assertEqual(f"{self.subscription.price} TJS", "799 TJS")

    def test_verbose_names(self):
        """Тест verbose_names"""
        meta = Subscription._meta
        self.assertEqual(meta.verbose_name, 'Подписка')
        self.assertEqual(meta.verbose_name_plural, 'Подписки')

    def test_is_active_default(self):
        """Тест default значения is_active"""
        new_sub = Subscription.objects.create(
            name_ru='Тест',
            name_tg='Тест',
            price=100,
            duration_days=7
        )
        self.assertTrue(new_sub.is_active)


class SubscriptionAdvantageRelationshipTest(TestCase):
    def setUp(self):
        self.advantage = Advantage.objects.create(
            name_ru='Тест', 
            name_tg='Тест'
        )
        self.subscription = Subscription.objects.create(
            name_ru='Тест подписка',
            name_tg='Тест подписка',
            price=100,
            duration_days=7
        )

    def test_adding_advantages(self):
        """Тест добавления преимуществ к подписке"""
        self.subscription.advantages.add(self.advantage)
        self.assertEqual(self.subscription.advantages.count(), 1)
        self.assertEqual(self.advantage.subscriptions.count(), 1)

    def test_removing_advantages(self):
        """Тест удаления преимуществ"""
        self.subscription.advantages.add(self.advantage)
        self.subscription.advantages.remove(self.advantage)
        self.assertEqual(self.subscription.advantages.count(), 0)

    def test_clear_advantages(self):
        """Тест очистки преимуществ"""
        self.subscription.advantages.add(self.advantage)
        self.subscription.advantages.clear()
        self.assertEqual(self.subscription.advantages.count(), 0)


class ModelTranslationTest(TestCase):
    def test_translated_fields(self):
        """Тест наличия переведенных полей в моделях"""
        self.assertTrue(hasattr(Advantage, 'name_ru'))
        self.assertTrue(hasattr(Advantage, 'name_tg'))
        self.assertTrue(hasattr(Subscription, 'description_ru'))
        self.assertTrue(hasattr(Subscription, 'description_tg'))


class SubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.advantage = Advantage.objects.create(
            name_ru='Преимущество',
            name_tg='Афзалият'
        )
        self.subscription = Subscription.objects.create(
            name_ru='Стандарт',
            name_tg='Стандартӣ',
            description_ru='Стандартная подписка',
            description_tg='Обунаи стандартӣ',
            price=299,
            duration_days=30,
            is_active=True
        )
        self.subscription.advantages.add(self.advantage)
        self.factory = APIRequestFactory()

    def test_serializer_fields(self):
        """Тест полей сериализатора Subscription"""
        serializer = SubscriptionSerializer(instance=self.subscription)
        self.assertEqual(
            set(serializer.data.keys()),
            {'id', 'name', 'description', 'price', 'duration_days', 'advantages'}
        )

    def test_advantages_in_serializer(self):
        """Тест вложенных преимуществ в сериализаторе"""
        request = self.factory.get('/')
        
        # Явно устанавливаем русский язык для запроса
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'ru'
        translation.activate('ru')
        
        serializer = SubscriptionSerializer(
            instance=self.subscription,
            context={'request': request}
        )
        self.assertEqual(len(serializer.data['advantages']), 1)
        self.assertEqual(serializer.data['advantages'][0]['name'], 'Преимущество')
        
        # Дополнительно проверяем таджикский перевод
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'tg'
        translation.activate('tg')
        serializer = SubscriptionSerializer(
            instance=self.subscription,
            context={'request': request}
        )
        self.assertEqual(serializer.data['advantages'][0]['name'], 'Афзалият')


class SubscriptionViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.active_sub = Subscription.objects.create(
            name_ru='Активная',
            name_tg='Фаъол',
            price=100,
            duration_days=7,
            is_active=True
        )
        self.inactive_sub = Subscription.objects.create(
            name_ru='Неактивная',
            name_tg='Ғайрифаъол',
            price=200,
            duration_days=14,
            is_active=False
        )
        self.url_list = reverse('subscription-list')
        self.url_detail = reverse('subscription-detail', args=[self.active_sub.id])

    def test_list_active_only(self):
        """Тест получения только активных подписок"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.active_sub.id)

    def test_language_header(self):
        """Тест обработки заголовка языка"""
        # Русский язык
        response_ru = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response_ru.data['name'], 'Активная')

        # Таджикский язык
        response_tg = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response_tg.data['name'], 'Фаъол')

        # Fallback на русский
        response_en = self.client.get(
            self.url_detail,
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response_en.data['name'], 'Активная')

    def test_retrieve_inactive(self):
        """Тест получения неактивной подписки (должен 404)"""
        url = reverse('subscription-detail', args=[self.inactive_sub.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_permissions(self):
        """Тест прав доступа"""
        # POST запрещен для не-админов (ReadOnlyOrAdmin permission)
        response = self.client.post(self.url_list, {
            'name_ru': 'Новая',
            'price': 500,
            'duration_days': 30
        })
        self.assertEqual(response.status_code, 401)


class SubscriptionAPIIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.advantage = Advantage.objects.create(
            name_ru='Онлайн консультации',
            name_tg='Машваратҳои онлайн'
        )
        self.subscription = Subscription.objects.create(
            name_ru='Премиум',
            name_tg='Премиум',
            description_ru='Лучшая подписка',
            description_tg='Беҳтарин обуна',
            price=999,
            duration_days=30,
            is_active=True
        )
        self.subscription.advantages.add(self.advantage)
        self.url = reverse('subscription-detail', args=[self.subscription.id])

    def test_full_response_structure(self):
        """Тест полной структуры ответа API"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='ru'
        )
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['name'], 'Премиум')
        self.assertEqual(data['description'], 'Лучшая подписка')
        self.assertEqual(data['price'], '999.00')
        self.assertEqual(data['duration_days'], 30)
        self.assertEqual(len(data['advantages']), 1)
        self.assertEqual(data['advantages'][0]['name'], 'Онлайн консультации')

    def test_advantages_translation_in_response(self):
        """Тест перевода преимуществ в ответе API"""
        response = self.client.get(
            self.url,
            HTTP_ACCEPT_LANGUAGE='tg'
        )
        self.assertEqual(response.data['advantages'][0]['name'], 'Машваратҳои онлайн')