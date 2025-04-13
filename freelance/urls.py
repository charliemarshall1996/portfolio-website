"""
URL configuration for freelance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os.path

from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    # Add explicit paths BEFORE Wagtail's catch-all
    re_path("visitors/", include("visitors.urls")),
    re_path("blog/", include("blog.urls")),
    re_path("booking/", include("booking.urls")),

    # Wagtail catch-all should come LAST
    path('', include(wagtail_urls)),
    re_path("", include("home.urls")),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # tell gunicorn where static files are in dev mode
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += [
        path('favicon.ico', RedirectView.as_view(
            url=settings.STATIC_URL + 'myapp/images/favicon.ico'))
    ]
