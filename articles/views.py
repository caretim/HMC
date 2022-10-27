from django.shortcuts import render,redirect
from .models import Article
from django.contrib.auth import get_user_model
from .form import MakeCommentForm
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator


@require_safe
def index(request):
    page = request.GET.get('page','1')
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles,10)
    page_obj = paginator.get_page(page)
    context = {
        'articles': page_obj
    }
    return render(request, 'articles/index.html', context)




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