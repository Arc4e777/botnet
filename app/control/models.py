from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from bots.models import UserBot
import django_rq
import asyncio, random
from pyrogram.errors import FloodWait, Unauthorized
# Create your models here.

class Task(models.Model):
	target = models.CharField(max_length=200, verbose_name=_('Target'))
	bots = models.ManyToManyField(UserBot)

	in_process = models.BooleanField(default=False)
	bots_banned = models.IntegerField(default=0, verbose_name=_('Bots banned'))
	start_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Start date'))

	SUCCESS_SEND_MESSAGE = _("send message")
	FLOOD_BAN_MESSAGE = _("flood ban for")
	BAN_MESSAGE = _("banned")
	SLEEP_MESSAGE = _("sleep for")

	class Meta:
		verbose_name = _('Task')
		verbose_name_plural = _('Tasks')

	def __str__(self):
		return f'{_("Task")} #{self.id}'

	def get_actions(self):
		return Action.objects.filter(task=self)

	async def do_actions(self, bot, actions):
		while True:
			async for action in actions:
				sleep_time = random.randint(3, 7)

				try:
					await bot.send_message(self.target, action.message)
					result = f'<span style="color: green;">{bot} {Task.SUCCESS_SEND_MESSAGE}</span>'
				except FloodWait as e:
					result = f'<span style="color: yellow;">{bot} {Task.FLOOD_BAN_MESSAGE} {e.value}с</span>'
					sleep_time += e.value
				except Unauthorized:
					self.bots_banned += 1
					bot.status = 'deactivated'
					await bot.asave()
					await self.asave()

					sleep_time = 0
					result = f'<span style="color: red;">{bot} {Task.BAN_MESSAGE}!</span>'

				log = f'<div class="output-cmd">{result}, {Task.SLEEP_MESSAGE} {sleep_time}с</div>'
				with open(f'logs/logs-{self.id}.log', 'a') as file:
					file.write(log)

				if bot.status == 'deactivated':
					return
				else:
					await asyncio.sleep(sleep_time)

	async def create_threads(self):
		actions = self.get_actions()
		await asyncio.gather(*[self.do_actions(bot, actions) async for bot in self.bots.all()])

	def start(self):
		self.in_process = True
		self.bots_banned = 0
		self.start_date = timezone.now()
		self.save()
		self.bots.all().update(free=False)

		with open(f'logs/logs-{self.id}.log', 'w') as file:
			file.write('---start---')

		queue = django_rq.get_queue('default', is_async=True, default_timeout=-1)
		queue.enqueue(self.create_threads, job_id=str(self))

	def stop(self):
		actions = ' --> '.join([action.message for action in self.get_actions()])
		result = Result.objects.create(
			target=self.target,
			bots_count=self.bots.count(),
			bots_banned=self.bots_banned,

			start_date=self.start_date,
			end_date=timezone.now(),
			actions=actions
		)

		self.in_process = False
		self.bots_banned = 0
		self.start_date = None
		self.save()
		self.bots.all().update(free=True)

		queue = django_rq.get_queue('default', is_async=True, default_timeout=-1)
		django_rq.utils.stop_jobs(queue, [str(self)])


class Action(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('Task'))

	message = models.CharField(max_length=200, verbose_name=_('Message'))

	class Meta:
		verbose_name = _('Action')
		verbose_name_plural = _('Actions')

	def __str__(self):
		return str(_('Action'))


class Result(models.Model):
	target = models.CharField(max_length=200, verbose_name=_('Target'))
	bots_count = models.IntegerField(verbose_name=_('Bots count'))
	bots_banned = models.IntegerField(verbose_name=_('Bots banned'))

	start_date = models.DateTimeField(verbose_name=_('Start date'))
	end_date = models.DateTimeField(verbose_name=_('End date'))
	actions = models.TextField(verbose_name=_('Actions'))

	class Meta:
		verbose_name = _('Result')
		verbose_name_plural = _('Results')

	def __str__(self):
		return f'{_("Result")} #{self.id}'











