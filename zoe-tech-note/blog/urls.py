from django.urls import path
from django.contrib.auth import views as auth_views  # 確保導入 auth_views
from django.views.generic import TemplateView  # 確保導入 TemplateView
from .views import ArticleListCreate, ArticleDetail, create_article, edit_article, delete_article, article_detail_view, index, search, contact_view, contact_success, contact_limit, tag_view, ContactMessageCreate

urlpatterns = [
    path('admin-login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='admin-login'),  # 專屬登入頁面
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),  # 登出頁面
    
    # API 路由
    path('api/articles/', ArticleListCreate.as_view(), name='article-list-create'),  # 文章列表和創建
    path('api/articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),  # 文章詳情、更新和刪除
    path('api/contact/', ContactMessageCreate.as_view(), name='contact-message-create'),  # 留言創建
    
    # 網頁路由
    path('articles/create/', create_article, name='create-article'),  # 新增文章
    path('articles/edit/<int:pk>/', edit_article, name='edit-article'),  # 編輯文章
    path('articles/delete/<int:pk>/', delete_article, name='delete-article'),  # 刪除文章
    path('articles/<int:pk>/', article_detail_view, name='article-detail-view'),  # 文章詳情頁面
    path('search/', search, name='search'),  # 搜尋文章
    path('contact/', contact_view, name='contact'),  # 留言頁面
    path('contact/success/', TemplateView.as_view(template_name='contact_success.html'), name='contact-success'),  # 留言成功頁面
    path('contact/limit/', TemplateView.as_view(template_name='contact_limit.html'), name='contact-limit'),  # 留言限制頁面
    path('tag/<str:tag_name>/', tag_view, name='tag-view'),  # 分類文章頁面
    path('', index, name='index'),  # 首頁
]