from rest_framework import serializers

from posts.models import Comment, Group, Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:

        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Group."""

    class Meta:

        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели Post."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    group = serializers.SlugRelatedField(read_only=True, slug_field='title')

    class Meta:

        model = Post
        fields = '__all__'
