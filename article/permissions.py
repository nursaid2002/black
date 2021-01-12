from rest_framework.permissions import BasePermission


class ArticlePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_normal)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_normal or request.user.is_staff)

class IsArticleAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user


class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated