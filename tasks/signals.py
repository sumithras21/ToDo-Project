from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Tasks

@receiver(post_save, sender=Tasks)
def task_saved(sender, instance, created, **kwargs):
    if created:
        print("Task Created:", instance.title)
    else:
        print("Task Updated:", instance.title)

@receiver(pre_delete, sender=Tasks)
def task_deleted(sender, instance, **kwargs):
    print("Task Deleted:", instance.title)