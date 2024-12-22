from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 標籤名稱

    def __str__(self):
        return self.name  # 返回標籤名稱作為表示

class Article(models.Model):
    title = models.CharField(max_length=200)  # 文章標題
    tags = models.ManyToManyField(Tag, blank=True)  # 文章標籤，可多選
    content = MarkdownxField()  # 文章內容，使用 Markdown 編輯
    created_at = models.DateTimeField(auto_now_add=True)  # 文章創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 文章更新時間

    def formatted_markdown(self):
        """將 Markdown 內容轉換為 HTML"""
        return markdownify(self.content)

    def __str__(self):
        return self.title  # 返回文章標題作為表示

class ContactMessage(models.Model):
    email = models.EmailField()  # 留言者的電子郵件
    message = models.TextField()  # 留言內容
    created_at = models.DateTimeField(auto_now_add=True)  # 留言創建時間

    def __str__(self):
        return f"Message from {self.email}"  # 返回留言者的電子郵件作為表示