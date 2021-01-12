from django.db import models

from account.models import User


class Admin(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, primary_key=True)
    # parent = models.ForeignKey('self', related_name='admin', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    admin = models.ForeignKey('Admin', related_name='admins', on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.author}: {self.text}"



class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article', null=True, blank=True)