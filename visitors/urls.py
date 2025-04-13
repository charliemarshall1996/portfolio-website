from django import urls
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'visitors', views.VisitorViewSet)

urlpatterns = [
    urls.path('api/', urls.include(router.urls)),
    urls.path('api/visitors/stats/',
              views.VisitorViewSet.as_view({'get': 'stats'}), name='visitor-stats'),
]
