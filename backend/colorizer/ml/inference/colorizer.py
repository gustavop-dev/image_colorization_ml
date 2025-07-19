"""
Inference and colorization functionality for trained models.
"""

import numpy as np
import tensorflow as tf
import cv2
from pathlib import Path
from typing import Union, Tuple
import math
import os
import tempfile
from PIL import Image, ImageOps

class ImageColorizer:
    """
    Handles inference and colorization of grayscale images.
    """
    
    def __init__(self, model: tf.keras.Model, img_size: int = 256):
        """
        Initialize the colorizer with a trained model.
        
        Args:
            model (tf.keras.Model): The trained colorization model
            img_size (int): Size of input images for the model
        """
        self.model = model
        self.img_size = img_size
    
    def _compress_image_smart(self, image_path: Union[str, Path], max_size_mb: float = 1.0, max_dimension: int = 1600) -> str:
        """
        Compress image intelligently similar to WhatsApp compression.
        
        This function reduces file size while maintaining good visual quality by:
        - Limiting maximum dimension (like WhatsApp's 1600px limit)
        - Progressive JPEG quality reduction
        - Smart format conversion
        - Proper handling of WEBP, PNG transparency
        
        Args:
            image_path (Union[str, Path]): Path to input image
            max_size_mb (float): Maximum file size in MB (default: 1.0)
            max_dimension (int): Maximum dimension for longest side (default: 1600)
            
        Returns:
            str: Path to compressed image (temporary file)
        """
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Check original file size
        original_size = os.path.getsize(image_path)
        if original_size <= max_size_bytes:
            return str(image_path)  # No compression needed
        
        # Open image with PIL for better compression control
        with Image.open(image_path) as img:
            original_format = img.format
            print(f"Original format: {original_format}")
            
            # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
            if img.mode != 'RGB':
                # Handle transparency by adding white background
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    
                    if img.mode == 'P':
                        # Handle palette mode (some PNGs, GIFs)
                        img = img.convert('RGBA')
                    
                    if 'transparency' in img.info or img.mode in ('RGBA', 'LA'):
                        # Handle transparency properly for PNG and WEBP
                        if img.mode == 'LA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                    else:
                        background.paste(img)
                    img = background
                else:
                    img = img.convert('RGB')
            
            # Apply auto-orientation (handles EXIF rotation)
            img = ImageOps.exif_transpose(img)
            
            original_width, original_height = img.size
            
            # Step 1: Resize if image is too large (WhatsApp-style)
            if max(original_width, original_height) > max_dimension:
                # Calculate new dimensions maintaining aspect ratio
                if original_width > original_height:
                    new_width = max_dimension
                    new_height = int((original_height * max_dimension) / original_width)
                else:
                    new_height = max_dimension
                    new_width = int((original_width * max_dimension) / original_height)
                
                # Use high-quality resampling
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized from {original_width}x{original_height} to {new_width}x{new_height}")
            
            # Step 2: Progressive quality reduction until size target is met
            quality_levels = [85, 75, 65, 55, 45, 35, 25]  # WhatsApp typically uses 75-85%
            
            for quality in quality_levels:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                # Save with current quality (always as JPEG for compression)
                img.save(
                    temp_path, 
                    'JPEG', 
                    quality=quality, 
                    optimize=True,  # Enable JPEG optimization
                    progressive=True  # Progressive JPEG for better compression
                )
                
                # Check file size
                compressed_size = os.path.getsize(temp_path)
                size_mb = compressed_size / (1024 * 1024)
                
                print(f"Quality {quality}%: {size_mb:.2f}MB (target: {max_size_mb}MB)")
                
                if compressed_size <= max_size_bytes:
                    print(f"✅ Compressed from {original_size/(1024*1024):.2f}MB to {size_mb:.2f}MB (WEBP/PNG→JPEG)")
                    return temp_path
                else:
                    # Remove temp file and try lower quality
                    os.unlink(temp_path)
            
            # If still too large, create a final version with very aggressive compression
            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Further resize if necessary
            current_width, current_height = img.size
            if max(current_width, current_height) > 800:  # Emergency resize
                if current_width > current_height:
                    new_width = 800
                    new_height = int((current_height * 800) / current_width)
                else:
                    new_height = 800
                    new_width = int((current_width * 800) / current_height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"Emergency resize to {new_width}x{new_height}")
            
            img.save(temp_path, 'JPEG', quality=20, optimize=True)
            final_size = os.path.getsize(temp_path)
            print(f"⚠️ Final aggressive compression: {final_size/(1024*1024):.2f}MB")
            
            return temp_path
    
    def _process_patches(self, image: np.ndarray, patch_size: int = 256, overlap: int = 32) -> np.ndarray:
        """
        Process image in patches to maintain high resolution.
        
        Args:
            image (np.ndarray): Input image in RGB format
            patch_size (int): Size of each patch (default: 256)
            overlap (int): Overlap between patches for smoother blending
            
        Returns:
            np.ndarray: Processed image with original resolution
        """
        h, w, c = image.shape
        stride = patch_size - overlap
        
        # Calculate number of patches needed
        patches_h = math.ceil(h / stride)
        patches_w = math.ceil(w / stride)
        
        print(f"Processing image in {patches_h}x{patches_w} = {patches_h*patches_w} patches")
        
        # Create output image
        result = np.zeros_like(image, dtype=np.float32)
        weight_map = np.zeros((h, w), dtype=np.float32)
        
        for i in range(patches_h):
            for j in range(patches_w):
                if (i * patches_w + j + 1) % 10 == 0:  # Progress indicator
                    print(f"Processing patch {i * patches_w + j + 1}/{patches_h * patches_w}")
                
                # Calculate patch coordinates
                start_h = i * stride
                start_w = j * stride
                end_h = min(start_h + patch_size, h)
                end_w = min(start_w + patch_size, w)
                
                # Extract patch
                patch = image[start_h:end_h, start_w:end_w]
                
                # Pad patch to model size if needed
                patch_h, patch_w = patch.shape[:2]
                if patch_h != patch_size or patch_w != patch_size:
                    # Pad to patch_size
                    padded_patch = np.zeros((patch_size, patch_size, c), dtype=patch.dtype)
                    padded_patch[:patch_h, :patch_w] = patch
                    patch_to_process = padded_patch
                else:
                    patch_to_process = patch
                
                # Process patch through model
                patch_input = (patch_to_process.astype(np.float32) / 255.0)[None, ...]
                patch_output = self.model.predict(patch_input, verbose=0)[0]
                patch_output = np.clip(patch_output * 255.0, 0, 255)
                
                # Extract only the valid region (remove padding)
                patch_result = patch_output[:patch_h, :patch_w]
                
                # Create weight map for blending (reduces edge artifacts)
                patch_weight = np.ones((patch_h, patch_w), dtype=np.float32)
                if overlap > 0:
                    # Apply gaussian-like weights near edges for smooth blending
                    for y in range(patch_h):
                        for x in range(patch_w):
                            weight_y = min(y + 1, patch_h - y, overlap) / overlap
                            weight_x = min(x + 1, patch_w - x, overlap) / overlap
                            patch_weight[y, x] = min(weight_y, weight_x)
                
                # Add to result with blending
                result[start_h:end_h, start_w:end_w] += patch_result * patch_weight[:, :, np.newaxis]
                weight_map[start_h:end_h, start_w:end_w] += patch_weight
        
        # Normalize by weight map to complete blending
        weight_map[weight_map == 0] = 1  # Avoid division by zero
        result = result / weight_map[:, :, np.newaxis]
        
        return result.astype(np.uint8)
    
    def colorize(self, image_path: Union[str, Path], save_to: Union[str, Path, None] = None, use_patches: bool = True, auto_compress: bool = True, max_size_mb: float = 1.0) -> np.ndarray:
        """
        Colorize a single grayscale image using the trained model.
        
        This method can process images in high resolution by using patch-based processing,
        and automatically compresses large images for optimal processing speed.
        
        Args:
            image_path (Union[str, Path]): Path to input grayscale image
            save_to (Union[str, Path, None]): Optional path to save colorized output
            use_patches (bool): Whether to use patch-based processing for high resolution
            auto_compress (bool): Whether to automatically compress large images
            max_size_mb (float): Maximum file size in MB before compression
            
        Returns:
            np.ndarray: Colorized image array in uint8 RGB format with original dimensions
            
        Raises:
            RuntimeError: If the model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")

        # Step 1: Auto-compress if needed
        processed_image_path = image_path
        temp_files_to_cleanup = []
        
        if auto_compress:
            file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
            if file_size_mb > max_size_mb:
                print(f"🗜️ Image size ({file_size_mb:.2f}MB) exceeds {max_size_mb}MB, applying smart compression...")
                compressed_path = self._compress_image_smart(image_path, max_size_mb)
                processed_image_path = compressed_path
                if compressed_path != str(image_path):  # Only add to cleanup if it's a temp file
                    temp_files_to_cleanup.append(compressed_path)
            else:
                print(f"✅ Image size ({file_size_mb:.2f}MB) is within limits, no compression needed")

        try:
            # Load and preprocess the input image
            img = cv2.imread(str(processed_image_path), cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Store original dimensions
            original_height, original_width = img_rgb.shape[:2]
            
            # Decide processing method based on image size and user preference
            if use_patches and (original_height > self.img_size or original_width > self.img_size):
                print(f"🎨 Processing {original_width}x{original_height} image using patch-based method for high quality...")
                pred_original_size = self._process_patches(img_rgb)
            else:
                print(f"🎨 Processing {original_width}x{original_height} image using resize method...")
                # Fallback to simple resize method for smaller images
                img_resized = cv2.resize(img_rgb, (self.img_size, self.img_size))
                inp = (img_resized.astype(np.float32) / 255.0)[None, ...]
                pred = self.model.predict(inp)[0]
                pred = np.clip(pred * 255.0, 0, 255).astype(np.uint8)
                pred_original_size = cv2.resize(pred, (original_width, original_height))

            # Save output if requested
            if save_to is not None:
                Path(save_to).parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(save_to), cv2.cvtColor(pred_original_size, cv2.COLOR_RGB2BGR))

            return pred_original_size
            
        finally:
            # Cleanup temporary compressed files
            for temp_file in temp_files_to_cleanup:
                try:
                    os.unlink(temp_file)
                    print(f"🗑️ Cleaned up temporary file: {temp_file}")
                except Exception as e:
                    print(f"⚠️ Could not cleanup {temp_file}: {e}")
    
    def save_model(self, path: Union[str, Path]) -> None:
        """
        Save the trained model to disk.
        
        This method saves the entire model (architecture + weights) to the
        specified path in TensorFlow's SavedModel format.
        
        Args:
            path (Union[str, Path]): Path where the model should be saved
            
        Raises:
            RuntimeError: If the model hasn't been provided
        """
        if self.model is None:
            raise RuntimeError("Model not built. Call build_model() first.")
        
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(str(path))
        print(f"Model saved to {path}") 