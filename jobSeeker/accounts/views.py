from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import EmployerSignUpForm, JobSeekerSignUpForm


def employer_signup(request):
    if request.method == "POST":
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, "Employer account created successfully!")
            return redirect("jobs:employer_dashboard")
    else:
        form = EmployerSignUpForm()
    return render(request, "accounts/employer_signup.html", {"form": form})


def jobseeker_signup(request):
    if request.method == "POST":
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Job seeker account created successfully!")
            return redirect("jobs:list")
    else:
        form = JobSeekerSignUpForm()
    return render(request, "accounts/jobseeker_signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # redirect depending on role
                if user.role == "employer":
                    return redirect("jobs:employer_dashboard")
                elif user.role == "jobseeker":
                    return redirect("jobs:list")
                else:
                    return redirect("admin:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")
