from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, MakeCommentForm
from .models import Article
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm


@require_safe
def index(request):
    page = request.GET.get("page", "1")
    articles = Article.objects.order_by("-pk")
    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(page)
    form = AuthenticationForm()
    user = get_user_model().objects.get(pk=pk)
    weight = user.userweights
    tall = user.usertall
    if user.gender == 1:
        fat = (weight * user.userfat) / 100
        standard_w = ((tall / 100) ** 2) * 22
        standard_nf = standard_w * 0.85
        standard_f = standard_w * 0.15
        score = 80 - (standard_nf - (weight - fat)) + (standard_f - fat)
        if score > 150:
            tier = 1
        elif score > 130:
            tier = 2
        elif score > 110:
            tier = 3
        elif score > 90:
            tier = 4
        elif score > 80:
            tier = 5
        elif score > 70:
            tier = 6
        elif score > 60:
            tier = 7
        else:
            tier = 8
    else:
        fat = (weight * user.userfat) / 100
        standard_w = ((tall / 100) ** 2) * 22
        standard_nf = standard_w * 0.77
        standard_f = standard_w * 0.23
        score = 80 - (standard_nf - (weight - fat)) + (standard_f - fat)
        if score > 150:
            tier = 1
        elif score > 130:
            tier = 2
        elif score > 110:
            tier = 3
        elif score > 90:
            tier = 4
        elif score > 80:
            tier = 5
        elif score > 70:
            tier = 6
        elif score > 60:
            tier = 7
        else:
            tier = 8

    context = {
        "articles": page_obj,
        "form": form,
        "user": user,
        "score": score,
        "tier": tier,
    }

    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        articleform = ArticleForm(request.POST, request.FILES)
        if articleform.is_valid():
            article = articleform.save(commit=False)
            article.user = request.user
            article.save()
            print(4)
            return redirect("articles:index")
    else:
        articleform = ArticleForm()
    context = {"article_form": articleform}
    return render(request, "articles/create.html", context)


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == "POST":
            articleform = ArticleForm(request.POST, request.FILES, instance=article)
            if articleform.is_valid():
                articleform.save()
                return redirect("articles:detail", article.pk)
        else:
            articleform = ArticleForm(instance=article)
        context = {"articleform": articleform}
        return render(request, "articles/update.html", context)
    else:
        return redirect("articles:detail", article.pk)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
        return redirect("articles:index")


def detail(request, pk):
    articles = Article.objects.get(pk=pk)
    commentform = MakeCommentForm()
    context = {
        "articles": articles,
        "commentform": commentform,
    }
    return render(request, "articles/detail.html", context)


def comment(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = MakeCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect("articles:detail", pk)


# 좋아요~~~
def like(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    context = {"isLiked": is_liked, "likeCount": article.like_users.count()}
    return JsonResponse(context)


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        articles = Article.objects.filter(title__contains=searched)
        return render(
            request,
            "articles/searched.html",
            {"searched": searched, "articles": articles},
        )
    else:
        return render(
            request,
            "articles/searched.html",
        )
