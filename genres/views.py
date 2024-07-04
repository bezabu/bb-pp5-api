from django.db.models import Count, Avg
from rest_framework import generics, permissions, filters
from django.core.exceptions import PermissionDenied
from .models import Genre
from .serializers import GenreSerializer
from bb_pp5_api.permissions import IsOwnerOrReadOnly, HasMoviePermissions, IsCuratorOrReadOnly



class GenreList(generics.ListAPIView):
    """
    List all genres
    No Create view
    """
    
    queryset = Genre.objects.annotate(
        movies_count=Count('movies', distinct=True),
        movies_avg=Avg('movies__reviews__rating')
    ).order_by('-movies_count')
    
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'moviess_count',
        'moviess_avg',
    ]


class GenreCreate(generics.CreateAPIView):
    """
    Movie create view
    Only accessible by movie curators
    """
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated, IsCuratorOrReadOnly]

class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a movie and edit or delete it if you own it.
    """
    serializer_class = GenreSerializer
    permission_classes = [HasMoviePermissions]
    #permission_classes = [IsCuratorOrReadOnly]
    queryset = Genre.objects.annotate(
        movies_count=Count('movies', distinct=True)
    ).order_by('-movies_count')


