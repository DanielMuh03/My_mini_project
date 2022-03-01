from django.contrib import admin

from .models import *


class MusicImageInline(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    inlines = [MusicImageInline, ]


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Favorite)

