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
        self.create_superusers()
        self.create_all_test_data()

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
            'gender': User.Gender.MALE,
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
            'gender': User.Gender.MALE,
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
        from subscriptions.models import Advantage, Subscription
        from patients.models import SocialStatus, Patient
        from doctors.models import (
            Specialty, MedicalCategory, AcademicDegree, 
            Service, Language, LanguageLevel
        )

        # 1. Регионы и города (полный список)
        self.stdout.write("Создание регионов и городов...")
        try:
            call_command('loaddata', 'a_base/fixtures/initial_districts.json')
            self.stdout.write(self.style.SUCCESS('Регионы успешно загружены.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке районов: {str(e)}'))

        # 2. Подписки и преимущества (полный список)
        self.stdout.write("Создание подписок...")
        advantages_data = [
            {"name": "Базовый доступ", "description": "Доступ к базовым функциям приложения"},
            {"name": "Расширенный поиск", "description": "Возможность использовать расширенный поиск врачей"},
            {"name": "Приоритетная поддержка", "description": "Приоритет при обработке ваших запросов в поддержку"},
            {"name": "Без рекламы", "description": "Полное отсутствие рекламы в приложении"},
            {"name": "Экспресс-запись", "description": "Возможность записываться к врачам без очереди"},
            {"name": "Персональный ассистент", "description": "Помощь в подборе врачей и записи на прием"},
            {"name": "Неограниченные консультации", "description": "Неограниченное количество онлайн-консультаций"},
            {"name": "Анализы со скидкой", "description": "Скидка 20% на все анализы в партнерских лабораториях"},
        ]

        advantages = Advantage.objects.bulk_create([
            Advantage(**adv) for adv in advantages_data
        ])

        subscriptions_data = [
            {
                "name": "Базовая",
                "description": "Базовый набор возможностей для комфортного использования сервиса",
                "price": 100,
                "duration_days": 30,
                "advantages": ["Базовый доступ"]
            },
            {
                "name": "Стандартная",
                "description": "Расширенные возможности для более удобного поиска врачей",
                "price": 299,
                "duration_days": 30,
                "advantages": [
                    "Базовый доступ",
                    "Расширенный поиск",
                    "Приоритетная поддержка",
                    "Без рекламы"
                ]
            },
            {
                "name": "Премиум",
                "description": "Максимальный комфорт и персональный подход к вашему здоровью",
                "price": 799,
                "duration_days": 30,
                "advantages": [
                    "Базовый доступ",
                    "Расширенный поиск",
                    "Приоритетная поддержка",
                    "Без рекламы",
                    "Экспресс-запись",
                    "Персональный ассистент",
                    "Неограниченные консультации",
                    "Анализы со скидкой"
                ]
            }
        ]

        for sub_data in subscriptions_data:
            sub = Subscription.objects.create(
                name=sub_data["name"],
                description=sub_data["description"],
                price=sub_data["price"],
                duration_days=sub_data["duration_days"]
            )
            sub.advantages.add(*[
                adv for adv in advantages 
                if adv.name in sub_data["advantages"]
            ])
        self.stdout.write(self.style.SUCCESS('Подписки созданы!'))

        # 3. Медицинские данные (полные списки)
        self.stdout.write("Создание медицинских данных...")
        
        # Специальности
        specialties = [
            "Терапевт", "Анестезиолог-реаниматолог", "Реаниматолог",
            "Рентгенолог", "УЗИ-специалист", "Пульмонолог", "Кардиолог",
            "Судебно-медицинский эксперт"
        ]
        Specialty.objects.bulk_create([
            Specialty(name=name) for name in sorted(set(specialties), key=lambda x: x.lower())
        ])

        # Медицинские категории
        MedicalCategory.objects.bulk_create([
            MedicalCategory(name=name) for name in [
                "Категорияи олӣ", "Категорияи аввал", "Категорияи дуюм"
            ]
        ])

        # Ученые степени
        AcademicDegree.objects.bulk_create([
            AcademicDegree(name=name) for name in [
                "Кандидат медицинских наук", 
                "Доктор медицинских наук", 
                "Профессор"
            ]
        ])

        # Услуги
        Service.objects.bulk_create([
            Service(name=name) for name in [
                "Индивидуальная консультация (на рабочем месте)",
                "Онлайн консультация", 
                "Консультация с посещением пациента", 
                "Консультации в вечернее время вне рабочих часов", 
                "Консультации в выходные и праздничные дни",
                "Выдача рецептов"
            ]
        ])

        # Языки
        Language.objects.bulk_create([
            Language(name=name) for name in [
                "Таджикский", "Русский", "Английский", "Хинди", 
                "Узбекский", "Турецкий", "Немецкий", "Кыргызский"
            ]
        ])

        # Уровни языков
        LanguageLevel.objects.bulk_create([
            LanguageLevel(level=level) for level in [
                "Родной язык", "Свободное владение", 
                "Рабочий уровень", "Элементарный уровень"
            ]
        ])
        self.stdout.write(self.style.SUCCESS('Медицинские данные созданы!'))

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
        subscriptions = Subscription.objects.all()
        
        users_data = [
            {
                'phone_number': '+992000000000',
                'email': 'base@user.com',
                'first_name': 'Базовый',
                'last_name': 'Пользователь',
                'password': 'admin',
                'middle_name': 'Системы',
                'subscription': subscriptions[0],
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender': User.Gender.MALE,
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
                'subscription': subscriptions[1],
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender': User.Gender.MALE,
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
                'subscription': subscriptions[2],
                'subscription_start_date': timezone.now(),
                'subscription_end_date': timezone.now() + timedelta(days=30),
                'gender': User.Gender.MALE,
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