from django.urls import path
from . import views


urlpatterns = [
	path('log-list/<int:task_id>/', views.log_list),
	path('bots-banned/<int:task_id>/', views.bots_banned),
]