from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from django.utils import translation
from core.models import CustomUser
from a_base.models import Region, District, Subscription, Gender, Advantage

class CustomUserSerializerTests(APITestCase):
    def setUp(self):
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
        
        self.gender_male = Gender.objects.create(name="Мужской", name_ru="Мужской", name_tg="Мард")
        self.gender_female = Gender.objects.create(name="Женский", name_ru="Женский", name_tg="Зан")

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

        self.group = Group.objects.create(name="Пациент")
        
        self.user_data = {
            "phone_number": "+992123456789",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": self.gender_male.id,
            "district": self.district1.id,
            "email": "john.doe@example.com",
            "inn": "123456789",
        }
        
        self.user = CustomUser.objects.create(
            phone_number="+992987654321",
            first_name="Jane",
            last_name="Doe",
            date_of_birth="1990-01-01",
            gender=self.gender_female,
            district=self.district2
        )
        self.user.groups.add(self.group)

    def test_user_serialization(self):
        from core.serializers import CustomUserSerializer
        
        serializer = CustomUserSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(data['phone_number'], self.user.phone_number)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['gender']['id'], self.gender_female.id)
        self.assertEqual(data['gender']['name'], self.gender_female.name_ru)
        self.assertEqual(data['district']['id'], self.district2.id)
        self.assertEqual(data['district']['name'], self.district2.name_ru)
        self.assertEqual(len(data['groups']), 1)
        self.assertEqual(data['groups'][0]['id'], self.group.id)

    # def test_update_user(self):
    #     from core.serializers import CustomUserSerializer
        
    #     updated_data = {
    #         "first_name": "Updated",
    #         "last_name": "Name",
    #         "email": "updated@example.com"
    #     }
        
    #     serializer = CustomUserSerializer(instance=self.user, data=updated_data, partial=True)
    #     self.assertTrue(serializer.is_valid(), serializer.errors)
        
    #     user = serializer.save()
    #     self.assertEqual(user.first_name, "Updated")
    #     self.assertEqual(user.last_name, "Name")
    #     self.assertEqual(user.email, "updated@example.com")

    # def test_excluded_fields_not_in_serializer(self):
    #     from core.serializers import CustomUserSerializer
        
    #     serializer = CustomUserSerializer(instance=self.user)
    #     data = serializer.data
        
    #     excluded_fields = [
    #         'subscription_start_date', 
    #         'subscription_end_date',
    #         'confirmation_code', 
    #         'confirmation_code_created_at',
    #         'user_permissions', 
    #         'is_staff', 
    #         'is_active', 
    #         'is_superuser',
    #         'last_login', 
    #         'password'
    #     ]
        
    #     for field in excluded_fields:
    #         self.assertNotIn(field, data)

    # def test_full_name_property(self):
    #     from core.serializers import CustomUserSerializer
        
    #     serializer = CustomUserSerializer(instance=self.user)
    #     data = serializer.data
        
    #     self.assertEqual(data['get_full_name'], "Doe Jane")
        
    #     # Проверяем с отчеством
    #     self.user.middle_name = "Middle"
    #     self.user.save()
        
    #     serializer = CustomUserSerializer(instance=self.user)
    #     data = serializer.data
    #     self.assertEqual(data['get_full_name'], "Doe Jane Middle")

    # def test_subscription_serialization(self):
    #     from core.serializers import CustomUserSerializer
        
    #     # Активируем подписку для пользователя
    #     self.user.subscription = self.subscription
    #     self.user.activate_subscription()
    #     self.user.save()
        
    #     serializer = CustomUserSerializer(instance=self.user)
    #     data = serializer.data
        
    #     self.assertEqual(data['subscription']['id'], self.subscription.id)
    #     self.assertTrue(data['has_active_subscription'])