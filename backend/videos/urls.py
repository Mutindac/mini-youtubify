from django.urls import path
from .views import VideoUploadView, VideoListView, VideoDetailView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('list/', VideoListView.as_view(), name='video-list'),
    path('detail/<int:video_id>/', VideoDetailView.as_view(), name='video-detail'),
    
]
print("Video URLs configured")