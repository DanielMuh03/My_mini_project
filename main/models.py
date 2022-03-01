from django.db import models

from account.models import MainUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='music')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='music')
    title = models.CharField(max_length=225)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='music', blank=True, null=True)
    post = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    post = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MainUser,
                                   related_name='likers',
                                   blank=True)

    def __str__(self):
        return self.post


class Favorite(models.Model):
    film = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)