from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.http import HttpResponseRedirect

from . import models
from bots.models import UserBot
from django import forms

from rq.worker import Worker
import django_rq
# Register your models here.

class ActionInline(admin.TabularInline):
	extra = 0
	model = models.Action

class TaskForm(forms.ModelForm):
	bots_count = forms.IntegerField(label=_('Bots count'))

	class Meta:
		model = models.Task
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.available_bots = UserBot.objects.available()
		self.fields['bots_count'].help_text = f'Доступно: {self.available_bots.count()}'

	def clean_bots_count(self):
		if self.cleaned_data['bots_count'] and self.cleaned_data['bots_count'] > self.available_bots.count():
			raise forms.ValidationError(_('Bots count > available bots'))
		return self.cleaned_data['bots_count']

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ['_str', 'target', 'in_process']
	form = TaskForm
	change_form_template = 'admin/task/change_form.html'

	def _str(self, obj):
		return format_html(str(obj))
	_str.short_description = ''

	def _bots_count(self, obj):
		return format_html(str(obj.bots.all().count()))
	_bots_count.short_description = _('Bots count')

	def _bots_banned(self, obj):
		return format_html(f'<span style="color: red;" hx-get="/control/bots-banned/{obj.id}/" hx-trigger="load, every 2s"></span>')
	_bots_banned.short_description = _('Bots banned')

	def add_view(self, request, extra_context=None):
		self.fieldsets = (
			('', {'fields': ('target', 'bots_count', )}),
		)
		self.inlines = [ActionInline]
		self.readonly_fields = []
		self.form.base_fields['bots_count'].initial = None
		self.form.base_fields['bots_count'].required = True
		return super().add_view(request, extra_context=extra_context)

	def save_model(self, request, obj, form, change):
		obj.save()
		if not obj.in_process:
			obj.bots.set(form.available_bots[:form.cleaned_data['bots_count']])

	def change_view(self, request, object_id, extra_context=None):
		obj = models.Task.objects.get(id=object_id)
		extra_context = extra_context or {}
		extra_context['task'] = obj

		self.form.base_fields['bots_count'].initial = obj.bots.count()

		if obj.in_process:
			self.form.base_fields['bots_count'].required = False
			self.fieldsets = (
				(_('Settings'), {'fields': ('target', '_bots_count', )}),
				(_('Results'), {'fields': ('in_process', '_bots_banned', 'start_date', )})
			)
			self.readonly_fields = ['in_process', '_bots_count', 'target', '_bots_banned', 'start_date']
			self.inlines = []
		else:
			self.form.base_fields['bots_count'].required = True
			self.fieldsets = (
				(_('Settings'), {'fields': ('target', 'bots_count', )}),
				(_('Results'), {'fields': ('in_process', )})
			)
			self.readonly_fields = ['in_process']
			self.inlines = [ActionInline]

		return super().change_view(request, object_id, extra_context=extra_context)

	def response_change(self, request, obj):
		if '_start' in request.POST:
			obj.save()
			if obj.get_actions().count() == 0:
				messages.error(request, 'Task dont have actions!')
				return HttpResponseRedirect('.')

			queue = django_rq.get_queue('default')
			workers = Worker.count(queue=queue)
			active_tasks = models.Task.objects.filter(in_process=True)
			if active_tasks.count() >= workers:
				messages.error(request, _('No available workers !'))
				return HttpResponseRedirect('.')

			obj.start()
			messages.success(request, 'Task started!')
			return HttpResponseRedirect('.')

		if '_stop' in request.POST:
			obj.stop()
			messages.warning(request, 'Task stopped!')
			return HttpResponseRedirect('.')

		return super().response_change(request, obj)

	def delete_queryset(self, request, queryset):
		for task in queryset:
			if not task.in_process:
				task.delete()
			else:
				messages.error(request, str(_('Error with deletion')) + f' {task}: ' + str(_('Task in process!')))

@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ['_str', 'target', '_duration']
	list_filter = ['target']
	show_facets = admin.ShowFacets.ALWAYS

	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def _str(self, obj):
		return format_html(str(obj))
	_str.short_description = ''

	def _duration(self, obj):
		return format_html(str((obj.end_date - obj.start_date).seconds) + ' сек.')
	_duration.short_description = _('Duration')

	def _bots_banned(self, obj):
		return format_html(f'<span style="color: red;">{obj.bots_banned}</span>')
	_bots_banned.short_description = _('Bots banned')

	fieldsets = (
		('', {'fields': ('target', 'actions', 'bots_count', '_bots_banned', '_duration', 'start_date', 'end_date')}),
	)













