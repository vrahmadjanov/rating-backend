import random
from datetime import time
from faker import Faker
from django.core.management.base import BaseCommand
from doctors.models import MedicalInstitution, Workplace, Doctor, Schedule

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Создает рабочие места для докторов и заполняет их расписания'

    def handle(self, *args, **options):
        # Проверяем наличие докторов и медицинских учреждений
        if not Doctor.objects.exists():
            self.stdout.write(self.style.ERROR('Нет докторов в базе данных. Сначала создайте докторов.'))
            return
            
        if not MedicalInstitution.objects.exists():
            self.stdout.write(self.style.ERROR('Нет медицинских учреждений в базе данных. Сначала создайте учреждения.'))
            return

        # Добавление рабочих мест каждому врачу
        doctors = Doctor.objects.all()
        institutions = list(MedicalInstitution.objects.all())
        
        for doctor in doctors:
            # Выбираем от 1 до 3 случайных учреждений для каждого врача
            workplaces_count = random.randint(1, min(3, len(institutions)))
            workplaces = random.sample(institutions, k=workplaces_count)
            
            for institution in workplaces:
                position = random.choice(["Врач", "Старший врач", "Главный врач", "Заведующий отделением"])
                start_date = fake.date_between(start_date="-10y", end_date="today")
                
                # 30% chance that doctor no longer works here
                end_date = fake.date_between(start_date=start_date, end_date="today") if random.random() < 0.3 else None

                workplace, created = Workplace.objects.get_or_create(
                    doctor=doctor,
                    medical_institution=institution,
                    defaults={
                        'position': position,
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )

                # Добавление/обновление расписания для каждого рабочего места
                self.stdout.write(f"Создание расписания для {doctor} в {institution.name}...")
                self.create_or_update_schedule(workplace)

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))

    def create_or_update_schedule(self, workplace):
        """Создает или обновляет реалистичное расписание для рабочего места"""
        # Определяем параметры расписания
        schedule_data = {
            'appointment_interval': random.choice([15, 20, 30, 45, 60]),
        }
        
        # Добавляем рабочие часы для каждого дня
        days = {
            'monday': 0.8,    # 80% вероятность работы в понедельник
            'tuesday': 0.8,
            'wednesday': 0.8,
            'thursday': 0.8,
            'friday': 0.8,
            'saturday': 0.3,   # 30% вероятность работы в субботу
            'sunday': 0.1      # 10% вероятность работы в воскресенье
        }
        
        for day, probability in days.items():
            if random.random() < probability:
                start_hour = random.randint(8, 10)  # Начало работы между 8 и 10 утра
                end_hour = start_hour + random.randint(6, 10)  # Рабочий день 6-10 часов
                end_hour = min(end_hour, 20)  # Ограничиваем максимальное время окончания до 20:00
                
                schedule_data[f'{day}_start'] = time(hour=start_hour, minute=0)
                schedule_data[f'{day}_end'] = time(hour=end_hour, minute=0)
            else:
                schedule_data[f'{day}_start'] = None
                schedule_data[f'{day}_end'] = None
        
        # Создаем или обновляем расписание
        Schedule.objects.update_or_create(
            workplace=workplace,
            defaults=schedule_data
        )