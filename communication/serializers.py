"""
Serializers for the Communication API using Django REST Framework.
"""

import urllib.request
import urllib.error

from rest_framework import serializers

from communication.models import Post


class PostAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    api_url = serializers.SerializerMethodField()

    def get_api_url(self, obj):
        return f"/api/v2/people/{obj.pk}/"


class PostListSerializer(serializers.ModelSerializer):
    author = PostAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'post_title', 'post_slug', 'author', 'created', 'modified']
        read_only_fields = ['id', 'post_slug']


class PostDetailSerializer(PostListSerializer):
    content = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['markdown_url', 'content']

    def get_content(self, obj):
        try:
            request = urllib.request.Request(str(obj.markdown_url))
            response = urllib.request.urlopen(request)
            return response.read().decode('utf-8')
        except (urllib.error.URLError, ValueError):
            return None
