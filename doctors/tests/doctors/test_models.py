from django.test import TestCase
from django.contrib.auth import get_user_model
from a_base.models import (
    Specialty, MedicalCategory, AcademicDegree, 
    ExperienceLevel, Service, ServicePlace
)
from doctors.models import Doctor
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class DoctorModelTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.user = User.objects.create_user(
            phone_number='+992000000000',
            password='testpass123',
            first_name='TestUser',
            date_of_birth='1990-01-01',
        )
        
        self.specialty1 = Specialty.objects.create(name_ru='Кардиология', name_tg='Кардиология')
        self.specialty2 = Specialty.objects.create(name_ru='Неврология', name_tg='Неврология')
        self.medical_category = MedicalCategory.objects.create(name_ru='Высшая категория', name_tg='Категорияи олий')
        self.academic_degree = AcademicDegree.objects.create(name_ru='Кандидат медицинских наук', name_tg="н.и.т.")
        self.experience_level = ExperienceLevel.objects.create(level_ru="0-3 года", level_tg="0-3 сол")
        self.service_place = ServicePlace.objects.create(name_ru="На дому", name_tg="Дар хона")
        self.service1 = Service.objects.create(service_place=self.service_place, name_ru='Консультация', name_tg='Консультатсия')
        self.service2 = Service.objects.create(service_place=self.service_place, name_ru='Диагностика', name_tg='Диагностика')
        
        self.doctor_data = {
            'user': self.user,
            'medical_category': self.medical_category,
            'academic_degree': self.academic_degree,
            'experience_level': self.experience_level,
            'about': 'Опытный врач с 3-летним стажем',
            'license_number': 'LIC123456',
            'work_phone_number': '+992987654321',
            'whatsapp': '+992987654321',
            'telegram': '@johndoe',
            'titles_and_merits': 'Отличник здравоохранения'
        }
        
        self.doctor = Doctor.objects.create(**self.doctor_data)
        self.doctor.specialties.add(self.specialty1, self.specialty2)
        self.doctor.services.add(self.service1, self.service2)
    
    def test_doctor_creation(self):
        """Тестирование создания врача"""
        self.assertEqual(Doctor.objects.count(), 1)
        doctor = Doctor.objects.first()
        self.assertEqual(doctor.user, self.user)
        self.assertEqual(doctor.medical_category, self.medical_category)
        self.assertEqual(doctor.academic_degree, self.academic_degree)
        self.assertEqual(doctor.experience_level, self.experience_level)
        self.assertEqual(doctor.about, self.doctor_data['about'])
        self.assertEqual(doctor.license_number, self.doctor_data['license_number'])
        self.assertEqual(doctor.work_phone_number, self.doctor_data['work_phone_number'])
        self.assertEqual(doctor.whatsapp, self.doctor_data['whatsapp'])
        self.assertEqual(doctor.telegram, self.doctor_data['telegram'])
        self.assertEqual(doctor.titles_and_merits, self.doctor_data['titles_and_merits'])
    
    def test_specialties_relationship(self):
        """Тестирование связи со специализациями"""
        doctor = Doctor.objects.first()
        self.assertEqual(doctor.specialties.count(), 2)
        self.assertIn(self.specialty1, doctor.specialties.all())
        self.assertIn(self.specialty2, doctor.specialties.all())
    
    def test_services_relationship(self):
        """Тестирование связи с услугами"""
        doctor = Doctor.objects.first()
        self.assertEqual(doctor.services.count(), 2)
        self.assertIn(self.service1, doctor.services.all())
        self.assertIn(self.service2, doctor.services.all())
    
    def test_optional_fields(self):
        """Тестирование необязательных полей"""
        # Создаем врача без необязательных полей
        user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='TestUser2',
            date_of_birth='1990-01-01',
            )
        doctor = Doctor.objects.create(user=user2)
        
        self.assertIsNone(doctor.experience_level)
        self.assertIsNone(doctor.medical_category)
        self.assertIsNone(doctor.academic_degree)
        self.assertEqual(doctor.specialties.count(), 0)
        self.assertEqual(doctor.services.count(), 0)
        self.assertEqual(doctor.about, '')
        self.assertIsNone(doctor.license_number)
        self.assertIsNone(doctor.work_phone_number)
        self.assertIsNone(doctor.whatsapp)
        self.assertIsNone(doctor.telegram)
        self.assertEqual(doctor.titles_and_merits, '')
    
    def test_phone_validation(self):
        """Тестирование валидации телефонных номеров"""
        user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='TestUser2',
            date_of_birth='1990-01-01',
        )
        # Неправильный формат рабочего телефона
        with self.assertRaises(ValidationError):
            doctor = Doctor(
                user=user2,
                work_phone_number='992987654321',  # Нет + в начале
                experience_level=self.experience_level
            )
            doctor.full_clean()
        
        # Неправильный формат WhatsApp
        with self.assertRaises(ValidationError):
            doctor = Doctor(
                user=user2,
                whatsapp='+99298765432',  # Не хватает одной цифры
                experience_level=self.experience_level
            )
            doctor.full_clean()
        
        # Правильный формат
        try:
            doctor = Doctor(
                user=user2,
                work_phone_number='+992987654321',
                whatsapp='+992987654321',
                telegram='@valid',
                experience_level=self.experience_level
            )
            doctor.full_clean()
        except ValidationError:
            self.fail("Валидация не должна вызывать ошибку для правильных номеров")
    
    def test_str_representation(self):
        """Тестирование строкового представления"""
        doctor = Doctor.objects.first()
        expected_str = (
            f"{self.user.get_full_name} "
            f"(Кардиология, Неврология, {self.academic_degree.name})"
        )
        self.assertEqual(str(doctor), expected_str)
        
        # Проверка для врача без специализаций и степени
        user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='TestUser2',
            date_of_birth='1990-01-01',
        )
        doctor2 = Doctor.objects.create(user=user2)
        expected_str2 = f"{user2.get_full_name} (Без специализации, Без степени)"
        self.assertEqual(str(doctor2), expected_str2)
    
    def test_ordering(self):
        """Тестирование порядка сортировки"""
        user2 = User.objects.create_user(
            phone_number='+992000000001',
            password='testpass123',
            first_name='TestUser2',
            date_of_birth='1990-01-01',
        )
        doctor2 = Doctor.objects.create(
            user=user2,
            experience_level=self.experience_level
        )
        
        doctors = Doctor.objects.all()
        self.assertEqual(doctors[0], doctor2)  # Последний созданный должен быть первым
        self.assertEqual(doctors[1], self.doctor)
    
    def test_auto_timestamps(self):
        """Тестирование автоматических временных меток"""
        doctor = Doctor.objects.first()
        self.assertIsNotNone(doctor.created_at)
        self.assertIsNotNone(doctor.updated_at)
        
        # Проверка обновления updated_at
        old_updated_at = doctor.updated_at
        doctor.about = "Новое описание"
        doctor.save()
        self.assertNotEqual(doctor.updated_at, old_updated_at)
    
    def test_user_relationship(self):
        """Тестирование связи с пользователем"""
        self.assertEqual(self.user.doctor_profile, self.doctor)
        
        # Проверка, что один пользователь может иметь только один профиль врача
        with self.assertRaises(Exception):  # IntegrityError или ValueError
            Doctor.objects.create(user=self.user, experience_level=self.experience_level)