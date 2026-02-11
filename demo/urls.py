from django.urls import path, include
from apps.core.views import *
from django.conf.urls.static import *
from django.conf import *
from django.contrib import admin
from django.contrib.auth import views
from apps.blog.views import *
from apps.core.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views

from apps.userprofile.urls import *


urlpatterns = [
    path('lfk/admin/login/', admin.site.urls),
    path("", include("apps.userprofile.urls")),
    path('', include('apps.blog.urls')),


    path('', home, name='home'),

    # Sport
    path('lag/senior/', senior, name='senior'),
    path('lag/senior/herrer/', senior_herrer, name='senior_herrer'),
    path('lag/senior/kvinner/', senior_kvinner, name='senior_kvinner'),

    path('lag/wednesday-united/', wednesday_united, name='wednesday_united'),
    path('lag/ungdom/', ungdom, name='ungdom'),
    path('lag/barn/', barn, name='barn'),

    path('uefa-playmakers/', uefa_playmakers, name='uefa_playmakers'),
    path('landslagsskolen/', landslagsskolen, name='landslagsskolen'),
    path('fair-play/', fair_play, name='fair_play'),


    # Marked
    path('partnere/', vare_samarbeidspartnere, name='vare_samarbeidspartnere'),
    path('baerekraft/', baerekraft, name='baerekraft'),
    path('medlemsfordeler/', medlemsfordeler, name='medlemsfordeler'),
    path('grasrotandelen/', grasrotandelen, name='grasrotandelen'),
    path('la-stampa-magasin/', la_stampa_magasin, name='la_stampa_magasin'),
    path('stampapodden/', stampapodden, name='stampapodden'),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)