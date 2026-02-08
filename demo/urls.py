from django.urls import path
from apps.core.views import *
from django.conf.urls.static import *
from django.conf import *
from django.contrib import admin
from django.contrib.auth import views

from apps.core.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('lag/senior/', senior, name='senior'),
    path('lag/senior/herrer/', senior_herrer, name='senior_herrer'),
    path('lag/senior/kvinner/', senior_kvinner, name='senior_kvinner'),

    path('lag/wednesday-united/', wednesday_united, name='wednesday_united'),
    path('lag/ungdom/', ungdom, name='ungdom'),
    path('lag/barn/', barn, name='barn'),

    path('uefa-playmakers/', uefa_playmakers, name='uefa_playmakers'),
    path('landslagsskolen/', landslagsskolen, name='landslagsskolen'),
    path('fair-play/', fair_play, name='fair_play'),

    path('bli-med/', bli_med, name='bli_med'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)