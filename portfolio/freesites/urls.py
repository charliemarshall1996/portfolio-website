
from django.urls import path

from . import views

app_name = "freesites"

urlpatterns = [
    path("", views.home_view, name="home"),
    path('inquiry/', views.submit_inquiry, name='inquiry'),
    path('queue/<uuid:code>', views.queue_status, name='queue'),
    path('queue-full/', views.queue_full, name='queue_full'),
    path('queue-list/', views.queue_list, name='queue_list'),
    path('completed/', views.completed_list, name='completed_list'),
    path('complete/<int:inquiry_id>/',
         views.complete_inquiry, name='complete_inquiry'),
    path('in_progress/<int:inquiry_id>/',
         views.in_progress_inquiry, name='in_progress_inquiry'),
]
