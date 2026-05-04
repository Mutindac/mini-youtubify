from django.db import models

class Video(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    cloudinary_public_id = models.CharField(max_length=500, null=True, blank=True)
    video_url = models.URLField(max_length=500, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    hls_playlist = models.CharField(max_length=500, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title