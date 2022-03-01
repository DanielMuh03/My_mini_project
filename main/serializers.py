from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MusicSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Music
        fields = ('id', 'title', 'category', 'created_at', 'description')

    def to_representation(self, instance):
        representaion = super().to_representation(instance)
        representaion['author'] = instance.author.email
        representaion['category'] = CategorySerializer(instance.category).data
        representaion['images'] = MusicImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representaion

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Music.objects.create(**validated_data)
        return post


class MusicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)

        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    # reply_count = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('content', )

    def get_author(self, obj):
        return obj.author.username

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.content

        else:
             representation['comments'] = CommentSerializer(instance.parent.first(), many=True).data
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'