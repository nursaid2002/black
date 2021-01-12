from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from article.views import ArticleViewSet, CommentViewSet, CategoryListView

router = DefaultRouter()
router.register('article', ArticleViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include('article.urls')),
    path('category/', CategoryListView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('account/', include('account.urls')),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)