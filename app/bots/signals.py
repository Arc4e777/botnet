from .models import UserBot

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import os


@receiver(post_save, sender=UserBot, weak=False)
def post_create_validation(sender, instance, created, **kwargs):
	if instance.id and created:
		instance.validation()

@receiver(post_delete, sender=UserBot, weak=False)
def delete_session(sender, instance, **kwargs):
	if os.path.isfile(instance.session.path):
		os.remove(instance.session.path)