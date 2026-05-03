from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    hls_playlist_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "video_file",
            "thumbnail",
            "thumbnail_url",
            "status",
            "created_at",
            "hls_playlist_url",
        ]

    def get_hls_playlist_url(self, obj):
        if not obj.hls_playlist:
            return None

        request = self.context.get("request")

        url = f"/media/{obj.hls_playlist.lstrip('/')}"

        return request.build_absolute_uri(url) if request else url

    def get_thumbnail_url(self, obj):
        request = self.context.get("request")

        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url

        return None