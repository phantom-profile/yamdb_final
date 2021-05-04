from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category-list')
router.register('genres', GenreViewSet, basename='genre-list')
router.register('titles', TitleViewSet, basename='title-list')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
