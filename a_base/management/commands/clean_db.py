from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Очищает базу данных для всех приложений'

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка базы данных для всех приложений...")
        for app_config in apps.get_app_configs():
            self.stdout.write(f"Обработка приложения: {app_config.verbose_name}")
            for model in app_config.get_models():
                self.stdout.write(f"Удаление всех объектов модели {model.__name__}...")
                model.objects.all().delete()