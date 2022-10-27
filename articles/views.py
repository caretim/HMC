

from django.shortcuts import render,redirect
from .models import Article
from django.contrib.auth import get_user_model
from .form import MakeCommentForm

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')



def detail(request,pk):
    articles = Article.objects.get(pk=pk)
    commentform = MakeCommentForm()
    context={
        'articles' :  articles,
        'commentform':commentform
    }
    return(request,"articles/detail.html",context)
    



def comment(request,article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == "POST":
        form = MakeCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect("articles:detail", article_pk)



    


