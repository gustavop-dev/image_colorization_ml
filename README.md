# Image Colorization ML Project

This project implements an image colorization system using deep learning techniques. It consists of a Django backend that serves a REST API and a Vue.js frontend for user interaction.

## Project Overview

The system allows users to upload grayscale images and receive colorized versions using a deep learning model based on autoencoders. The project is designed as a web application with the following components:

- **Backend**: Django REST API that handles image processing and model inference
- **Frontend**: Vue.js application that provides a user interface for image uploads and results display
- **ML Model**: A deep learning model that adds color to grayscale images

## 🚀 Live Demo

**Try the application online:** [https://colorizer.projectapp.co/](https://colorizer.projectapp.co/)

> **💡 Tip:** For optimal performance and faster response times, please use images smaller than **1 MB**. Larger images may take significantly longer to process.

## Project Structure

```
image_colorization_ml/
├── backend/                    # Django backend
│   ├── colorizer/              # Main Django app
│   │   ├── ml/                 # Machine Learning module
│   │   │   ├── trained_models/ # Pre-trained model files
│   │   │   │   └── colorization_model.h5
│   │   │   ├── inference/      # Model inference logic
│   │   │   ├── training/       # Model training scripts
│   │   │   ├── data/           # Data processing utilities
│   │   │   ├── models/         # Model architecture definitions
│   │   │   ├── services.py     # ML service functions
│   │   │   ├── config.py       # ML configuration settings
│   │   │   └── core.py         # Core ML functionality
│   │   ├── views/              # API view functions
│   │   ├── migrations/         # Database migrations
│   │   ├── ml_model.py         # ML model interface
│   │   ├── utils.py            # Utility functions
│   │   ├── urls.py             # API endpoints
│   │   ├── admin.py            # Django admin configuration
│   │   └── apps.py             # App configuration
│   ├── config/                 # Django project settings
│   ├── venv/                   # Python virtual environment
│   ├── db.sqlite3              # SQLite database
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Vue.js frontend
│   ├── src/                    # Source code
│   │   ├── components/         # Vue components
│   │   ├── views/              # Vue views/pages
│   │   ├── router/             # Vue router configuration
│   │   ├── stores/             # Pinia state management
│   │   ├── styles/             # CSS/SCSS styles
│   │   ├── App.vue             # Main Vue component
│   │   └── main.js             # Application entry point
│   ├── public/                 # Static assets
│   ├── node_modules/           # Node.js dependencies
│   ├── package.json            # Node.js dependencies and scripts
│   ├── package-lock.json       # Dependency lock file
│   ├── vite.config.js          # Vite configuration
│   ├── index.html              # HTML template
│   └── jsconfig.json           # JavaScript configuration
├── .git/                       # Git repository data
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## Installation & Setup

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **Git** (for cloning the repository)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd image_colorization_ml/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000` (or the port specified in the console output).

### Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd image_colorization_ml/backend
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

#### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Download and Setup ML Model

1. **Download the trained model** from: https://drive.google.com/drive/folders/1iVUZJYrOvRmwf1YSTzSh7aGSSEKmpF28?usp=drive_link

2. **Create the trained_models directory** (if it doesn't exist):
   
   **Windows:**
   ```bash
   mkdir colorizer\ml\trained_models
   ```
   
   **Linux/Mac:**
   ```bash
   mkdir -p colorizer/ml/trained_models
   ```

3. **Move the downloaded model file** (`colorization_model.h5`) to:
   ```
   backend/colorizer/ml/trained_models/colorization_model.h5
   ```

#### Step 6: Run Database Migrations
```bash
python manage.py migrate
```

#### Step 7: Start Django Development Server
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`.

### Complete Setup Verification

After setting up both frontend and backend:

1. **Backend**: Visit `http://localhost:8000/admin` to verify Django is running
2. **Frontend**: Visit `http://localhost:3000` to access the web interface
3. **API**: Test the API endpoints at `http://localhost:8000/api/`

### Troubleshooting

- **Virtual Environment Issues**: Make sure you're in the correct directory when creating/activating the virtual environment
- **Model Download**: Ensure the model file is exactly named `colorization_model.h5` and placed in the correct directory
- **Port Conflicts**: If ports 3000 or 8000 are occupied, the applications will suggest alternative ports
- **Python Version**: Ensure you're using Python 3.8 or higher for compatibility with the ML libraries
- **"Backend Not Ready" Message**: If you see a message on the web interface indicating that the backend is not ready:
  1. **Stop the Django server** (Ctrl+C)
  2. **Verify all dependencies** are installed: `pip install -r requirements.txt`
  3. **Check the model file** is in the correct location: `backend/colorizer/ml/trained_models/colorization_model.h5`
  4. **Restart the server**: `python manage.py runserver`
  5. **Wait 30-60 seconds** for the model to load completely before testing again

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