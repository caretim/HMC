from django.shortcuts import render
from .models import Article
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator
# Create your views here.

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
