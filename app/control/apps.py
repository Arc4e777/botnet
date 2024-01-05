from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control'
    verbose_name = _('Control')