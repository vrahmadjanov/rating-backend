from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Получаем кастомную модель пользователя
User = get_user_model()

class Command(BaseCommand):
    help = 'Очищает базу данных и создает тестовые данные (полная версия)'

    def handle(self, *args, **kwargs):
        self.clean_database()
        self.create_groups()
        self.create_all_test_data()
        self.create_superusers()

    def clean_database(self):
        """Очистка всей базы данных"""
        self.stdout.write("Очистка базы данных...")
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("База данных очищена!"))

    def create_groups(self):
        """Создание групп пользователей"""
        groups = ["Doctors", "Patients", "Admins"]
        for name in groups:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Группы пользователей созданы!"))

    def create_superusers(self):
        """Создание администраторов системы"""
        admin_data = {
            'phone_number': '+992123456789',
            'email': 'admin@admin.com',
            'first_name': 'Admin',
            'last_name': 'Admin',
            'password': 'admin',
            'middle_name': '',
            'inn': '123456786',
            'date_of_birth': "2002-08-08",
            'is_superuser': True,
            'is_staff': True
        }

        staff_data = {
            'phone_number': '+992000000004',
            'email': 'staff@staff.com',
            'first_name': 'Staff',
            'last_name': 'Staff',
            'password': 'admin',
            'middle_name': '',
            'inn': '123456785',
            'date_of_birth': "2002-12-12",
            'is_staff': True
        }

        admin = User.objects.create_user(**admin_data)
        staff = User.objects.create_user(**staff_data)
        
        admin_group = Group.objects.get(name="Admins")
        admin.groups.add(admin_group)
        staff.groups.add(admin_group)

        self.stdout.write(self.style.SUCCESS('Администраторы созданы!'))

    def create_all_test_data(self):
        """Создание всех тестовых данных (полная версия)"""
        from patients.models import SocialStatus, Patient
        from a_base.models import Subscription, Gender

        # 1. Регионы и города (полный список)
        self.stdout.write("Создание регионов и городов...")
        try:
            call_command('loaddata', 'a_base/fixtures/districts.json')
            self.stdout.write(self.style.SUCCESS('Регионы успешно загружены.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке районов: {str(e)}'))

        # 2. Подписки и преимущества (полный список)
        self.stdout.write("Создание подписок...")
        try:
            call_command('loaddata', 'a_base/fixtures/subscriptions.json')
            self.stdout.write(self.style.SUCCESS('Информация о подписках успешно загружена.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке подписок: {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Подписки созданы!'))

        # 3. Медицинские данные (полные списки)
        self.stdout.write("Создание специализаций...")
        try:
            call_command('loaddata', 'a_base/fixtures/specialties.json')
            self.stdout.write(self.style.SUCCESS('Информация о специализациях успешно загружена.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке специализаций: {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Специализации созданы!'))

        # Клиники
        self.stdout.write("Создание клиник...")
        try:
            call_command('loaddata', 'a_base/fixtures/clinics.json')
            self.stdout.write(self.style.SUCCESS('Информация о клиниках успешно загружена.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке клиник: {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Клиники созданы!'))

        # Медицинские категории
        self.stdout.write("Создание медицинских категорий для врачей...")
        try:
            call_command('loaddata', 'a_base/fixtures/medical_categories.json')
            self.stdout.write(self.style.SUCCESS('Информация о медицинских категориях успешно загружена'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке медицинских категорий: {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Медицинские категории созданы!'))

        # Ученые степени
        self.stdout.write("Создание ученых степеней...")
        try:
            call_command('loaddata', 'a_base/fixtures/academic_degrees.json')
            self.stdout.write(self.style.SUCCESS('Ученые степени успешно загружены.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке ученых степеней: {str(e)}'))

        # Услуги
        self.stdout.write("Создание списка услуг...")
        try:
            call_command('loaddata', 'a_base/fixtures/services.json')
            self.stdout.write(self.style.SUCCESS('Список услуг успешно загружен.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке писка услуг: {str(e)}'))

        # Языки
        self.stdout.write("Создание списка языков и их уровней...")
        try:
            call_command('loaddata', 'a_base/fixtures/languages.json')
            self.stdout.write(self.style.SUCCESS('Список языков и их уровней успешно загружен.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке списка языков: {str(e)}'))


        self.stdout.write(self.style.SUCCESS('Медицинские данные созданы!'))

        # Пол
        self.stdout.write("Создание полов...")
        genders_dt = [
            {
                "name": "Мужской",
                "name_ru": "Мужской",
                "name_tg": "Мард"
            },
            {
                "name": "Женский",
                "name_ru": "Женский",
                "name_tg": "Зан"
            }
        ]

        for gender in genders_dt:
            Gender.objects.create(
                name=gender["name"],
                name_ru=gender["name_ru"],
                name_tg=gender["name_tg"]
                )
        self.stdout.write(self.style.SUCCESS('Полы успешно созданы!'))

        # 4. Социальные статусы (полный список)
        self.stdout.write("Создание социальных статусов...")
        SocialStatus.objects.bulk_create([
            SocialStatus(**status) for status in [
                {
                    "name": "Студент",
                    "description": "Лица, обучающиеся в образовательных учреждениях"
                },
                {
                    "name": "Пенсионер",
                    "description": "Лица, получающие пенсию по возрасту или инвалидности"
                },
                {
                    "name": "Рабочий",
                    "description": "Лица, занятые на производстве или в сфере услуг"
                },
                {
                    "name": "Безработный",
                    "description": "Лица, не имеющие постоянного места работы"
                },
                {
                    "name": "Инвалид",
                    "description": "Лица с ограниченными возможностями здоровья"
                },
                {
                    "name": "Ребенок",
                    "description": "Несовершеннолетние лица до 18 лет"
                },
                {
                    "name": "Военнослужащий",
                    "description": "Лица, проходящие военную службу"
                },
                {
                    "name": "Беременная",
                    "description": "Женщины в период беременности"
                },
                {
                    "name": "Многодетная семья",
                    "description": "Семьи с тремя и более детьми"
                },
                {
                    "name": "Ветеран",
                    "description": "Участники боевых действий и ветераны труда"
                }
            ]
        ])
        self.stdout.write(self.style.SUCCESS('Социальные статусы созданы!'))

        # 5. Тестовые пользователи с подписками
        from a_base.models import District
        self.stdout.write("Создание тестовых пользователей...")
        
        users_data = [
            {
                'phone_number': '+992000000000',
                'email': 'base@user.com',
                'first_name': 'Базовый',
                'last_name': 'Пользователь',
                'password': 'admin',
                'middle_name': 'Системы',
                'subscription': Subscription.objects.get(id=1),
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender': Gender.objects.get(name="Мужской"),
                'inn': '123456789',
                'date_of_birth': "2002-08-08",
                'district': District.objects.get(id=101)
            },
            {
                'phone_number': '+992000000001',
                'email': 'standart@user.com',
                'first_name': 'Стандартный',
                'last_name': 'Пользователь',
                'password': 'admin',
                'middle_name': 'Системы',
                'subscription': Subscription.objects.get(id=2),
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender':  Gender.objects.get(name="Мужской"),
                'inn': '123456788',
                'date_of_birth': "2002-08-08",
                'district': District.objects.get(id=201)
            },
            {
                'phone_number': '+992000000002',
                'email': 'premium@user.com',
                'first_name': 'Премиальный',
                'last_name': 'Пользователь',
                'password': 'admin',
                'middle_name': 'Системы',
                'subscription': Subscription.objects.get(id=3),
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender':  Gender.objects.get(name="Женский"),
                'inn': '123456787',
                'date_of_birth': "2002-08-08",
                'district': District.objects.get(id=301)
            }
        ]

        for user_data in users_data:
            user = User.objects.create_user(**user_data)
            Patient.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS('Тестовые пользователи созданы!'))
        self.stdout.write(self.style.SUCCESS('Все данные успешно созданы!'))