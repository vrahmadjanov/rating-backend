import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from a_base.models import Gender, District, ExperienceLevel, Specialty
from clinics.models import Clinic, ClinicType
from doctors.models import Doctor, Workplace
from datetime import datetime
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Imports doctors from a fixed Excel file path'

    COLUMN_MAPPING = {
        'Фамилия': 'last_name_ru',
        'Насаб(фамилия)': 'last_name_tg',
        'Имя': 'first_name_ru',
        'Ном(имя)': 'first_name_tg',
        'Отчество': 'middle_name_ru',
        'Номипадар(отчество)': 'middle_name_tg',
        'Дата рождения (ДД/ММ/ГГГГ)': 'date_of_birth',
        'Пол': 'gender',
        'Район': 'district',
        'Индивидуальный номер налогоплательщика (ИНН)': 'inn',
        'Ваш номер телефона для связи с пациентами': 'work_phone_number',
        'Ваш номер Ватсап для связи с пациентами': 'whatsapp',
        'Ваш номер Телеграм для связи с пациентами': 'telegram',
        'Ваш адрес электронной почты': 'email',

        'Профессиональный стаж работы в здравоохранении (количество лет)': 'experience_level',
        'Специализация по лечебному профилю': 'specialty_ru',
        'Ихтисос ё самти фаъолият (специализация)': 'specialty_tg',

        'Выберете название своего медицинского учреждения': 'clinic_name_ru',
        'Номи муассисаи тиббии худро интихоб кунед': 'clinic_name_tg',
        'Напишите свою текущую должность': 'position_ru',
        'Вазифаи ҳозираи худро ба пуррагӣ нависед.': 'position_tg',
        }

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "sughd_db.xlsx")

        try:
            # Чтение и переименование столбцов
            df = pd.read_excel(file_path, usecols=self.COLUMN_MAPPING.keys(), dtype=str)
            df.rename(columns=self.COLUMN_MAPPING, inplace=True)
        
            # Счетчики
            created_doctors = 0
            created_clinics = 0
            created_workplaces = 0
            errors = 0
            
            for index, row in df.iterrows():
                try:
                    first_name = row['first_name_tg'] if pd.isna(row['first_name_ru']) or row['first_name_ru'] == '' else row['first_name_ru']
                    last_name = row['last_name_tg'] if pd.isna(row['last_name_ru']) or row['last_name_ru'] == '' else row['last_name_tg']
                    middle_name = row['middle_name_tg'] if pd.isna(row['middle_name_ru']) or row['middle_name_ru'] == '' else row['middle_name_tg']

                    date_of_birth = datetime.strptime(row['date_of_birth'], "%d/%m/%Y").date()

                    gender = Gender.objects.get(name_ru=row['gender'])
                    
                    district = District.objects.get(name_ru=row['district'])
                    
                    clinic_type = ClinicType.objects.get(id=1)
                    
                    clinic, clinic_created = Clinic.objects.get_or_create(
                        clinic_type = clinic_type,
                        name_ru=row['clinic_name_ru'], 
                        name_tg=row['clinic_name_tg'],
                        district=district,
                        address_ru="Пока без адреса..."
                        )
                    
                    if clinic_created:
                        created_clinics += 1
                    
                    email = row['email'] if row['email'] != '-' or '' else None
                    phone_number = row['work_phone_number'] if row['work_phone_number'] not in ('-', '') else None
                    inn = int(row['inn']) if pd.notna(row['inn']) else None

                    experience_level = ExperienceLevel.objects.get(level_ru=row['experience_level'])
                    
                    # Создание пользователя
                    user, user_created = User.objects.get_or_create(
                            phone_number=phone_number,
                            first_name=first_name,
                            last_name=last_name,
                            middle_name=middle_name,
                            date_of_birth=date_of_birth,
                            gender=gender,
                            district=district,
                            inn=inn,
                            email=email
                    )
                        
                    # Создает профиль врача
                    doctor, doctor_created = Doctor.objects.get_or_create(
                        user=user,
                        experience_level=experience_level,
                        work_phone_number=row['work_phone_number'],
                        whatsapp=row['whatsapp'],
                        telegram=row['telegram'],
                    )
                    
                    if doctor_created:
                        created_doctors += 1

                    workplace, workplace_created = Workplace.objects.get_or_create(
                        doctor=doctor, 
                        clinic=clinic, 
                        position_ru=row['position_ru'], 
                        position_tg=row['position_tg']
                        )
                    
                    if workplace_created:
                        created_workplaces += 1
                
                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.ERROR(f'{errors-1}. Error processing row {index}: {str(e)}'))
                    continue
            
            self.stdout.write(self.style.SUCCESS(
                f'Import completed. Created: {created_doctors} doctors, {created_clinics} clinics, {created_workplaces} workplaces. Errors: {errors}'
            ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file: {str(e)}'))