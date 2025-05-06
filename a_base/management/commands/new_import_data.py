import os
from django.db.models import Q
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from a_base.models import (Gender, District, ExperienceLevel, University, Specialty, MedicalCategory, 
                           AcademicDegree, Language, LanguageLevel, Service, ServicePlace)
from clinics.models import Clinic, ClinicType
from doctors.models import Doctor, Workplace, Education, DoctorLanguage
from datetime import datetime
from django.conf import settings
import re

User = get_user_model()

def user_exists(phone_number=None, inn=None, email=None):
    """Проверяет, существует ли пользователь с такими данными"""
    query = Q()
    if phone_number:
        query |= Q(phone_number=phone_number)
    if inn:
        query |= Q(inn=inn)
    if email:
        query |= Q(email=email)
    
    return User.objects.filter(query).exists()

def clean_phone(phone_number):
    """Проверка и очистка номера телефона"""
    if pd.isna(phone_number) or not phone_number:
        return None
        
    phone_number = str(phone_number).strip()
    if not re.match(r'^\+992\d{9}$', phone_number):
        return None
    return phone_number

def clean_date(date_of_birth):
    """Проверка и преобразование даты"""
    if pd.isna(date_of_birth) or not date_of_birth:
        return None

    try:
        return datetime.strptime(str(date_of_birth), "%d/%m/%Y").date()
    except (ValueError, TypeError):
        return None

def clean_inn(inn):
    """Проверка и очистка ИНН"""
    if pd.isna(inn) or not inn:
        return None
        
    inn = str(inn).strip()
    if len(inn) != 9 or not inn.isdigit():
        return False
    return inn

