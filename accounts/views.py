from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as my_login, logout as my_logout, get_user_model

# Create your views here.


























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