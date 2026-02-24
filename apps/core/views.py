import warnings
from urllib import *
from django.shortcuts import *

from django.shortcuts import *
from django.http import *
from django.core.mail import *
from django.contrib.auth import *
from django.template.loader import *
from textwrap import *
from django.views.decorators.csrf import *
from django.db.models import * 
from django.contrib.auth.decorators import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.blog.models import *


# Home
def home(request):
    posts = list(
        Blog.objects.filter(wordpress_id__isnull=True).order_by('-created_at', '-id')
    ) + list(
        Blog.objects.filter(wordpress_id__isnull=False).order_by('id')
    )

    return render(request, 'core/home.html', {
        'latest_blog': posts[0] if len(posts) > 0 else None,
        'second_latest_blog': posts[1] if len(posts) > 1 else None
    })

def xtravgs(request):
    return render(request, 'pages/xtravgs.html')

# Sport
def senior(request):
    return render(request, 'teams/senior.html')

def senior_herrer(request):
    return render(request, 'teams/senior-herrer.html')

def senior_kvinner(request):
    return render(request, 'teams/senior-kvinner.html')

def wednesday_united(request):
    return render(request, 'teams/wednesday-united.html')

def ungdom(request):
    return render(request, 'teams/ungdom.html')

def barn(request):
    return render(request, 'teams/barn.html')

def uefa_playmakers(request):
    return render(request, 'pages/uefa-playmakers.html')

def landslagsskolen(request):
    return render(request, 'pages/landslagsskolen.html')

def fair_play(request):
    return render(request, 'pages/fair-play.html')



# Marked
from django.shortcuts import render

def vare_samarbeidspartnere(request):
    return render(request, 'pages/vare-samarbeidspartnere.html')

def baerekraft(request):
    return render(request, 'pages/baerekraft.html')

def medlemsfordeler(request):
    return render(request, 'pages/medlemsfordeler.html')

def grasrotandelen(request):
    return render(request, 'pages/grasrotandelen.html')

def la_stampa_magasin(request):
    return render(request, 'pages/la-stampa-magasin.html')

def stampapodden(request):
    return render(request, 'pages/stampapodden.html')


# Arrangement
def tine_fotballskole(request):
    return render(request, 'pages/tine-fotballskole.html')

def thallaug_cup(request):
    return render(request, 'pages/thallaug-cup.html')

def kiwi_cup(request):
    return render(request, 'pages/kiwi-cup.html')


# Om klubben

def historie(request):
    return render(request, 'pages/about/historie.html')

def klubbhandbok(request):
    return render(request, 'pages/about/klubbhandbok.html')

def klubbkolleksjon(request):
    return render(request, 'pages/about/klubbkolleksjon.html')

def medlemskap(request):
    return render(request, 'pages/about/medlemskap.html')

def styret(request):
    return render(request, 'pages/about/styret.html')

def kontakt(request):
    return render(request, 'pages/about/kontakt.html')

def varsling(request):
    return render(request, 'pages/about/varsling.html')

def forsikring(request):
    return render(request, 'pages/about/forsikring.html')

def dommere(request):
    return render(request, 'pages/about/dommere.html')

def politiattest(request):
    return render(request, 'pages/about/politiattest.html')

def minibuss(request):
    return render(request, 'pages/about/minibuss.html')

def fotballfondet(request):
    return render(request, 'pages/about/fotballfondet.html')

def frivillighetsbanken(request):
    return render(request, 'pages/about/frivillighetsbanken.html')


# def contact(request):
#     if request.method=='POST' and 'contact' in request.POST:
#         navn = request.POST.get('navn')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

#         data = {
#             'navn': navn,
#             'email': email,
#             'message': message,
#         }
#         message = dedent('''
#         Fra: {}

#         Navn: {}

#         Beskjed: {}
#         ''').format(data['email'], data['navn'], data['message'], )
#         send_mail('Epost fra portfolio', message, '', ['sabertoothtri@gmail.com'])
#         return redirect('/')
#     return render(request, 'pages/contact.html')  