from django.urls import path

from . import views

app_name = "scrapers"

urlpatterns = [
    path("api/get-oldest-searchparameter/",
         views.get_oldest_searchparameter, name="get_oldest_searchparameter"),
    path("api/update-searchparameter/",
         views.UpdateSearchRunView.as_view(), name="update-searchparameter")
]
