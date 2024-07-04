from django.db.models import Count, Avg, Q
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Review
from .serializers import ReviewSerializer
from bb_pp5_api.permissions import IsOwnerOrReadOnly



class ReviewList(generics.ListCreateAPIView):
    """
    List reviews or create a review if logged in
    The perform_create method associates the review with the logged in user.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
        likes_heart_count=Count('likes', filter=Q(likes__flavour=0)),
        likes_smile_count=Count('likes', filter=Q(likes__flavour=1)),
        likes_thumb_count=Count('likes', filter=Q(likes__flavour=2)),
        likes_laugh_count=Count('likes', filter=Q(likes__flavour=3)),
        likes_applaud_count=Count('likes', filter=Q(likes__flavour=0)),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile'
    ]
    search_fields = [
        'owner__username',
        'movie__title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
        'likes_heart_count',
        'likes_smile_count',
        'likes_thumb_count',
        'likes_laugh_count',
        'likes_applaud_count',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a review and edit or delete it if you own it.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Review.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
        likes_heart_count=Count('likes', filter=Q(likes__flavour=0)),
        likes_smile_count=Count('likes', filter=Q(likes__flavour=1)),
        likes_thumb_count=Count('likes', filter=Q(likes__flavour=2)),
        likes_laugh_count=Count('likes', filter=Q(likes__flavour=3)),
        likes_applaud_count=Count('likes', filter=Q(likes__flavour=0)),
    ).order_by('-created_at')