from django.urls import path

from . import views

app_name = "scrapers"


urlpatterns = [
    path("api/searchparameter/<int:pk>/",
         views.SearchParameterView.as_view(), name="searchparameter-update"),
    path("api/searchparameter/<str:directory>/",
         views.SearchParameterView.as_view(), name="searchparameter-get"),
]
