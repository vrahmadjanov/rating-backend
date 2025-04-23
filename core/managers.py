from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, password=None, is_active=True, **extra_fields):
        """Создает и сохраняет пользователя"""
        if not phone_number:
            raise ValueError('Пользователь должен иметь номер телефона')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            password=password,
            **extra_fields
        )