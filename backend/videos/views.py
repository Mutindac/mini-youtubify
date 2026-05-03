import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from .utils import process_video, generate_thumbnail, convert_to_hls


class VideoUploadView(APIView):
    def post(self, request):
        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            video = serializer.save(status="processing")

            # paths
            input_path = video.video_file.path
            processed_path = input_path.replace(".mp4", "_processed.mp4")

            thumbnail_dir = os.path.join("media", "thumbnails")
            os.makedirs(thumbnail_dir, exist_ok=True)

            thumbnail_path = os.path.join(
                thumbnail_dir, f"{video.id}_thumbnail.jpg"
            )

            hls_output_dir = os.path.join(
                "media", "processed", f"video_{video.id}"
            )
            os.makedirs(hls_output_dir, exist_ok=True)

            try:
                # process video
                process_video(input_path, processed_path)

                # generate thumbnail
                generate_thumbnail(processed_path, thumbnail_path)

                # convert to HLS
                playlist_path = convert_to_hls(
                    processed_path, hls_output_dir
                )

                if not playlist_path:
                    raise Exception("Failed to convert video to HLS")

                # save thumbnail
                with open(thumbnail_path, "rb") as f:
                    video.thumbnail.save(
                        f"{video.id}_thumbnail.jpg",
                        f,
                        save=False
                    )

                # save relative path
                video.hls_playlist = os.path.relpath(
                    playlist_path, "media"
                ).replace("\\", "/")

                video.status = "ready"
                video.save()

               
                hls_url = request.build_absolute_uri(
                    f"/media/{video.hls_playlist}"
                )

                return Response({
                    "message": "Video uploaded and processed successfully",
                    "status": video.status,
                    "video_id": video.id,
                    "thumbnail_url": request.build_absolute_uri(video.thumbnail.url)
                    if video.thumbnail else None,
                    "hls_playlist_url": hls_url,
                    "video": VideoSerializer(video).data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print("Error processing video:", e)

                video.status = "failed"
                video.save()

                return Response({
                    "message": "Video uploaded but failed to process",
                    "status": video.status,
                    "video_id": video.id,
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# VIDEO LIST

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


# VIDEO DETAIL

class VideoDetailView(APIView):
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)

            hls_url = None
            if video.hls_playlist:
                hls_url = request.build_absolute_uri(
                    f"/media/{video.hls_playlist}"
                )

            data = VideoSerializer(video).data
            data["hls_playlist_url"] = hls_url

            return Response(data, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response(
                {"error": "Video not found"},
                status=status.HTTP_404_NOT_FOUND
            )