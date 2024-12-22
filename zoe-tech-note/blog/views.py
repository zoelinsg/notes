from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .forms import ArticleForm, ContactForm
from .models import Article, ContactMessage, Tag
from .serializers import ArticleSerializer, ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden

# 首頁視圖
def index(request):
    tag_id = request.GET.get('tag')
    if tag_id:
        articles = Article.objects.filter(tags__id=tag_id)
    else:
        articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(request, 'index.html', {'articles': articles, 'tags': tags})

# 遊客不須登入就可瀏覽文章列表頁面
class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# 遊客不須登入就可瀏覽文章詳情頁面
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# 遊客不須登入就可瀏覽文章詳情頁面
def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    tags = Tag.objects.all()
    return render(request, 'article_detail.html', {'article': article, 'tags': tags})

# 遊客不須登入就可用關鍵字搜尋文章
def search(request):
    keyword = request.GET.get('keyword', '')
    articles = Article.objects.filter(title__icontains=keyword)
    tags = Tag.objects.all()
    return render(request, 'search.html', {'articles': articles, 'tags': tags, 'keyword': keyword})

# 遊客不須登入就可看分類文章
def tag_view(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    articles = Article.objects.filter(tags__name=tag_name)
    return render(request, 'tag.html', {'tag': tag, 'articles': articles})

# 只有我登入後才能新增文章
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article-list-create')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

# 只有我登入後才能編輯文章
@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article-detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})

# 只有我登入後才能刪除文章
@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article-list-create')
    return render(request, 'delete_article.html', {'article': article})

# 留言功能視圖
def contact_view(request):
    ip_address = request.META.get('REMOTE_ADDR')
    cache_key = f'contact_form_{ip_address}' # 以 IP 位址作為緩存鍵
    if cache.get(cache_key): # 如果緩存存在
        return redirect('contact-limit') # 重定向到留言限制視圖

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                '新留言來自 {}'.format(email),
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['zoelin.sg@gmail.com'],  # 確保這裡是你的接收郵箱
            )
            cache.set(cache_key, True, 1800)  # 設置半小時的緩存
            return redirect('contact-success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# 留言成功視圖
def contact_success(request):
    return render(request, 'contact_success.html')

# 留言限制視圖
def contact_limit(request):
    return render(request, 'contact_limit.html')

# 登入視圖
def login_view(request):
    return render(request, 'registration/login.html')

# 登出視圖
def logout_view(request):
    return render(request, 'registration/logged_out.html')

# 留言 API 視圖
class ContactMessageCreate(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact_message = serializer.save()
        send_mail(
            '新留言來自 {}'.format(contact_message.email),
            contact_message.message,
            settings.DEFAULT_FROM_EMAIL,
            ['zoelin.sg@gmail.com'],  # 確保這裡是你的接收郵箱
        )