from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Application, StatusHistory


@receiver(pre_save, sender=Application)
def cache_previous_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._previous_status = Application.objects.get(pk=instance.pk).status
        except Application.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Application)
def create_status_history_on_change(sender, instance, created, **kwargs):
    if not created:
        old_status = getattr(instance, "_previous_status", None)
        if old_status and old_status != instance.status:
            StatusHistory.objects.create(
                application=instance,
                from_status=old_status,
                to_status=instance.status,
            )
