from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from a_base.models import SocialStatus, Gender, District, Subscription, Advantage, Region
from patients.models import Patient

User = get_user_model()


class PatientModelTest(TestCase):
    def setUp(self):
        # Создаем необходимые связанные объекты
        self.region = Region.objects.create(name="Душанбе")
        self.district = District.objects.create(name="Душанбе", region=self.region)
        self.gender = Gender.objects.create(name="Мужской", name_ru="Мужской", name_tg="Мард")
        self.social_status = SocialStatus.objects.create(
            name="Рабочий",
            name_ru="Рабочий",
            name_tg="Коргар",
            description="Лица, занятые на производстве или в сфере услуг",
            description_ru="Лица, занятые на производстве или в сфере услуг",
            description_tg="Шахсоне, ки дар истеҳсолот ё соҳаи хидматрасонӣ машғуланд"
            )
        
        self.advantage = Advantage.objects.create(
            name="Базовый доступ",
            name_ru="Базовый доступ",
            name_tg="Дастрасии асосӣ",

            description="Доступ к базовым функциям приложения",
            description_ru="Доступ к базовым функциям приложения",
            description_tg="Дастрасӣ ба функсияҳои асосии барнома"
        )

        self.subscription = Subscription.objects.create(
            name="Базовая",
            name_ru="Базовая",
            name_tg="Асосӣ",

            description="Базовый набор возможностей для комфортного использования сервиса",
            description_ru="Базовый набор возможностей для комфортного использования сервиса",
            description_tg="Маҷмуаи асосии имконот барои истифодаи осони хизмат",

            price=100,
            duration_days=30,
        )

        self.subscription.advantages.add(self.advantage)
        
        # Создаем пользователя
        self.user = User.objects.create(
            first_name='Иван',
            last_name='Иванов',
            middle_name='Иванович',
            date_of_birth=date(1990, 1, 1),
            gender=self.gender,
            district=self.district,
            phone_number='+992123456789',
            email='ivan@example.com',
            subscription=self.subscription
        )
        
        # Данные для создания пациента
        self.patient_data = {
            'user': self.user,
            'passport': '1234567890',
            'registration_address': 'Душанбе, ул. Ленина 1',
            'actual_address': 'Душанбе, ул. Ленина 1',
            'sin': '123456789012',
            'eng': '1234567890123456',
            'weight': Decimal('75.50'),
            'height': Decimal('180.00'),
            'blood_type': 'A+',
            'social_status': self.social_status
        }

    def test_create_patient(self):
        """Тестирование создания пациента"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Проверяем, что объект создан
        self.assertIsInstance(patient, Patient)
        self.assertEqual(Patient.objects.count(), 1)
        
        # Проверяем поля
        self.assertEqual(patient.user, self.user)
        self.assertEqual(patient.passport, '1234567890')
        self.assertEqual(patient.registration_address, 'Душанбе, ул. Ленина 1')
        self.assertEqual(patient.actual_address, 'Душанбе, ул. Ленина 1')
        self.assertEqual(patient.sin, '123456789012')
        self.assertEqual(patient.eng, '1234567890123456')
        self.assertEqual(patient.weight, Decimal('75.50'))
        self.assertEqual(patient.height, Decimal('180.00'))
        self.assertEqual(patient.blood_type, 'A+')
        self.assertEqual(patient.social_status, self.social_status)
        
        # Проверяем автоматически заполняемые поля
        self.assertIsNotNone(patient.created_at)
        self.assertIsNotNone(patient.updated_at)

    def test_update_patient(self):
        """Тестирование полного обновления пациента"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Обновляем данные
        new_social_status = SocialStatus.objects.create(
            name="Пенсионер",
            name_ru="Пенсионер",
            name_tg="Нафақахӯр",
            description="Лица, получающие пенсию по возрасту или инвалидности",
            description_ru="Лица, получающие пенсию по возрасту или инвалидности",
            description_tg="Шахсоне, ки нафақа гирифта, аз рӯи синну сол ё маъюбӣ"
            )
        
        updated_data = {
            'passport': '0987654321',
            'registration_address': 'Душанбе, ул. Сомони 2',
            'actual_address': 'Душанбе, ул. Сомони 2',
            'sin': '987654321098',
            'eng': '9876543210987654',
            'weight': Decimal('80.00'),
            'height': Decimal('182.00'),
            'blood_type': 'B+',
            'social_status': new_social_status
        }
        
        # Обновляем объект
        for field, value in updated_data.items():
            setattr(patient, field, value)
        patient.save()
        
        # Перезагружаем объект из базы
        patient.refresh_from_db()
        
        # Проверяем обновленные поля
        self.assertEqual(patient.passport, '0987654321')
        self.assertEqual(patient.registration_address, 'Душанбе, ул. Сомони 2')
        self.assertEqual(patient.actual_address, 'Душанбе, ул. Сомони 2')
        self.assertEqual(patient.sin, '987654321098')
        self.assertEqual(patient.eng, '9876543210987654')
        self.assertEqual(patient.weight, Decimal('80.00'))
        self.assertEqual(patient.height, Decimal('182.00'))
        self.assertEqual(patient.blood_type, 'B+')
        self.assertEqual(patient.social_status, new_social_status)

    def test_partial_update_patient(self):
        """Тестирование частичного обновления пациента"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Обновляем только некоторые поля
        patient.weight = Decimal('77.00')
        patient.blood_type = 'AB+'
        patient.save()
        
        # Перезагружаем объект из базы
        patient.refresh_from_db()
        
        # Проверяем обновленные поля
        self.assertEqual(patient.weight, Decimal('77.00'))
        self.assertEqual(patient.blood_type, 'AB+')
        
        # Проверяем, что остальные поля не изменились
        self.assertEqual(patient.passport, '1234567890')
        self.assertEqual(patient.height, Decimal('180.00'))

    def test_delete_patient(self):
        """Тестирование удаления пациента"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Проверяем, что объект создан
        self.assertEqual(Patient.objects.count(), 1)
        
        # Удаляем объект
        patient.delete()
        
        # Проверяем, что объект удален
        self.assertEqual(Patient.objects.count(), 0)

    def test_patient_str_representation(self):
        """Тестирование строкового представления пациента"""
        patient = Patient.objects.create(**self.patient_data)
        expected_str = f"{self.user.get_full_name} (Пользователь: {self.user.email})"
        self.assertEqual(str(patient), expected_str)

    def test_patient_bmi_property(self):
        """Тестирование вычисления индекса массы тела (BMI)"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Проверяем расчет BMI (75.5 / (1.8 * 1.8) ≈ 23.30)
        self.assertAlmostEqual(float(patient.bmi), 23.30, places=2)
        
        # Проверяем случай, когда рост или вес не указаны
        patient.height = None
        patient.save()
        self.assertIsNone(patient.bmi)

    # def test_patient_age_property(self):
    #     """Тестирование вычисления возраста пациента"""
    #     # Устанавливаем дату рождения пользователя
    #     self.user.date_of_birth = date(1990, 1, 1)
    #     self.user.save()
        
    #     patient = Patient.objects.create(**self.patient_data)
        
    #     # Рассчитываем ожидаемый возраст
    #     today = timezone.now()
    #     expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))
        
    #     self.assertEqual(patient.age, expected_age)

    def test_patient_relations(self):
        """Тестирование связей модели Patient"""
        patient = Patient.objects.create(**self.patient_data)
        
        # Проверяем связь с пользователем
        self.assertEqual(patient.user, self.user)
        self.assertEqual(self.user.patient_profile, patient)
        
        # Проверяем связь с социальным статусом
        self.assertEqual(patient.social_status, self.social_status)