from django.db.models import Count, Avg
from rest_framework import generics, permissions, filters
from django.core.exceptions import PermissionDenied
from .models import Movie
from .serializers import MovieSerializer
from bb_pp5_api.permissions import IsOwnerOrReadOnly, HasMoviePermissions, IsCuratorOrReadOnly



class MovieList(generics.ListCreateAPIView):
    """
    List all movies
    No Create view
    """
    
    queryset = Movie.objects.annotate(
        reviews_count=Count('reviews', distinct=True),
        reviews_avg=Avg('reviews__rating')
    ).order_by('-reviews_count')
    
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'reviews_count',
        'reviews_avg',
        'year',
        'director',
        'genre',
    ]


class MovieCreate(generics.CreateAPIView):
    """
    Movie create view
    Only accessible by movie curators
    """
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.IsAuthenticated, IsCuratorOrReadOnly]



class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a movie and edit or delete it if you own it.
    """
    serializer_class = MovieSerializer
    permission_classes = [HasMoviePermissions]
    #permission_classes = [IsCuratorOrReadOnly]
    queryset = Movie.objects.annotate(
        reviews_count=Count('reviews', distinct=True)
    ).order_by('-reviews_count')


