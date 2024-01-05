"""
WSGI config for botnet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botnet.settings')

application = get_wsgi_application()

from control.models import Task
for task in Task.objects.filter(in_process=True):
	task.stop()