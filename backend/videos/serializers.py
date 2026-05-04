from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "video_url",
            "thumbnail_url",
            "cloudinary_public_id",
            "status",
            "created_at",
        ]