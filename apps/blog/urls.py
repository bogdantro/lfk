from django.urls import path
from .views import (
    blog, blog_post, blog_create, blog_edit, blog_trash, blog_restore, blog_delete_permanent,
    dashboard_blog_list, dashboard_blog_trash,
)

urlpatterns = [
    path('nyheter/', blog, name='blog'),
    path('nyheter/ny/', blog_create, name='blog_create'),

    # Dashboard
    path('dashboard/nyheter/', dashboard_blog_list, name='dashboard_blog_list'),
    path('dashboard/nyheter/papirkurv/', dashboard_blog_trash, name='dashboard_blog_trash'),
    path('dashboard/nyheter/<int:pk>/rediger/', blog_edit, name='blog_edit'),
    path('dashboard/nyheter/<int:pk>/slett/', blog_trash, name='blog_trash'),
    path('dashboard/nyheter/<int:pk>/gjenopprett/', blog_restore, name='blog_restore'),
    path('dashboard/nyheter/<int:pk>/slett-permanent/', blog_delete_permanent, name='blog_delete_permanent'),

    path('<str:slug>-<int:id>/', blog_post, name='blog_post'),
]
