from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from slugify import slugify

from accounts.permissions import IsAdmin, ReadOnly

from .models import Category, Genre, Review, Title
from .permissions import ReviewCommentPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitleSerializer)


class GetPostDeleteViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', ]
    search_fields = ['name', ]

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data.get('name'))
        if not serializer.validated_data.get('slug'):
            serializer.save(slug=slug)
        else:
            serializer.save()


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['name', ]
    search_fields = ['name', ]

    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data.get('name'))
        if not serializer.validated_data.get('slug'):
            serializer.save(slug=slug)
        else:
            serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['year', ]
    search_fields = ['genre__slug', 'category__slug', ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        else:
            return TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('-id')
        category = self.request.query_params.get('category', None)
        genre = self.request.query_params.get('genre', None)
        name = self.request.query_params.get('name', None)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ReviewCommentPermission,
    ]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [ReviewCommentPermission]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title__id=title_id)
        serializer.save(author=self.request.user, review=review)
