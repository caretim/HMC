from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
def detail(request, pk):
    user = get_user_model()
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)