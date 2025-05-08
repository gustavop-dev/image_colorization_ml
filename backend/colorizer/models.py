from django.db import models
import os
from django.utils import timezone

def get_upload_path(instance, filename):
    """Generate upload path for image files"""
    return os.path.join('images', 'original', filename)

def get_colorized_path(instance, filename):
    """Generate upload path for colorized image files"""
    name, ext = os.path.splitext(filename)
    return os.path.join('images', 'colorized', f"{name}_colorized{ext}")

class ImageColorization(models.Model):
    """Model for storing original and colorized images"""
    original_image = models.ImageField(upload_to=get_upload_path)
    colorized_image = models.ImageField(upload_to=get_colorized_path, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Image {self.id} - {'Processed' if self.processed else 'Pending'}"
    
    def delete(self, *args, **kwargs):
        """Delete image files when model instance is deleted"""
        # Delete the original image file
        if self.original_image:
            if os.path.isfile(self.original_image.path):
                os.remove(self.original_image.path)
        
        # Delete the colorized image file if it exists
        if self.colorized_image:
            if os.path.isfile(self.colorized_image.path):
                os.remove(self.colorized_image.path)
        
        super().delete(*args, **kwargs)
