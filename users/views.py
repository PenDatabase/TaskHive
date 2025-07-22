from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import RegisterForm

from .models import WORKitUser as User, Profile


# Register Users
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                form.save()
                return redirect("home")
        else:
            form = RegisterForm()
            
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})



#Profile page
@login_required
def profile_display(request):
    user = User.objects.get(id=request.user.id)
    return render(request, "registration/profile.html", {"user": user})