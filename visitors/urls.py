from django import urls
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'visitors', views.VisitorViewSet)

urlpatterns = [
    urls.path('api/', urls.include(router.urls)),
]
