from django.urls import path
from .views import (
    blog, blog_post, blog_create, blog_edit, blog_trash, blog_restore, blog_delete_permanent,
    dashboard_blog_list, dashboard_blog_trash,
)

DASHBOARD = 'lfk/kundebruker/secure/login/'

urlpatterns = [
    path('nyheter/', blog, name='blog'),
    path('nyheter/ny/', blog_create, name='blog_create'),

    # Dashboard – under the staff dashboard's own address (the "myaccount" page),
    # which the club's admins already have bookmarked.
    path(f'{DASHBOARD}nyheter/', dashboard_blog_list, name='dashboard_blog_list'),
    path(f'{DASHBOARD}nyheter/papirkurv/', dashboard_blog_trash, name='dashboard_blog_trash'),
    path(f'{DASHBOARD}nyheter/<int:pk>/rediger/', blog_edit, name='blog_edit'),
    path(f'{DASHBOARD}nyheter/<int:pk>/slett/', blog_trash, name='blog_trash'),
    path(f'{DASHBOARD}nyheter/<int:pk>/gjenopprett/', blog_restore, name='blog_restore'),
    path(f'{DASHBOARD}nyheter/<int:pk>/slett-permanent/', blog_delete_permanent, name='blog_delete_permanent'),

    path('<str:slug>-<int:id>/', blog_post, name='blog_post'),
]
