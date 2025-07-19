import { reactive } from 'vue';
import { upload_request } from './services/request_http.js';

// Reactive state of the store
const state = reactive({
  isLoading: false,
  originalImage: null,
  colorizedImage: null,
  error: null,
  uploadProgress: 0
});

/**
 * Store to handle image colorization
 */
export const colorizationStore = {
  // Getters to access the state
  get isLoading() {
    return state.isLoading;
  },
  
  get originalImage() {
    return state.originalImage;
  },
  
  get colorizedImage() {
    return state.colorizedImage;
  },
  
  get error() {
    return state.error;
  },
  
  get uploadProgress() {
    return state.uploadProgress;
  },

  /**
   * Uploads and colorizes an image
   * @param {File} imageFile - Image file to colorize
   * @returns {Promise<string|null>} URL of the colorized image or null if error
   */
  async colorizeImage(imageFile) {
    // Previous validations
    if (!imageFile) {
      this.setError('No image file has been provided');
      return null;
    }

    // Validate size (5MB maximum for better UX)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (imageFile.size > maxSize) {
      this.setError('File is too large. Maximum allowed: 5MB');
      return null;
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
    if (!allowedTypes.includes(imageFile.type)) {
      this.setError('Unsupported file format. Use JPG, JPEG, PNG or BMP');
      return null;
    }

    try {
      this.setLoading(true);
      this.clearError();
      this.setUploadProgress(0);

      // Save original image
      state.originalImage = URL.createObjectURL(imageFile);

      // Prepare FormData
      const formData = new FormData();
      formData.append('image', imageFile);

      this.setUploadProgress(50);

      // Send request
      const response = await upload_request('colorize/', formData);

      this.setUploadProgress(100);

      // Create URL for the colorized image
      const imageBlob = new Blob([response.data], { type: response.headers['content-type'] || 'image/jpeg' });
      const colorizedImageUrl = URL.createObjectURL(imageBlob);
      
      state.colorizedImage = colorizedImageUrl;

      return colorizedImageUrl;

    } catch (error) {
      console.error('Error colorizing image:', error);
      
      // Handle different types of errors
      if (error.response) {
        // Server responded with an error code
        const status = error.response.status;
        
        if (status === 400) {
          this.setError('Invalid image file or file too large');
        } else if (status === 503) {
          this.setError('Colorization service is not available. Please try again later');
        } else if (status === 500) {
          this.setError('Internal server error. Please try again later');
        } else {
          this.setError('Server error: ' + (error.response.data?.error || 'Unknown error'));
        }
      } else if (error.request) {
        // No response received from server
        this.setError('Could not connect to server. Please check your connection');
      } else {
        // Error in request configuration
        this.setError('Request error: ' + error.message);
      }

      return null;
    } finally {
      this.setLoading(false);
      this.setUploadProgress(0);
    }
  },

  /**
   * Clears images and resets state
   */
  clearImages() {
    // Release object URLs to avoid memory leaks
    if (state.originalImage) {
      URL.revokeObjectURL(state.originalImage);
      state.originalImage = null;
    }
    
    if (state.colorizedImage) {
      URL.revokeObjectURL(state.colorizedImage);
      state.colorizedImage = null;
    }
    
    this.clearError();
    state.uploadProgress = 0;
  },

  /**
   * Downloads the colorized image
   * @param {string} filename - File name (optional)
   */
  downloadColorizedImage(filename = 'colorized_image.jpg') {
    if (!state.colorizedImage) {
      this.setError('No colorized image available for download');
      return;
    }

    try {
      const link = document.createElement('a');
      link.href = state.colorizedImage;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading image:', error);
      this.setError('Error downloading the image');
    }
  },

  // Helper methods to modify state
  setLoading(loading) {
    state.isLoading = loading;
  },

  setError(error) {
    state.error = error;
  },

  clearError() {
    state.error = null;
  },

  setUploadProgress(progress) {
    state.uploadProgress = progress;
  }
}; 