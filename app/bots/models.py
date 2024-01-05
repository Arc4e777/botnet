from django.db import models
from .data import COUNTRY_CHOICES

from django.core.validators import FileExtensionValidator
from django.core.files.storage import FileSystemStorage

from django.utils.translation import gettext_lazy as _

from django.conf import settings

from pyrogram import Client
from asgiref.sync import async_to_sync

import requests, random
# Create your models here.

SESSION_STORAGE = FileSystemStorage(location=settings.BOT_SESSION_ROOT)

class UserBotQuerySet(models.QuerySet):
	def available(self):
		return self.filter(status='active', free=True, country='ID')

class UserBot(models.Model):
	objects = UserBotQuerySet.as_manager()
	STATUS_CHOICES = (
		('active', _('Active')),
		('deactivated', _('Deactivated')),
	)

	tg_id = models.BigIntegerField(null=True, blank=True, verbose_name=_('TG ID'))
	session = models.FileField(
		storage=SESSION_STORAGE,
		validators=[FileExtensionValidator(allowed_extensions=['session'])],
		verbose_name=_('Session'),
		unique=True
	)
	country = models.CharField(
		choices=COUNTRY_CHOICES,
		max_length=200,
		verbose_name=_('Country')
	)
	proxy = models.JSONField(null=True, blank=True, verbose_name=_('Proxy'))
	proxy_string = models.CharField(null=True, blank=True, verbose_name=_('Proxy string'))

	created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))
	updated_date = models.DateTimeField(auto_now=True, verbose_name=_('Updated date'))

	free = models.BooleanField(default=True, verbose_name=_('Free'))
	status = models.CharField(
		max_length=50,
		choices=STATUS_CHOICES,
		default='active',
		verbose_name=_('Status')
	)

	class Meta:
		verbose_name = _('Userbot')
		verbose_name_plural = _('Userbots')

	def __str__(self):
		return f'{_("Userbot")} #{self.id}'

	@property
	def name(self):
		return self.session.path.replace('.session', '')

	async def is_valid(self):
		client = Client(self.name, settings.APP_ID, settings.APP_HASH, proxy=proxy)
		await client.connect()

		try:
			me = await client.get_me()
			await client.disconnect()
			return True, me.id
		except Exception as e:
			print(e, flush=True)
			return False, self.tg_id
	
	def validation(self):
		is_valid, tg_id = async_to_sync(self.is_valid)()

		if is_valid:
			status = 'active'
		else:
			status = 'deactivated'

		UserBot.objects.filter(id=self.id).update(status=status, tg_id=tg_id)

	def save(self, *args, **kwargs):
		if not self.session:
			return

		super().save(*args, **kwargs)

	async def send_message(self, target, message):
		async with Client(self.name, settings.APP_ID, settings.APP_HASH, proxy=proxy) as app:
			await app.send_message(target.replace('@', ''), message)









