from django.contrib import admin
from .models import Article, Admin, Category, Comment, ArticleImage
from account.models import User


class ImageInLine(admin.TabularInline):
    model = ArticleImage
    extra = 2
    fields = ('image', )

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ImageInLine,
    ]

    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Admin)

