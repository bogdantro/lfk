from django.urls import path
from .views import blog, blog_post, blog_create

urlpatterns = [
    path('nyheter/', blog, name='blog'),
    path('nyheter/ny/', blog_create, name='blog_create'),
    path('<str:slug>-<int:id>/', blog_post, name='blog_post'),
]
