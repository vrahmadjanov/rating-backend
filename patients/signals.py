from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Patient

@receiver(post_save, sender=Patient)
def add_doctor_to_group(sender, instance, created, **kwargs):
    """
    При создании пациента автоматически добавляет его в группу 'Пациент'.
    """
    if created and instance.user:
        group, _ = Group.objects.get_or_create(name="Пациент")
        instance.user.groups.add(group)

