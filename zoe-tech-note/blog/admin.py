from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Article, Tag, ContactMessage

# 註冊 Article 和 Tag 模型到 Django 管理後台，使用 MarkdownxModelAdmin 來支援 Markdown 編輯
admin.site.register(Article, MarkdownxModelAdmin)
admin.site.register(Tag)

# 註冊 ContactMessage 模型到 Django 管理後台
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'created_at')  # 顯示的欄位
    search_fields = ('email', 'message')  # 可搜尋的欄位