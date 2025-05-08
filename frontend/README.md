# Image Colorization Frontend

This directory contains the Vue.js frontend for the Image Colorization project.

## Planned Features

- Modern, responsive UI built with Vue.js
- Image upload interface
- Before/after image comparison
- Image gallery with colorization history
- Progressive Web App (PWA) capabilities

## Setup Instructions

1. Initialize a Vue.js project:
   ```
   vue create .
   ```
   Or using Vite:
   ```
   npm init vue@latest
   ```

2. Install dependencies:
   ```
   npm install axios vue-router vuetify
   ```

3. Set up API connection to the Django backend

4. Start the development server:
   ```
   npm run dev
   ```

## Frontend Structure

```
frontend/
├── public/            # Static assets
├── src/               # Source files
│   ├── assets/        # Images, fonts, etc.
│   │   ├── ImageUpload.vue
│   │   ├── ImageViewer.vue
│   │   └── ...
│   ├── views/         # Page components
│   │   ├── Home.vue
│   │   ├── Gallery.vue
│   │   └── ...
│   ├── router/        # Vue Router configuration
│   ├── App.vue        # Root component
│   └── main.js        # Entry point
├── .gitignore
├── package.json       # NPM dependencies
└── README.md          # This file
```

## API Connection

The frontend will communicate with the Django backend at these endpoints:

- `POST /api/upload/` - Upload an image for colorization
- `GET /api/colorize/?id={image_id}` - Get the status of a colorization process
- `GET /api/history/` - Get a list of all processed images
- `GET /api/image/{image_id}/` - Get details for a specific image
