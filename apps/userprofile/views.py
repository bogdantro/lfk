from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from apps.blog.models import Blog

from .forms import SignUpForm, UserprofileForm

from django.contrib.auth import login

def signup(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofileform = UserprofileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            login(request, user, backend=backend)  # <- Fix her

            return redirect('myaccount')
    else:
        form = SignUpForm()
        userprofileform = UserprofileForm()
    
    return render(request, 'core/signup.html', {'form': form, 'userprofileform': userprofileform})

# How many of the newest articles the dashboard lists directly; the rest are under "Alle nyheter".
DASHBOARD_LATEST_POSTS = 6


@login_required
def myaccount(request):
    latest_posts = []
    if request.user.is_staff:
        latest_posts = Blog.objects.public().order_by('-published_at', '-id')[:DASHBOARD_LATEST_POSTS]
    return render(request, 'core/myaccount.html', {'latest_posts': latest_posts})


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import StaffOnlyAuthenticationForm

class StaffLoginView(LoginView):
    template_name = "core/login.html"   # your existing template
    authentication_form = StaffOnlyAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("myaccount")
