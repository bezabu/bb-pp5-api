from rest_framework import serializers
from reviews.models import Review
from likes.models import Like


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie_title = serializers.ReadOnlyField(source='movie.title')

    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    movie_image = serializers.ReadOnlyField(source='movie.image.url')
    likes_heart_count = serializers.ReadOnlyField()
    likes_smile_count = serializers.ReadOnlyField()
    likes_thumb_count = serializers.ReadOnlyField()
    likes_laugh_count = serializers.ReadOnlyField()
    likes_applaud_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, review=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Review
        fields = [
            'id', 'owner', 'movie', 'movie_title', 'movie_image', 'created_at',
            'updated_at', 'content', 'rating', 'is_owner', 'profile_id', 'profile_image',
            'like_id', 'likes_count', 'comments_count', 'likes_heart_count', 'likes_smile_count',
            'likes_thumb_count', 'likes_laugh_count', 'likes_applaud_count'
        ]

