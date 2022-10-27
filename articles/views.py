from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

@login_required
def create(request):
    if request.method == 'POST':
        articleform = ArticleForm(request.POST, request.FILES)
        if articleform.is_valid():
            article = articleform.save(commit=False)
            article.user = request.user
            article.save()
            print(4)
            return redirect('articles:index')
    else:
        articleform = ArticleForm()
    context = {
        'article_form': articleform
    }
    return render(request, 'articles/create.html', context)

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            articleform = ArticleForm(request.POST, request.FILES, instance=article)
            if articleform.is_valid():
                articleform.save()
                return redirect('articles:detail', article.pk)
        else:
            articleform = ArticleForm(instance=article)
        context = {
            'articleform': articleform
        }
        return render(request, 'articles/update.html', context)
    else:
        return redirect('articles:detail', article.pk)

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
        return redirect('articles:index')