def clean_graduation_year(graduation_year):
    """Проверка и очистка года выпуска"""
    if pd.isna(graduation_year) or not graduation_year:
        return False
    
    try:
        graduation_year = int(graduation_year)
        if graduation_year < 1900 or graduation_year > 2025:  # Исправлено условие с and на or
            return False
        return graduation_year
    except ValueError:
        return False

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

        'Образование (название ВУЗа)': 'university_name_ru',
        'Таҳсилот (номи расмии Донишгоҳ)': 'university_name_tg',
        'Город,ВУЗа': 'university_city_ru',
        'Шаҳри Донишгоҳ': 'university_city_tg',
        'СтранаВУЗа': 'university_country_ru',
        'Кишвари Донишгоҳ': 'university_country_tg',
        'Год выпуска (окончания) ВУЗа': 'graduation_year',

        'Профессиональный стаж работы в здравоохранении (количество лет)': 'experience_level',
        'Специализация по лечебному профилю': 'specialty_ru',
        'Ихтисос ё самти фаъолият (специализация)': 'specialty_tg',
        'Медицинская категория': 'medical_category',
        'Унвони илмӣ ва номзадӣ': 'academic_degree',
        'Заслуги и награды (Отличник здравоохранения, член-корреспондент Академии медицинских наук, почётный врач и т.д.)': 'title_and_merits_ru',
        'Унвонҳо ва мукофотҳо (Аълочии тандурустӣ, аъзои Академияи илмҳои тиб ва ғайра). Ҳама намуди унвонҳои доштаатонро дарҷ намоед.': 'title_and_merits_tg',
        'Напишите коротко о себе (информация, которая будет доступна пациентам)': 'about_ru',
        'Дар бораи худ мухтасар нависед (маълумоте, ки барои беморон дастрас мешавад)': 'about_tg',
        'Перечислите три Ваши сильные стороны в работе с пациентами': 'strength_ru',
        'Лутфан, се ҷиҳати (хусусияти) қавии худро дар вақти муносибат ва корбарӣ бо беморон, номбар кунед.': 'strength_tg',

        'Выберете название своего медицинского учреждения': 'clinic_name_ru',
        'Номи муассисаи тиббии худро интихоб кунед': 'clinic_name_tg',
        'Напишите свою текущую должность': 'position_ru',
        'Вазифаи ҳозираи худро ба пуррагӣ нависед.': 'position_tg',

        'Таджикский': 'lang_tg',
        'Русский': 'lang_ru',
        'Узбекский': 'lang_uz',
        'Английский': 'lang_en',
        'Кыргызский': 'lang_kg',
        'Немецкий': 'lang_dt',
        'Хинди': 'lang_in',
        'Турецкий': 'lang_tr',

        'Индивидуальная консультация (на своем рабочем месте)': 'Индивидуальная консультация;2',
        'Онлайн консультация': 'Индивидуальная консультация;3',
        'Консультация с выездом к пациенту': 'Индивидуальная консультация;1',
        'Консультация в ночное время': 'Консультация в ночное время;3',
        'Консультация в выходные и праздничные дни': 'Консультация в выходные и праздничные дни;2',
        'Выдача рецепта': 'Выдача рецепта;2'
        }
    
    service_list = ['Индивидуальная консультация;2', 'Индивидуальная консультация;3', 'Индивидуальная консультация;1',
                    'Консультация в ночное время;3', 'Консультация в выходные и праздничные дни;2', 'Выдача рецепта;2']

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "sughd_db.xlsx")
        error_rows = []  # Список для хранения строк с ошибками
        error_indices = []  # Список для хранения индексов строк с ошибками
        error_reasons = []  # Список для хранения причин ошибок

        try:
            # Чтение и переименование столбцов
            df = pd.read_excel(file_path, usecols=self.COLUMN_MAPPING.keys(), dtype=str)
            df.rename(columns=self.COLUMN_MAPPING, inplace=True)
        
            # Счетчики
            created_doctors = 0
            created_specialties = 0
            created_clinics = 0
            created_workplaces = 0
            created_universities = 0
            created_educations = 0
            errors = 0
            not_processed = 0
            
            for index, row in df.iterrows():
                try:
                    email = row['email'] if row['email'] != '-' or '' else None
                    phone_number = clean_phone(row.get('work_phone_number'))
                    if not phone_number:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверный номер телефона")
                        continue

                    # 2. Проверка даты рождения
                    date_of_birth = clean_date(row.get('date_of_birth'))
                    if not date_of_birth:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверная дата рождения")
                        continue
                    date_of_birth = datetime.strptime(row['date_of_birth'], "%d/%m/%Y").date()

                    # 3. Проверка ИНН
                    inn = clean_inn(row.get('inn'))
                    if inn is False:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверный ИНН")
                        continue

                    # Проверка существования пользователя
                    if user_exists(phone_number=phone_number, inn=inn, email=row.get('email')):
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Пользователь уже существует")
                        continue

                    first_name = row['first_name_tg'] if pd.isna(row['first_name_ru']) or row['first_name_ru'] == '' else row['first_name_ru']
                    last_name = row['last_name_tg'] if pd.isna(row['last_name_ru']) or row['last_name_ru'] == '' else row['last_name_tg']
                    middle_name = row['middle_name_tg'] if pd.isna(row['middle_name_ru']) or row['middle_name_ru'] == '' else row['middle_name_tg']
                    
                    try:
                        gender = Gender.objects.get(name_ru=row['gender']) 
                    except Gender.DoesNotExist:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверный пол")
                        continue
                    
                    try:
                        district = District.objects.get(name_ru=row['district']) 
                    except District.DoesNotExist:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверный район")
                        continue

                    clinic_type = ClinicType.objects.get(id=1)                
                    try:
                        experience_level = ExperienceLevel.objects.get(level_ru=row['experience_level'])
                    except ExperienceLevel.DoesNotExist:
                        not_processed += 1
                        error_rows.append(row)
                        error_indices.append(index)
                        error_reasons.append("Неверный уровень опыта")
                        continue

                    clinic = Clinic.objects.filter(
                        Q(name_ru=row['clinic_name_ru']) | 
                        Q(name_tg=row['clinic_name_tg'])
                    ).first()
                    if not clinic:
                        clinic = Clinic.objects.create(
                            clinic_type=clinic_type,
                            name_ru=row['clinic_name_ru'], 
                            name_tg=row['clinic_name_tg'],
                            district=district,
                            address_ru="Пока без адреса..."
                            )
                        created_clinics += 1

                    university = University.objects.filter(
                        Q(name_ru=row['university_name_ru']) | 
                        Q(name_tg=row['university_name_tg'])
                    ).first()

                    if not university:
                        university = University.objects.create(
                            name=row['university_name_ru'],
                            name_ru=row['university_name_ru'],
                            name_tg=row['university_name_tg'],
                            city=row['university_city_ru'],
                            city_ru=row['university_city_ru'],
                            city_tg=row['university_city_tg'],
                            country=row['university_country_ru'],
                            country_ru=row['university_country_ru'],
                            country_tg=row['university_country_tg']
                            )
                        
                        created_universities += 1
                    
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
                        
                    if user_created and (user.first_name == row['first_name_ru'] or user.first_name == row['first_name_tg']):
                        whatsapp = clean_phone(row.get('whatsapp'))
                        work_phone_number = clean_phone(row.get('work_phone_number'))
                        doctor, doctor_created = Doctor.objects.get_or_create(
                            user=user,
                            experience_level=experience_level,
                            work_phone_number=work_phone_number,
                            whatsapp=whatsapp,
                            telegram=row['telegram'] if row['telegram'] != '-' or '' else None,
                        )
                        
                        if doctor_created:
                            created_doctors += 1

                        specialty, specialty_created = Specialty.objects.get_or_create(
                            name_tg=row['specialty_tg'],
                            name_ru=row['specialty_ru']
                        )

                        if specialty_created:
                            created_specialties += 1

                        doctor.specialties.add(specialty)

                        medical_category_name = row['medical_category']
                        if pd.notna(medical_category_name) and medical_category_name != 'Нет категории':
                            try:
                                medical_category = MedicalCategory.objects.get(name_ru=medical_category_name)
                            except MedicalCategory.DoesNotExist:
                                medical_category = None
                        else:
                            medical_category = None

                        academic_degree_name = row['academic_degree']
                        if pd.notna(academic_degree_name) and academic_degree_name != 'надорам;':
                            try:
                                academic_degree_name, _ = academic_degree_name.split(';')
                                academic_degree = AcademicDegree.objects.get(name_tg=academic_degree_name)
                            except (ValueError, AcademicDegree.DoesNotExist):
                                academic_degree = None
                        else:
                            academic_degree = None

                        if pd.notna(row['title_and_merits_ru']):
                            doctor.titles_and_merits_ru=row['title_and_merits_ru']
                        elif pd.notna(row['title_and_merits_tg']):
                            doctor.titles_and_merits_tg=row['title_and_merits_tg']

                        # Инициализируем переменные
                        about_ru = ""
                        about_tg = ""

                        if pd.notna(row.get('about_ru')):
                            about_ru = str(row['about_ru'])
                        elif pd.notna(row.get('about_tg')):
                            about_tg = str(row['about_tg'])

                        strength_ru = row.get('strength_ru')
                        strength_tg = row.get('strength_tg')

                        if pd.notna(strength_ru):
                            about_ru += f"\n\nМои сильные стороны: {strength_ru}" if about_ru else f"Мои сильные стороны: {strength_ru}"
                        elif pd.notna(strength_tg):
                            about_tg += f"\n\nҚувваҳои ман: {strength_tg}" if about_tg else f"Қувваҳои ман: {strength_tg}"

                        if about_ru:
                            doctor.about_ru = about_ru.strip()
                        if about_tg:
                            doctor.about_tg = about_tg.strip()
                        
                        doctor.medical_category = medical_category
                        doctor.academic_degree = academic_degree
                        doctor.save()

                    if doctor.user.first_name == row['first_name_ru'] or doctor.user.first_name == row['first_name_tg']:
                        if pd.notna(row['lang_tg']):
                            try:
                                language = Language.objects.get(name_ru='Таджикский')
                                level = LanguageLevel.objects.get(level_ru=row['lang_tg'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_ru']):
                            try:
                                language = Language.objects.get(name_ru='Русский')
                                level = LanguageLevel.objects.get(level_ru=row['lang_ru'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_uz']):
                            try:
                                language = Language.objects.get(name_ru='Узбекский')
                                level = LanguageLevel.objects.get(level_ru=row['lang_uz'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_en']):
                            try:
                                language = Language.objects.get(name_ru='Английский')
                                level = LanguageLevel.objects.get(level_ru=row['lang_en'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_kg']):
                            try:
                                language = Language.objects.get(name_ru='Кыргызский')
                                level = LanguageLevel.objects.get(level_ru=row['lang_kg'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_dt']):
                            try:
                                language = Language.objects.get(name_ru='Немецкий')
                                level = LanguageLevel.objects.get(level_ru=row['lang_dt'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_in']):
                            try:
                                language = Language.objects.get(name_ru='Хинди')
                                level = LanguageLevel.objects.get(level_ru=row['lang_in'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass
                        if pd.notna(row['lang_tr']):
                            try:
                                language = Language.objects.get(name_ru="Турецкий")
                                level = LanguageLevel.objects.get(level_ru=row['lang_tr'])
                                DoctorLanguage.objects.create(doctor=doctor, language=language, level=level)
                            except (Language.DoesNotExist, LanguageLevel.DoesNotExist):
                                pass

                    for s in self.service_list:
                        service_name, service_place = s.split(';')
                        service_place = ServicePlace.objects.get(id=int(service_place))
                        service = Service.objects.get(service_place=service_place, name_ru=service_name)
                        if row[s] == 'Да':
                            doctor.services.add(service)

                    workplace, workplace_created = Workplace.objects.get_or_create(
                        doctor=doctor, 
                        clinic=clinic, 
                        position_ru=row['position_ru'], 
                        position_tg=row['position_tg']
                        )
                    
                    if workplace_created:
                        created_workplaces += 1

                    graduation_year = clean_graduation_year(row.get('graduation_year'))
                    if graduation_year:
                        education, education_created = Education.objects.get_or_create(
                            doctor=doctor,
                            university=university,
                            graduation_year=graduation_year
                        )

                        if education_created:
                            created_educations += 1

                except Exception as e:
                    errors += 1
                    error_rows.append(row)
                    error_indices.append(index)
                    error_reasons.append(str(e))
                    self.stdout.write(self.style.ERROR(f'{errors-1}. Error processing row {index}: {str(e)}'))
                    continue
            
            # Сохраняем ошибки в Excel файл
            if error_rows:
                error_df = pd.DataFrame(error_rows)
                error_df['Оригинальный индекс'] = error_indices
                error_df['Причина ошибки'] = error_reasons
                
                # Восстанавливаем оригинальные названия столбцов
                reverse_mapping = {v: k for k, v in self.COLUMN_MAPPING.items()}
                error_df.rename(columns=reverse_mapping, inplace=True)
                
                error_file_path = os.path.join(settings.BASE_DIR, "import_errors.xlsx")
                error_df.to_excel(error_file_path, index=False)
                self.stdout.write(self.style.WARNING(f'Файл с ошибками сохранен: {error_file_path}'))

            self.stdout.write(self.style.SUCCESS(
                f'Import completed. Created: {created_doctors} doctors, {created_clinics} clinics, {created_workplaces} workplaces, {created_universities} universities, {created_educations} educations, {created_specialties} specialties. Errors: {errors}, Not Processed: {not_processed}'
            ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading file: {str(e)}'))