from django.core.management.base import BaseCommand
from openpyxl import Workbook
from doctors.models import Doctor, DoctorLanguage, Workplace, Education
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Экспорт данных из базы в Excel файл'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            default='db_export.xlsx',
            help='Имя выходного файла (по умолчанию db_export.xlsx)'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        filepath = os.path.join(settings.BASE_DIR, filename)
        
        wb = Workbook()
        
        # Экспорт врачей
        self.export_doctors(wb)
        
        wb.save(filepath)
        self.stdout.write(self.style.SUCCESS(f'Данные успешно экспортированы в {filepath}'))

    def export_doctors(self, wb):
        """Экспорт данных о врачах"""
        ws = wb.create_sheet(title='Врачи', index=0)
        
        # Заголовки
        headers = [
            'ID', 'Фамилия', 'Имя', 'Отчество', 'Номер телефона', 'ИНН', 'Дата рождения', 'Область', 'Район проживания',
            'Пол', 'Специализации', 'Профессиональный опыт', 'Медицинская категория', 'Ученая степень',
            'Услуги, которые предоставляет врач', 'Номер лицензии',
            'Краткое описание деятельности врача и его качеств (рус)',
            'Краткое описание деятельности врача и его качеств (тадж)',
            'Рабочий телефон', 'Номер для связи в Whatsapp', 'Номер или никнейм для связи в Telegram',
            'Email', 'Заслуги и награды (рус)', 'Заслуги и награды (тадж)', 'Владение языками',
            'Места работы', 'Образование'
        ]
        ws.append(headers)
        
        # Данные
        for doctor in Doctor.objects.select_related('user', 'experience_level').prefetch_related('specialties', 'services'):
            specialties = ', '.join([s.name_ru for s in doctor.specialties.all()])
            services = ', '.join([s.name_ru for s in doctor.services.all()])
            languages = ', '.join([f'{l.language.name_ru} ({l.level.level_ru})' for l in DoctorLanguage.objects.filter(doctor=doctor)])
            workplaces = ', '.join([f'{w.clinic.name_ru} ({w.clinic.clinic_type.name_ru}) | {w.position_ru} | {w.position_tg}|' for w in Workplace.objects.filter(doctor=doctor)])
            educations = ', '.join([f'{e.university.name_ru}|{e.university.city_ru}| ({e.graduation_year})' for e in Education.objects.filter(doctor=doctor)])
            
            ws.append([
                doctor.id,
                doctor.user.last_name,
                doctor.user.first_name,
                doctor.user.middle_name,
                doctor.user.phone_number,
                doctor.user.inn,
                doctor.user.date_of_birth,
                doctor.user.district.region.name_ru,
                doctor.user.district.name_ru,
                doctor.user.gender.name_ru if doctor.user.gender else '',
                specialties,
                doctor.experience_level.level_ru if doctor.experience_level else '',
                doctor.medical_category.name_ru if doctor.medical_category else '',
                doctor.academic_degree.name_ru if doctor.academic_degree else '',
                services,
                doctor.license_number,
                doctor.about_ru,
                doctor.about_tg,
                doctor.work_phone_number,
                doctor.whatsapp,
                doctor.telegram,
                doctor.user.email,
                doctor.titles_and_merits_ru,
                doctor.titles_and_merits_tg,
                languages,
                workplaces,
                educations
            ])