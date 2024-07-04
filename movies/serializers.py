from rest_framework import serializers
from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    is_curator = serializers.SerializerMethodField()
    reviews_count = serializers.ReadOnlyField()
    reviews_avg = serializers.ReadOnlyField()

    def get_is_curator(self, obj):
        request = self.context['request']
        return request.user.groups.filter(name='Movie Curator').exists()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'year', 'director', 'genre',
            'actors', 'image', 'is_curator', 'reviews_count', 'reviews_avg',
        ]