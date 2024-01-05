from django.contrib import admin
from django.contrib import messages
from django.contrib.messages.storage import default_storage
from django import forms

from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.http import HttpResponseRedirect

from . import models
from asgiref.sync import async_to_sync

import zipfile
from django.core.files import File
# Register your models here.

class UploadForm(forms.ModelForm):
	archive = forms.FileField(label=_('Archive'))

	class Meta:
		model = models.UserBot
		fields = '__all__'

	def clean_archive(self):
		if not '.zip' in self.cleaned_data['archive'].name:
			raise forms.ValidationError('Разрешенные расширения: zip.')
		return self.cleaned_data['archive']

@admin.register(models.UserBot)
class UserBotAdmin(admin.ModelAdmin):
	show_facets = admin.ShowFacets.ALWAYS

	actions = ['validate']
	list_display = ['_str', 'tg_id', 'country', '_status', 'created_date', 'free']
	list_filter = ['status', 'free']
	change_list_template = 'admin/userbot/change_list.html'

	def _str(self, obj):
		return format_html(str(obj))
	_str.short_description = ''

	def _status(self, obj):
		style = ''

		match obj.status:
			case 'active':
				style = 'color: green;'

			case 'deactivated':
				style = 'color: red;'

		return format_html(f'<span style="{style}">{obj.get_status_display()}</span>')
	_status.short_description = _('Status')

	def response_change(self, request, obj):
		if '_check-valid' in request.POST:
			obj.validation()
			return HttpResponseRedirect('.')

		return super().response_change(request, obj)

	def response_add(self, request, obj, post_url_continue=None):
		if '_upload' in request.POST:
			return HttpResponseRedirect('/admin/bots/userbot/')

		return super().response_add(request, obj, post_url_continue)

	def save_model(self, request, obj, form, change):
		if '_upload' in request.POST:
			# Write parse zip code here.
			archive = request.FILES['archive']
			country = form.cleaned_data['country']
			count = 0
			with zipfile.ZipFile(archive, 'r') as zip_file:
				for file in zip_file.namelist():
					if '.session' in file and 'MACOSX' not in file:
						with zip_file.open(file, 'r') as session:
							session_file = File(session)
							userbot = models.UserBot.objects.create(session=session_file, country=country)
							count += 1

			messages.add_message(request, messages.INFO, f'Ботов добавлено: {count}')

			return None

		return super().save_model(request, obj, form, change)

	def add_view(self, request, extra_context=None):
		if request.GET.get('upload', default=0):
			self.form = UploadForm
			self.change_form_template = 'admin/userbot/upload_form.html'
			self.fieldsets = (
				('', {'fields': ('archive', 'country', )}),
			)
			return super().add_view(request, extra_context)

		self.form = super().form
		self.change_form_template = super().change_form_template
		self.fieldsets = (
			('', {'fields': ('session', 'country', )}),
		)
		self.readonly_fields = []
		return super().add_view(request, extra_context)

	def change_view(self, request, object_id, extra_context=None):
		self.form = super().form
		self.change_form_template = 'admin/userbot/change_form.html'
		obj = models.UserBot.objects.get(id=object_id)

		fields = ['tg_id', 'session', 'country', 'free', '_status', 'created_date', 'updated_date']
		if obj.status == 'flood_ban':
			fields.append('unban_date')

		self.fieldsets = (
			('', {'fields': tuple(fields)}),
		)
		self.readonly_fields = fields
		return super().change_view(request, object_id, extra_context)

	@admin.action(description=_('Validate selected'))
	def validate(modeladmin, request, queryset):
		for userbot in queryset:
			userbot.validation()

		messages.add_message(request, messages.INFO, _('Validate completed'))








