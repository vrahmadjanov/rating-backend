import os
import random
import tempfile
from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker
from django.conf import settings
from core.models import CustomUser
from a_base.models import City
from doctors.models import (
    Doctor, Specialty, MedicalCategory, AcademicDegree, Service,
    Language, LanguageLevel, UserLanguage
)

fake = Faker('ru_RU')

def get_random_image(folder):
    """Возвращает случайное изображение из указанной папки."""
    image_path = os.path.join(settings.BASE_DIR, folder)
    images = [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))]
    
    if not images:
        return None, None
        
    random_image = random.choice(images)
    with open(os.path.join(image_path, random_image), 'rb') as f:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(f.read())
        temp_file.seek(0)
    
    return random_image, temp_file

class Command(BaseCommand):
    help = 'Создает 20 тестовых врачей'

    def handle(self, *args, **kwargs):
        # Получаем все необходимые данные одним запросом
        models_data = {
            'specialties': Specialty.objects.all(),
            'medical_categories': MedicalCategory.objects.all(),
            'academic_degrees': AcademicDegree.objects.all(),
            'services': Service.objects.all(),
            'languages': Language.objects.all(),
            'language_levels': LanguageLevel.objects.all(),
            'cities': City.objects.all()
        }

        self.stdout.write("Создание тестовых данных...")
        
        for _ in range(20):
            # Создаем пользователя
            user_data = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'middle_name': fake.middle_name(),
                'email': fake.unique.email(),
                'phone_number': f"+992{random.randint(100000000, 999999999)}",
                'gender': random.choice(['M', 'F']),
                'inn': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
                'city': random.choice(list(models_data['cities'])),
                'is_active': False
            }
            
            user = CustomUser.objects.create_user(**user_data)
            user.generate_confirmation_code()

            # Создаем врача
            is_verified = random.choice([True, False])
            doctor_data = {
                'user': user,
                'medical_category': random.choice(list(models_data['medical_categories'])),
                'academic_degree': random.choice(list(models_data['academic_degrees'])),
                'experience_years': random.choice(Doctor.ExperienceChoices.values),
                'philosophy': fake.text(max_nb_chars=200),
                'license_number': f"LIC{random.randint(1000, 9999)}",
                'work_phone_number': f"+992{random.randint(100000000, 999999999)}",
                'whatsapp': f"+992{random.randint(100000000, 999999999)}",
                'telegram': f"+992{random.randint(100000000, 999999999)}",
                'is_verified': is_verified,
                'verification_date': fake.date_between(start_date='-5y') if is_verified else None,
                'verified_by': fake.name() if is_verified else None,
                'titles_and_merits': fake.text(max_nb_chars=100)
            }
            
            doctor = Doctor.objects.create(**doctor_data)
            
            # Многие ко многим
            doctor.specialty.set(random.sample(list(models_data['specialties']), random.randint(1, 3)))
            doctor.services.set(random.sample(list(models_data['services']), random.randint(1, 3)))
            
            # Языки
            for lang in random.sample(list(models_data['languages']), random.randint(1, 3)):
                UserLanguage.objects.create(
                    doctor=doctor,
                    language=lang,
                    level=random.choice(list(models_data['language_levels']))
                )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))