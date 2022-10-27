
from django.shortcuts import render, redirect, get_object_or_404
# from .models import User 
from django.contrib import messages
from django.contrib.auth import login as my_login, logout as my_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

@require_POST
@login_required
def ID_delete(request):
    request.user.delete()
    return redirect('articles:index')

  

# Create your views here.
def detail(request, pk):
    user = get_user_model()
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)
    
    
    
    def login (request):
    if request.method == 'post':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            my_login(request,form.get_user())
            return redirect(" article:index ")
    else:
        form = AuthenticationForm(request.POST)
    context = {
        'form':form
    }
    return render (request, "accounts/login.html",context)


def update (request,pk):
    if request.method == 'POST':
        user =get_user_model().objects.get(pk=pk)
        if request.user == user.user:
            form = AuthenticationForm(request.POST ,instance=user)
            form.is_valid()
            form.save()
            return redirect("article:index")
    else:
        form = AuthenticationForm(instance=user)
    context={
        'form':form
    }
    return render (request,"accounts/update.html",context)

