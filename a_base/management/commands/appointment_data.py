import random
from datetime import datetime, timedelta, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Генерирует тестовые записи на прием к врачам с учетом их расписания'

    def handle(self, *args, **options):
        self.stdout.write("Начало генерации тестовых записей на прием...")
        
        if not Doctor.objects.exists():
            self.stdout.write(self.style.ERROR('Нет врачей в базе данных. Сначала создайте врачей.'))
            return
            
        if not Patient.objects.exists():
            self.stdout.write(self.style.ERROR('Нет пациентов в базе данных. Сначала создайте пациентов.'))
            return
        
        self.generate_appointments()

        self.stdout.write(self.style.SUCCESS('Тестовые записи на прием успешно созданы!'))

    def generate_appointments(self):
        doctors = Doctor.objects.prefetch_related('workplaces__schedule').all()
        patients = Patient.objects.all()
        
        created_count = 0
        attempts = 0
        max_attempts = 200  # Максимальное количество попыток создать записи
        
        while created_count < 100 and attempts < max_attempts:
            attempts += 1
            doctor = random.choice(doctors)
            patient = random.choice(patients)
            
            # Выбираем случайную дату в ближайшие 30 дней
            appointment_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
            
            # Получаем доступные слоты для врача на эту дату
            available_slots = self.get_available_slots(doctor, appointment_date)
            
            if not available_slots:
                continue  # Пропускаем если нет доступных слотов
            
            # Выбираем случайный доступный слот
            start_time, end_time = random.choice(available_slots)
            
            # Определяем статус записи
            status, cancel_reason, cancel_notes, cancelled_at = self.generate_status(appointment_date)
            
            # Генерируем данные о пациенте
            is_another_patient = random.random() < 0.2  # 20% вероятность записи другого человека
            another_data = self.generate_another_patient_data() if is_another_patient else {}
            
            # Создаем запись
            try:
                Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    appointment_date=appointment_date,
                    start_time=start_time,
                    end_time=end_time,
                    status=status,
                    cancellation_reason=cancel_reason,
                    cancellation_notes=cancel_notes,
                    cancelled_at=cancelled_at,
                    phone_number=patient.user.phone_number,
                    is_another_patient=is_another_patient,
                    **another_data,
                    problem_description=fake.text(max_nb_chars=200) if random.random() < 0.7 else None
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при создании записи: {e}'))

    def get_available_slots(self, doctor, date):
        """Возвращает доступные временные слоты для записи к врачу на указанную дату"""
        available_slots = []
        
        # Проверяем все рабочие места врача
        for workplace in doctor.workplaces.all():
            if not hasattr(workplace, 'schedule'):
                continue
                
            schedule = workplace.schedule
            slots = schedule.get_available_slots(date)
            
            # Фильтруем слоты, которые уже заняты в других рабочих местах
            for slot in slots:
                if not Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=date,
                    start_time=slot[0],
                    end_time=slot[1],
                    status=Appointment.Status.UPCOMING
                ).exists():
                    available_slots.append(slot)
        
        return available_slots

    def generate_status(self, appointment_date):
        """Генерирует статус записи и связанные данные"""
        now = timezone.now()
        appointment_datetime = timezone.make_aware(datetime.combine(appointment_date, time(0, 0)))
        
        if appointment_datetime < now:
            # Прошедшие записи
            status_choice = random.choices(
                [Appointment.Status.COMPLETE, Appointment.Status.CANCELLED, Appointment.Status.NOSHOW],
                weights=[70, 20, 10]  # 70% завершенных, 20% отмененных, 10% неявок
            )[0]
            
            if status_choice == Appointment.Status.CANCELLED:
                cancel_reason = random.choice(Appointment.CancelReason.choices)[0]
                cancel_notes = fake.sentence() if cancel_reason == 'others' else None
                cancelled_at = appointment_datetime - timedelta(days=random.randint(1, 7))
                return status_choice, cancel_reason, cancel_notes, cancelled_at
            elif status_choice == Appointment.Status.NOSHOW:
                return status_choice, None, None, None
            else:
                return status_choice, None, None, None
        else:
            # Будущие записи
            return Appointment.Status.UPCOMING, None, None, None

    def generate_another_patient_data(self):
        """Генерирует данные для случая записи другого человека"""
        gender = random.choice(['M', 'F', 'other'])
        
        return {
            'another_patient_name': fake.name(),
            'another_patient_age': random.randint(1, 90),
            'another_patient_gender': gender,
            'phone_number': f'+992{fake.numerify("##")}{fake.numerify("######")}'
        }