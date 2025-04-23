from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import Patient, SocialStatus
from map.models import City
import random
from faker import Faker

User = get_user_model()
fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Заполняет бд данными о пациентах'

    def handle(self, *args, **kwargs):
        self.stdout.write('Заполнение базы данных...')
        self.fill_database()
        self.stdout.write('База данных успешно заполнена.')

    def fill_database(self):
        # Получаем все существующие города и социальные статусы
        cities = City.objects.all()
        social_statuses = SocialStatus.objects.all()
        
        if not cities.exists():
            self.stdout.write(self.style.ERROR('Нет городов в базе данных. Сначала заполните города.'))
            return
            
        if not social_statuses.exists():
            self.stdout.write(self.style.ERROR('Нет социальных статусов в базе данных. Сначала заполните социальные статусы.'))
            return

        # Создаем 20 пользователей и пациентов
        for _ in range(20):
            user = self.create_user(cities)
            self.create_patient(user, social_statuses)

    def create_user(self, cities):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.middle_name()
        email = fake.unique.email()
        phone_number = f'+992{fake.numerify("##")}{fake.numerify("#######")}'
        gender = random.choice([User.Gender.MALE, User.Gender.FEMALE])
        inn = fake.unique.numerify('#########')
        
        # Генерируем дату рождения (от 18 до 90 лет назад)
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        
        # Выбираем случайный город
        city = random.choice(cities)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            phone_number=phone_number,
            gender=gender,
            inn=inn,
            date_of_birth=birth_date,
            city=city
        )
        
        return user

    def create_patient(self, user, social_statuses):
        registration_address = fake.address()
        passport = fake.numerify('########')
        actual_address = fake.address()
        sin = fake.unique.numerify('##########')
        eng = fake.unique.numerify('##########')
        social_status = random.choice(social_statuses)

        Patient.objects.create(
            user=user,
            passport = passport,
            registration_address=registration_address,
            actual_address=actual_address,
            sin=sin,
            eng=eng,
            social_status=social_status
        )