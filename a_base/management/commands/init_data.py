from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps


class Command(BaseCommand):
    help = 'Очищает базу данных и создает тестовые данные'

    def handle(self, *args, **kwargs):
        """Основной метод обработки команд"""
        self.clean_database()
        self.init_data()
        self.create_users()

    def clean_database(self):
        """Очищает всю базу данных"""
        self.stdout.write("Очистка базы данных...")
        
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                model.objects.all().delete()
                
        self.stdout.write(self.style.SUCCESS("База данных успешно очищена!"))

    def init_data(self):
        """Инициализирует исходные данные"""
        medical_fixtures = [
            ('groups.json', 'группы пользователей'),
            ('subscriptions.json', 'подписки'),
            ('districts.json', 'регионы и районы'),
            ('genders.json', 'полы'),
            ('languages.json', 'языки'),
            ('social_statuses.json', 'социальные статусы'),
            ('specialties.json', 'специализации'),
            ('clinics.json', 'клиники'),
            ('medical_categories.json', 'медицинские категории'),
            ('academic_degrees.json', 'ученые степени'),
            ('services.json', 'услуги'),
            ('experience_levels.json', 'уровни опыта'),
        ]

        for fixture, name in medical_fixtures:
            self._load_fixture_with_logging(
                f'a_base/fixtures/{fixture}',
                name
            )

    def create_users(self):
        """Создает пользовательские данные"""
        self._load_fixture_with_logging(
            'a_base/fixtures/staff.json',
            'персонал'
        )
        self._load_fixture_with_logging(
            'a_base/fixtures/doctors.json',
            'врачи'
        )
        self._load_fixture_with_logging(
            'a_base/fixtures/universities.json',
            'университетов'
        )
        self._load_fixture_with_logging(
            'a_base/fixtures/educations.json',
            'образования врачей'
        )
        self._load_fixture_with_logging(
            'a_base/fixtures/workplaces.json',
            'мест работы врачей'
        )
        self._load_fixture_with_logging(
            'a_base/fixtures/patients.json',
            'пациенты'
        )

    def _load_fixture_with_logging(self, fixture_path, data_name):
        """
        Универсальный метод для загрузки фикстур с логированием
        :param fixture_path: путь к файлу фикстуры
        :param data_name: название загружаемых данных
        """
        self.stdout.write(f"Создание {data_name}...")
        
        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(
                self.style.SUCCESS(f"{data_name.capitalize()} успешно загружены.")
            )
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке {data_name}: {str(e)}')
            )
            return False