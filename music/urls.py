from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from music import settings
from main.views import CategoryListView, PostsView, MusicImageView, CommentViewSet
from drf_yasg import openapi

router = DefaultRouter()
router.register('posts', PostsView)
router.register('comment', CommentViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Music KG",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/add-image/', MusicImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('', schema_view.with_ui()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

