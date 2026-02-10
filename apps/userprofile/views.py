from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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

@login_required
def myaccount(request):
    return render(request, 'core/myaccount.html')


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import StaffOnlyAuthenticationForm

class StaffLoginView(LoginView):
    template_name = "core/login.html"   # your existing template
    authentication_form = StaffOnlyAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("myaccount")
