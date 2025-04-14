from django.urls import path, include
from blog import views

app_name = "blog"

urlpatterns = [
    path('create-post/', views.create_blog_post, name='create-post')
]
