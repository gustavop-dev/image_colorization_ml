# Image Colorization ML Project

This project implements an image colorization system using deep learning techniques. It consists of a Django backend that serves a REST API and a Vue.js frontend for user interaction.

## Project Overview

The system allows users to upload grayscale images and receive colorized versions using a deep learning model based on autoencoders. The project is designed as a web application with the following components:

- **Backend**: Django REST API that handles image processing and model inference
- **Frontend**: Vue.js application that provides a user interface for image uploads and results display
- **ML Model**: A deep learning model that adds color to grayscale images

## Project Structure

```
image_colorization_ml/
├── backend/               # Django backend
│   ├── colorizer/         # Main Django app
│   │   ├── ml_model.py    # ML model implementation
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── urls.py        # API endpoints
│   │   └── views.py       # API view functions
│   ├── config/            # Django project settings
│   ├── media/             # Uploaded and processed images
│   │   ├── images/
│   │   │   ├── colorized/ # Colorized output images
│   │   │   └── original/  # Original uploaded images
│   ├── venv/              # Python virtual environment
│   ├── manage.py          # Django management script
│   └── requirements.txt   # Python dependencies
└── frontend/              # Vue.js frontend (to be implemented)
```

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd image_colorization_ml/backend
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```
   python manage.py migrate
   ```

5. Start the Django development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

The frontend will be implemented with Vue.js (implementation pending).

## API Endpoints

The backend provides the following REST API endpoints:

- `POST /api/upload/` - Upload an image for colorization
- `GET /api/colorize/?id={image_id}` - Get the status of a colorization process
- `GET /api/history/` - Get a list of all processed images
- `GET /api/image/{image_id}/` - Get details for a specific image

## ML Model Details

The colorization model is based on a convolutional autoencoder architecture:

- **Encoder**: Extracts features from grayscale images
- **Decoder**: Reconstructs the color channels

The model uses the LAB color space, where the L channel represents lightness (grayscale) and the A and B channels contain the color information. The model takes the L channel as input and predicts the A and B channels.

## Development Team Responsibilities

- **Backend Team**: Django API development, model integration
- **Frontend Team**: Vue.js interface development
- **ML Team**: Model training, optimization, and deployment

## Future Work

- Implement transfer learning with pre-trained models
- Enhance the model architecture for better colorization
- Add user authentication and result sharing
- Optimize for real-time colorization

## License

[MIT License](LICENSE) 