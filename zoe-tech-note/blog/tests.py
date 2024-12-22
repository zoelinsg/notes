from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, ContactMessage
from django.core import mail

# 建立測試案例
class ArticleTests(TestCase):

    # 設定測試資料
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.article = Article.objects.create(title='Test Article', content='Test Content')

    # 測試文章列表視圖
    def test_article_list_view(self):
        response = self.client.get(reverse('article-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    # 測試文章詳情視圖
    def test_article_detail_view(self):
        response = self.client.get(reverse('article-detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    # 測試文章搜尋視圖
    def test_search_view(self):
        response = self.client.get(reverse('search'), {'keyword': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    # 測試新增文章視圖（未登入）
    def test_create_article_view_not_logged_in(self):
        response = self.client.get(reverse('create-article'))
        self.assertNotEqual(response.status_code, 200)

    # 測試新增文章視圖（已登入）
    def test_create_article_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create-article'), {'title': 'New Article', 'content': 'New Content'})
        self.assertEqual(response.status_code, 302)  # 應該會重定向

    # 測試編輯文章視圖（已登入）
    def test_edit_article_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit-article', args=[self.article.pk]), {'title': 'Updated Title', 'content': 'Updated Content'})
        self.assertEqual(response.status_code, 302)  # 應該會重定向

    # 測試刪除文章視圖（已登入）
    def test_delete_article_view_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete-article', args=[self.article.pk]))
        self.assertEqual(response.status_code, 302)  # 應該會重定向
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    # 測試留言表單視圖
    def test_contact_form_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    # 測試留言表單提交
    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'email': 'test@example.com',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 302)  # 應該會重定向到成功頁面
        self.assertEqual(len(mail.outbox), 1)  # 應該會寄出一封信
        self.assertIn('This is a test message.', mail.outbox[0].body)