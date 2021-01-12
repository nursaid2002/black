from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Article, Category, Comment
from account.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'body', 'author_id')

    # title = serializers.CharField(max_length=120)
    # description = serializers.CharField()
    # body = serializers.CharField()
    # author_id = serializers.IntegerField()

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return "No Image"

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category.all(), many=True).data
        representation['image'] = self._get_image_url(instance)
        if "comment" not in self.fields:
            representation['comments'] = CommentSerializer(instance.comment_set.all(), many=True).data
        return representation

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.get(pk=pk))
        article.delete()
        return Response({"message": "Article with id `{}` has been deleted.".format(pk)}, status=204)

class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'author_id', 'image')




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'post')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user
        comment = Comment.objects.create(**validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author_id).data
        return representation

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author_id', 'id', 'text', 'article')