from django.shortcuts import render, redirect, get_object_or_404

# from .models import User
from django.contrib import messages
from django.contrib.auth import login as my_login, logout as my_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


@require_POST
@login_required
def ID_delete(request):
    request.user.delete()
    my_logout(request)
    return redirect("articles:index")


# Create your views here.
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {"user": user}
    return render(request, "accounts/detail.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect("articles:index")
    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    my_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("articles:index")


@login_required
def update(request, pk):
    if request.method == "POST":
        user = get_user_model().objects.get(pk=pk)
        if request.user == user.user:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            form.is_valid()
            form.save()
            return redirect("article:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "accounts/update.html", context)


@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        messages.warning(request, "본인을 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", pk)
    else:
        if request.user in user.followings.all():
            user.followings.remove(request.user)
        else:
            user.followings.add(request.user)
        return redirect("accounts:detail", pk)
