from django.db import models

class AudioFile(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    denoised_file = models.FileField(upload_to='processed/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio File {self.id}"
