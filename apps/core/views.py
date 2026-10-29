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
from .models import *


# Home
# Which hero the homepage shows – the one line to change to switch back:
#   'promotion' = the 2026 promotion celebration (core/hero-promotion.html)
#   'default'   = the everyday hero with the video (core/hero-default.html)
HOMEPAGE_HERO = 'promotion'

# Photos in the promotion hero (static/images/covers/<file>.webp + .jpg), all by Niklas Lyngfoss.
# The carousel alternates Herrer and Kvinner and shows the team's next photo each time.
# position = which part of the photo stays in view (CSS object-position): desktop, then mobile.
PROMOTION_PHOTOS = [
    {'team': 'herrer', 'file': 'opprykk-herrer-1', 'position': '50% 45%', 'position_mobile': '62% 50%',
     'alt': 'A-laget til Lillehammer FK stiller opp før kampen mot Sandefjord 2 på Stampesletta'},
    {'team': 'herrer', 'file': 'opprykk-herrer-2', 'position': '50% 18%', 'position_mobile': '45% 50%',
     'alt': 'Spillere med gullhatter feirer opprykket sammen med unge supportere på Stampesletta'},
    {'team': 'herrer', 'file': 'opprykk-herrer-3', 'position': '50% 55%', 'position_mobile': '52% 50%',
     'alt': 'Spillerne kaster en leder i været etter opprykket på Stampesletta'},
    {'team': 'kvinner', 'file': 'opprykk-kvinner-1', 'position': '50% 34%', 'position_mobile': '50% 50%',
     'alt': 'Kvinnelaget til Lillehammer FK samlet i ring før kampen mot Vang'},
    {'team': 'kvinner', 'file': 'opprykk-kvinner-2', 'position': '50% 48%', 'position_mobile': '50% 55%',
     'alt': 'Kvinnelaget til Lillehammer FK samlet til lagbilde etter kampen mot Vang'},
]


def home(request):
    posts = Blog.objects.public().newest_first()

    return render(request, 'core/home.html', {
        'latest_blog': posts[0] if len(posts) > 0 else None,
        'second_latest_blog': posts[1] if len(posts) > 1 else None,
        'hero': HOMEPAGE_HERO,
        'promotion_photos': PROMOTION_PHOTOS,
    })

def xtravgs(request):
    return render(request, 'pages/xtravgs.html')

def fotballextra(request):
    return render(request, 'pages/fotball-extra.html')

# Sport
def senior(request):
    return render(request, 'teams/senior.html')


####################################

def senior_herrer(request):
    players = Player.objects.filter(
        team__name__iexact="Herrer",
        is_active=True
    )

    return render(request, "teams/senior-herrer.html", {
        "players": players
    })

def senior_kvinner(request):
    players = Player.objects.filter(
        team__name__iexact="Kvinner",
        is_active=True
    )
    return render(request, 'teams/senior-kvinner.html', {"players": players})


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from .forms import PlayerForm  # your ModelForm for Player

@staff_member_required
def player_create(request):
    team_name = request.GET.get("team", "Herrer")  # default
    team = get_object_or_404(Team, name__iexact=team_name)

    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team  # ✅ force correct team
            player.save()
            return redirect("myaccount")
    else:
        form = PlayerForm()

    return render(request, "teams/player_create.html", {
        "form": form,
        "team": team,
    })

#####################################

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

def kontakt(request):
    return render(request, 'pages/about/kontakt.html')

def varsling(request):
    return render(request, 'pages/about/varsling.html')

def forsikring(request):
    return render(request, 'pages/about/forsikring.html')

def dommere(request):
    return render(request, 'pages/about/dommere.html')

def varsling(request):
    return render(request, 'pages/about/varsling.html')

def politiattest(request):
    return render(request, 'pages/about/politiattest.html')

def minibuss(request):
    return render(request, 'pages/about/minibuss.html')

def fotballfondet(request):
    return render(request, 'pages/about/fotballfondet.html')


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