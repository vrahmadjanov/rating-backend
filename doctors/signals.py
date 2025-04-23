from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Doctor

@receiver(post_save, sender=Doctor)
def add_doctor_to_group(sender, instance, created, **kwargs):
    """
    При создании врача автоматически добавляет его в группу 'Doctors'.
    """
    if created and instance.user:
        group, _ = Group.objects.get_or_create(name="Doctors")
        instance.user.groups.add(group)

