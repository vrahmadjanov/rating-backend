from rest_framework.test import APITestCase
from rest_framework import serializers
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from a_base.models import (
    Specialty, MedicalCategory, AcademicDegree, 
    ExperienceLevel, Service, ServicePlace, Gender
)

User = get_user_model()

class DoctorSerializerTestCase(APITestCase):
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
        self.gender = Gender.objects.create(name_ru="Мужской", name_tg="Мард")
        
        self.doctor = Doctor.objects.create(
            user=self.user,
            medical_category=self.medical_category,
            academic_degree=self.academic_degree,
            experience_level=self.experience_level,
            about='Опытный врач',
            philosophy='Индивидуальный подход',
            license_number='LIC123',
            work_phone_number='+992987654321',
            whatsapp='+992987654321',
            telegram='@johndoe',
            titles_and_merits='Отличник здравоохранения'
        )
        self.doctor.specialties.add(self.specialty1, self.specialty2)
        self.doctor.services.add(self.service1, self.service2)
        
        # Данные для создания/обновления врача
        self.valid_doctor_data = {
            'user': {
                'phone_number': '+992000000001',
                'password': 'testpass123',
                'first_name': 'TestUserFirstName',
                'last_name': 'TestUserLastName',
                'date_of_birth': '1990-01-01',
            },
            'specialties_ids': [self.specialty1.id],
            'medical_category_id': self.medical_category.id,
            'academic_degree_id': self.academic_degree.id,
            'experience_level_id': self.experience_level.id,
            'services_ids': [self.service1.id, self.service2.id],
            'about': 'Новый врач',
            'philosophy': 'Новый подход',
            'license_number': 'LIC456',
            'work_phone_number': '+992987654322',
            'whatsapp': '+992987654322',
            'telegram': '@janesmith',
            'titles_and_merits': 'Новые заслуги'
        }

    def test_serialization(self):
        """Тестирование сериализации (объект -> JSON)"""
        serializer = DoctorSerializer(instance=self.doctor)
        data = serializer.data
        
        # Проверяем основные поля
        self.assertEqual(data['id'], self.doctor.id)
        self.assertEqual(data['about'], self.doctor.about)
        self.assertEqual(data['license_number'], self.doctor.license_number)
        
        # Проверяем вложенные сериализаторы
        self.assertEqual(len(data['specialties']), 2)
        self.assertEqual(data['specialties'][0]['name'], self.specialty1.name)
        self.assertEqual(data['medical_category']['name'], self.medical_category.name)
        self.assertEqual(data['academic_degree']['name'], self.academic_degree.name)
        self.assertEqual(data['experience_level']['level'], self.experience_level.level)
        self.assertEqual(len(data['services']), 2)
        
        # Проверяем, что write-only поля отсутствуют в выходных данных
        self.assertNotIn('specialties_ids', data)
        self.assertNotIn('medical_category_id', data)
        self.assertNotIn('academic_degree_id', data)
        self.assertNotIn('experience_level_id', data)
        self.assertNotIn('services_ids', data)

    def test_deserialization_create(self):
        """Тестирование десериализации при создании (JSON -> объект)"""
        serializer = DoctorSerializer(data=self.valid_doctor_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        doctor = serializer.save()
        
        # Проверяем созданные объекты
        self.assertEqual(doctor.about, self.valid_doctor_data['about'])
        self.assertEqual(doctor.medical_category.id, self.valid_doctor_data['medical_category_id'])
        self.assertEqual(doctor.academic_degree.id, self.valid_doctor_data['academic_degree_id'])
        self.assertEqual(doctor.experience_level.id, self.valid_doctor_data['experience_level_id'])
        self.assertEqual(doctor.license_number, self.valid_doctor_data['license_number'])
        
        # Проверяем связи ManyToMany
        self.assertEqual(doctor.specialties.count(), 1)
        self.assertEqual(doctor.specialties.first().id, self.specialty1.id)
        self.assertEqual(doctor.services.count(), 2)
        
        # Проверяем созданного пользователя
        self.assertEqual(doctor.user.phone_number, self.valid_doctor_data['user']['phone_number'])
        self.assertEqual(doctor.user.first_name, self.valid_doctor_data['user']['first_name'])
        self.assertEqual(doctor.user.last_name, self.valid_doctor_data['user']['last_name'])
        self.assertEqual(doctor.user.password, self.valid_doctor_data['user']['password'])

    def test_deserialization_update(self):
        """Тестирование обновления существующего врача"""
        update_data = {
            'specialties_ids': [self.specialty2.id],
            'medical_category_id': None,  # Удаляем категорию
            'academic_degree_id': self.academic_degree.id,
            'services_ids': [self.service2.id],
            'about': 'Обновленное описание',
            'philosophy': 'Новая философия',
            'work_phone_number': '+992987654333',
            'user': {
                'first_name': 'John Updated',
                'last_name': 'Doe Updated'
            }
        }
        
        serializer = DoctorSerializer(instance=self.doctor, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        doctor = serializer.save()
        
        # Проверяем обновленные поля
        self.assertEqual(doctor.about, update_data['about'])
        self.assertEqual(doctor.philosophy, update_data['philosophy'])
        self.assertEqual(doctor.work_phone_number, update_data['work_phone_number'])
        self.assertIsNone(doctor.medical_category)
        
        # Проверяем обновленные связи
        self.assertEqual(doctor.specialties.count(), 1)
        self.assertEqual(doctor.specialties.first().id, self.specialty2.id)
        self.assertEqual(doctor.services.count(), 1)
        self.assertEqual(doctor.services.first().id, self.service2.id)

    def test_invalid_data(self):
        """Тестирование с невалидными данными"""
        invalid_data = {
            'specialties_ids': [999],  # Несуществующая специализация
            'medical_category_id': 999,  # Несуществующая категория
            'work_phone_number': '992987654321',  # Неправильный формат
        }
        
        serializer = DoctorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
        # Проверяем наличие ожидаемых ошибок
        self.assertIn('specialties_ids', serializer.errors)
        self.assertIn('medical_category_id', serializer.errors)
        self.assertIn('work_phone_number', serializer.errors)
        self.assertIn('user', serializer.errors)

    def test_update_method(self):
        """Тестирование метода update сериализатора"""
        serializer = DoctorSerializer()
        
        update_data = {
            'specialties': [self.specialty1],
            'medical_category': self.medical_category,
            'academic_degree': None,
            'services': [self.service1],
            'about': 'Новое описание',
            'philosophy': 'Новая философия',
            'license_number': 'NEW123',
            'work_phone_number': '+992987654444',
            'whatsapp': '+992987654444',
            'telegram': '@updated',
            'titles_and_merits': 'Новые заслуги'
        }
        
        updated_doctor = serializer.update(self.doctor, update_data)
        
        # Проверяем обновленные поля
        self.assertEqual(updated_doctor.about, update_data['about'])
        self.assertEqual(updated_doctor.philosophy, update_data['philosophy'])
        self.assertEqual(updated_doctor.license_number, update_data['license_number'])
        self.assertEqual(updated_doctor.work_phone_number, update_data['work_phone_number'])
        self.assertEqual(updated_doctor.whatsapp, update_data['whatsapp'])
        self.assertEqual(updated_doctor.telegram, update_data['telegram'])
        self.assertEqual(updated_doctor.titles_and_merits, update_data['titles_and_merits'])
        
        # Проверяем обновленные связи
        self.assertEqual(list(updated_doctor.specialties.all()), update_data['specialties'])
        self.assertEqual(updated_doctor.medical_category, update_data['medical_category'])
        self.assertIsNone(updated_doctor.academic_degree)
        self.assertEqual(list(updated_doctor.services.all()), update_data['services'])

    def test_partial_update(self):
        """Тестирование частичного обновления"""
        original_about = self.doctor.about
        original_philosophy = self.doctor.philosophy
        
        update_data = {
            'work_phone_number': '+992987654555',
        }
        
        serializer = DoctorSerializer(instance=self.doctor, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        doctor = serializer.save()
        
        # Проверяем обновленные поля
        self.assertEqual(doctor.work_phone_number, update_data['work_phone_number'])
        
        # Проверяем, что другие поля не изменились
        self.assertEqual(doctor.about, original_about)
        self.assertEqual(doctor.philosophy, original_philosophy)
        self.assertEqual(doctor.medical_category, self.medical_category)
        self.assertEqual(doctor.academic_degree, self.academic_degree)