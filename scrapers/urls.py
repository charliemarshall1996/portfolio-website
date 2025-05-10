from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("api/get-oldest-searchparameter/",
         views.get_oldest_searchparameter, name="get_oldest_searchparameter"),
]
