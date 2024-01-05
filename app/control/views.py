from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from django.http import HttpResponse

from .models import Task
# Create your views here.

@staff_member_required
@never_cache
def log_list(request, task_id):
	with open(f'logs/logs-{task_id}.log', 'r') as file:
		lines = file.readlines()[::-1]
		return HttpResponse('\n'.join(lines[:50]))
		# return HttpResponse('\n'.join(file.readlines()))

@staff_member_required
def bots_banned(request, task_id):
	task = Task.objects.get(id=task_id)
	return HttpResponse(str(task.bots_banned))