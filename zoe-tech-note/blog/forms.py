from django import forms
from .models import Article, Tag, ContactMessage

# 創建 ArticleForm 表單類別，用於文章的創建和編輯
class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)  # 多對多標籤

    class Meta:
        model = Article
        fields = ['title', 'tags', 'content']  # 表單包含的欄位

# 創建 ContactForm 表單類別，用於收集留言資料
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['email', 'message']  # 表單包含的欄位