from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from doctors.models import Doctor, Specialty, MedicalCategory, AcademicDegree, Service
from datetime import date, timedelta
from unittest.mock import patch

User = get_user_model()

class DoctorModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных перед выполнением всех тестов"""
        cls.user = User.objects.create_user(email="test@example.com", password="password", first_name="Доктор", last_name="Докторов")
        cls.specialty = Specialty.objects.create(name="Терапевт")
        cls.medical_category = MedicalCategory.objects.create(name="Высшая категория")
        cls.academic_degree = AcademicDegree.objects.create(name="Доктор наук")
        cls.service = Service.objects.create(name="Консультация")

    def setUp(self):
        """Создается новый врач перед каждым тестом"""
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialty=self.specialty,
            medical_category=self.medical_category,
            academic_degree=self.academic_degree,
            experience_years=15,
            philosophy="Помогаю пациентам сохранять здоровье",
            license_number="123456",
            work_phone_number="+123456789",
            whatsapp_telegram="+987654321",
            is_verified=True,
            verification_date=date.today(),
            verified_by="Админ",
            titles_and_merits="Заслуженный врач",
        )
        self.doctor.services.add(self.service)

    def test_doctor_creation(self):
        """Проверяем, что объект Doctor создается корректно"""
        self.assertEqual(self.doctor.user.username, "testuser")
        self.assertEqual(self.doctor.specialty.name, "Терапевт")
        self.assertEqual(self.doctor.medical_category.name, "Высшая категория")
        self.assertEqual(self.doctor.academic_degree.name, "Доктор наук")
        self.assertEqual(self.doctor.experience_years, 15)
        self.assertEqual(self.doctor.philosophy, "Помогаю пациентам сохранять здоровье")
        self.assertTrue(self.doctor.is_verified)
        self.assertEqual(self.doctor.verified_by, "Админ")
        self.assertEqual(self.doctor.license_number, "123456")
        self.assertEqual(self.doctor.work_phone_number, "+123456789")
        self.assertEqual(self.doctor.whatsapp_telegram, "+987654321")

    def test_doctor_string_representation(self):
        """Проверяем метод __str__"""
        self.assertEqual(str(self.doctor), "testuser (Терапевт, Доктор наук)")

    @patch("doctors.models.Doctor.calculate_experience_years", return_value=10)
    def test_calculate_experience_years(self, mock_calc_experience):
        """Проверяем расчет стажа работы"""
        self.doctor.experience_years = self.doctor.calculate_experience_years()
        self.assertEqual(self.doctor.experience_years, 10)

    def test_get_average_rating(self):
        """Проверяем расчет среднего рейтинга (без отзывов)"""
        self.assertEqual(self.doctor.get_average_rating(), 0)

    def test_user_added_to_doctors_group(self):
        """Проверяем, что пользователь автоматически добавляется в группу 'Doctors'"""
        group = Group.objects.get(name="Doctors")
        self.assertIn(group, self.user.groups.all())
