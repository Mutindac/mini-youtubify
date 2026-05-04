import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer


class VideoUploadView(APIView):
    def post(self, request):
        title = request.data.get('title')
        video_file = request.FILES.get('video_file')

        if not title or not video_file:
            return Response({"error": "Title and video file are required"}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.create(title=title, status='processing')

        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                video_file,
                resource_type='video',
                folder='mini_youtube',
                eager=[{"streaming_profile": "full_hd", "format": "m3u8"}],
                eager_async=True,
            )

            public_id = result['public_id']

            # Cloudinary auto thumbnail
            thumbnail_url = f"https://res.cloudinary.com/{result['secure_url'].split('/')[4]}/video/upload/so_0,f_jpg/{public_id}.jpg"

            video.cloudinary_public_id = public_id
            video.video_url = result['secure_url']
            video.thumbnail_url = thumbnail_url
            video.status = 'ready'
            video.save()

            return Response({
                "message": "Video uploaded successfully",
                "video_id": video.id,
                "video_url": video.video_url,
                "thumbnail_url": video.thumbnail_url,
                "video": VideoSerializer(video).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Upload error:", e)
            video.status = 'failed'
            video.save()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoDetailView(APIView):
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
            data = VideoSerializer(video).data
            return Response(data, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)