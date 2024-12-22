from rest_framework import serializers
from .models import Article, Tag, ContactMessage

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  # 序列化的欄位

class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # 嵌套序列化標籤

    class Meta:
        model = Article
        fields = ['id', 'title', 'tags', 'content', 'created_at', 'updated_at']  # 序列化的欄位

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'email', 'message', 'created_at']  # 序列化的欄位