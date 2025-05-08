from rest_framework import serializers
from .models import ImageColorization

class ImageColorizationSerializer(serializers.ModelSerializer):
    """Serializer for the ImageColorization model"""
    class Meta:
        model = ImageColorization
        fields = ['id', 'original_image', 'colorized_image', 'created_at', 'processed']
        read_only_fields = ['colorized_image', 'created_at', 'processed']

class ImageUploadSerializer(serializers.Serializer):
    """Serializer for image upload"""
    image = serializers.ImageField(required=True)
    
    def validate_image(self, value):
        """Validate the uploaded image"""
        # Check file size (limit to 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image size cannot exceed 10MB")
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        ext = '.' + value.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Only {', '.join(allowed_extensions)} files are allowed")
        
        return value 