from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bots'
    verbose_name = _('Bots')

    def ready(self):
        from . import signals