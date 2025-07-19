<template>
  <div class="relative min-h-screen overflow-hidden bg-gradient-to-br from-gray-50 via-white to-purple-50">
    <!-- Animated background elements -->
    <div class="absolute inset-0 overflow-hidden">
      <!-- Main orbiting gradients -->
      <div ref="gradient1" class="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-purple-300/30 via-pink-300/30 to-transparent rounded-full blur-3xl"></div>
      <div ref="gradient2" class="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-blue-300/30 via-cyan-300/30 to-transparent rounded-full blur-3xl"></div>
      <div ref="gradient3" class="absolute top-1/2 left-1/2 w-96 h-96 bg-gradient-to-br from-indigo-300/20 via-purple-300/20 to-transparent rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2"></div>
      
      <!-- Additional color blobs -->
      <div ref="colorBlob1" class="absolute top-20 right-1/3 w-80 h-80 bg-gradient-to-br from-pink-400/20 via-rose-300/20 to-transparent rounded-full blur-3xl"></div>
      <div ref="colorBlob2" class="absolute bottom-1/4 left-1/4 w-72 h-72 bg-gradient-to-tr from-violet-400/20 via-purple-300/20 to-transparent rounded-full blur-3xl"></div>
      <div ref="colorBlob3" class="absolute top-1/3 right-1/4 w-64 h-64 bg-gradient-to-bl from-cyan-400/20 via-blue-300/20 to-transparent rounded-full blur-3xl"></div>
      <div ref="colorBlob4" class="absolute bottom-1/3 right-1/2 w-56 h-56 bg-gradient-to-tl from-amber-300/15 via-yellow-300/15 to-transparent rounded-full blur-3xl"></div>
      <div ref="colorBlob5" class="absolute top-2/3 left-1/3 w-48 h-48 bg-gradient-to-br from-emerald-300/15 via-teal-300/15 to-transparent rounded-full blur-3xl"></div>
      
      <!-- Particles container -->
      <div ref="particlesContainer" class="absolute inset-0"></div>
      
      <!-- Subtle grid pattern -->
      <div class="absolute inset-0 grid-pattern opacity-50"></div>
    </div>

    <!-- Main content -->
    <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-8">
      <!-- Animated logo -->
      <div ref="titleContainer" class="mb-8">
        <h1 class="text-8xl font-black">
          <span ref="chromaText" class="text-gray-900 cursor-default">Chroma</span>
          <span ref="flowText" class="text-transparent bg-clip-text animated-gradient-text">Flow</span>
        </h1>
        <div ref="underline" class="h-2 animated-gradient-bg rounded-full mt-2 w-0"></div>
      </div>
      
      <!-- Subtitle -->
      <p ref="subtitle" class="text-xl text-gray-600 mb-16 text-center max-w-lg leading-relaxed opacity-0">
        Transforma tus memorias en blanco y negro en obras maestras llenas de color con inteligencia artificial
      </p>

      <!-- Modern drop area -->
      <div
        ref="dropZone"
        @drop="handleDrop"
        @dragover.prevent
        @dragenter.prevent="handleDragEnter"
        @dragleave.prevent="handleDragLeave"
        class="relative w-full max-w-2xl opacity-0"
        :class="{ 'pointer-events-none': !isServerReady }"
      >
        <!-- Color shadow -->
        <div class="absolute inset-0 bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 rounded-3xl blur-2xl opacity-20 transform scale-95 animate-pulse"></div>
        
        <!-- Main container -->
        <div class="relative bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl border border-gray-100 p-16 transition-all duration-500 group"
             :class="isServerReady ? 'hover:shadow-3xl hover:scale-[1.02]' : 'opacity-60'">
          
          <!-- Hover effect -->
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-transparent to-pink-500/5 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"
               v-if="isServerReady"></div>
          
          <!-- Server not ready overlay -->
          <div v-if="!isServerReady" class="absolute inset-0 bg-gray-500/10 rounded-3xl flex items-center justify-center">
            <div class="text-center">
              <svg class="w-8 h-8 text-gray-400 mx-auto mb-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <p class="text-gray-500 text-sm font-medium">
                {{ serverError || 'Connecting to server...' }}
              </p>
            </div>
          </div>
          
          <!-- Content -->
          <div class="relative flex flex-col items-center" :class="{ 'opacity-30': !isServerReady }">
            <!-- Animated icon -->
            <div ref="uploadIcon" class="mb-8 relative">
              <div class="absolute inset-0 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full blur-xl opacity-30 scale-150"></div>
              <div class="relative bg-gradient-to-br from-purple-100 to-pink-100 p-6 rounded-2xl">
                <svg class="w-16 h-16 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
              </div>
            </div>

            <!-- Main text -->
            <h3 class="text-3xl font-bold text-gray-800 mb-3">
              {{ isServerReady ? 'Arrastra tu imagen aquí' : 'Preparando servidor...' }}
            </h3>
            
            <!-- Secondary text -->
            <p class="text-gray-500 text-lg mb-6">
              <span v-if="isServerReady">
                o haz <span class="text-purple-600 font-semibold cursor-pointer hover:text-purple-700 transition-colors">clic para explorar</span>
              </span>
              <span v-else class="text-gray-400">
                {{ serverError || 'Conectando con el servidor de IA...' }}
              </span>
            </p>

            <!-- Format pills -->
            <div class="flex flex-wrap justify-center gap-2">
              <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">JPG</span>
              <span class="px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-sm font-medium">PNG</span>
              <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">WEBP</span>
              <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">Max: 5MB</span>
            </div>

            <!-- Hidden input -->
            <input
              type="file"
              @change="handleFileSelect"
              accept="image/*"
              :disabled="!isServerReady"
              class="absolute inset-0 w-full h-full opacity-0"
              :class="isServerReady ? 'cursor-pointer' : 'cursor-not-allowed'"
            />
          </div>
        </div>
      </div>

      <!-- Floating features -->
      <div ref="features" class="mt-16 flex flex-wrap justify-center gap-6 opacity-0">
        <div class="flex items-center gap-2 text-gray-600">
          <div class="w-2 h-2 bg-purple-400 rounded-full"></div>
          <span class="text-sm">Procesamiento instantáneo</span>
        </div>
        <div class="flex items-center gap-2 text-gray-600">
          <div class="w-2 h-2 bg-pink-400 rounded-full"></div>
          <span class="text-sm">Colores vibrantes</span>
        </div>
        <div class="flex items-center gap-2 text-gray-600">
          <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
          <span class="text-sm">Alta precisión</span>
        </div>
        <div class="flex items-center gap-2 text-gray-600">
          <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          <span class="text-sm">Hasta 5MB</span>
        </div>
      </div>
    </div>

    <!-- Server status indicator -->
    <div v-if="!isServerReady && healthStore.isInitialized" 
         class="fixed top-4 right-4 z-40 bg-yellow-100 border border-yellow-300 text-yellow-800 px-4 py-2 rounded-lg shadow-lg">
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <span class="text-sm font-medium">{{ serverError || 'Connecting to server...' }}</span>
      </div>
    </div>

    <!-- File size notification -->
    <div v-if="selectedFile && !error" 
         class="fixed top-4 right-4 z-40 bg-blue-100 border border-blue-300 text-blue-800 px-4 py-2 rounded-lg shadow-lg max-w-sm">
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"></path>
        </svg>
        <div class="text-sm">
          <div class="font-medium">{{ selectedFile.name }}</div>
          <div class="text-blue-600">{{ selectedFile.size }}</div>
        </div>
      </div>
    </div>

    <!-- Error notification -->
    <div v-if="error" 
         class="fixed top-4 right-4 z-40 bg-red-100 border border-red-300 text-red-800 px-4 py-2 rounded-lg shadow-lg max-w-sm">
      <div class="flex items-center gap-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <span class="text-sm">{{ error }}</span>
        <button @click="error = null" class="ml-2 text-red-600 hover:text-red-800">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Drag modal -->
    <DragModal v-if="isDragging && isServerReady" />

    <!-- Progress modal -->
    <ColorizationProgress 
      v-if="showProgress"
      :progress="currentProgress"
      :current-step="currentStep"
      @cancel="handleCancelProgress"
    />

    <!-- Result modal -->
    <ColorizationResult 
      v-if="showResult"
      :original-image="colorizationStore.originalImage"
      :colorized-image="colorizationStore.colorizedImage"
      @download="handleDownload"
      @try-another="handleTryAnother"
      @close="handleCloseResult"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { gsap } from 'gsap'
import DragModal from '@/components/home/DragModal.vue'
import ColorizationProgress from '@/components/home/ColorizationProgress.vue'
import ColorizationResult from '@/components/home/ColorizationResult.vue'
import { colorizationStore, healthStore } from '@/stores'

// Refs
const isDragging = ref(false)
const gradient1 = ref(null)
const gradient2 = ref(null)
const gradient3 = ref(null)
const colorBlob1 = ref(null)
const colorBlob2 = ref(null)
const colorBlob3 = ref(null)
const colorBlob4 = ref(null)
const colorBlob5 = ref(null)
const particlesContainer = ref(null)
const titleContainer = ref(null)
const chromaText = ref(null)
const flowText = ref(null)
const underline = ref(null)
const subtitle = ref(null)
const dropZone = ref(null)
const uploadIcon = ref(null)
const features = ref(null)
// Drag counter for nested drags
const dragCounter = ref(0)

// Modal states
const showProgress = ref(false)
const showResult = ref(false)
const currentProgress = ref(0)
const currentStep = ref(0)

// Error state
const error = ref(null)

// File preview state
const selectedFile = ref(null)
const showFilePreview = ref(false)

// Computed properties
const isServerReady = computed(() => healthStore.isReadyForColorization())
const serverError = computed(() => healthStore.error)

// Handlers
const handleDrop = async (e) => {
  e.preventDefault()
  dragCounter.value = 0
  isDragging.value = false
  
  const files = e.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    
    // Store file info
    selectedFile.value = {
      file: file,
      name: file.name,
      size: formatFileSize(file.size),
      type: file.type
    }
    
    // Immediate validation
    if (!validateFileSize(file)) {
      error.value = `File too large: ${selectedFile.value.size}. Maximum allowed: 5MB.`;
      selectedFile.value = null;
      return;
    }
    
    await processImageFile(file)
    selectedFile.value = null
  }
}

const handleDragEnter = (e) => {
  // Only allow drag if server is ready
  if (!isServerReady.value) {
    return
  }
  
  dragCounter.value++
  isDragging.value = true
  
  // Clear any previous errors when starting a new drag
  if (error.value) {
    error.value = null
  }
  
  gsap.to(dropZone.value, {
    scale: 1.05,
    duration: 0.3,
    ease: "power2.out"
  })
}

const handleDragLeave = () => {
  dragCounter.value--
  if (dragCounter.value <= 0) {
    dragCounter.value = 0
    isDragging.value = false
  }
  gsap.to(dropZone.value, {
    scale: 1,
    duration: 0.3,
    ease: "power2.out"
  })
}

const handleFileSelect = async (e) => {
  const file = e.target.files[0]
  if (file) {
    // Store file info for preview
    selectedFile.value = {
      file: file,
      name: file.name,
      size: formatFileSize(file.size),
      type: file.type
    }
    
    // Immediate validation
    if (!validateFileSize(file)) {
      error.value = `File too large: ${selectedFile.value.size}. Maximum allowed: 5MB.`;
      selectedFile.value = null;
      e.target.value = '';
      return;
    }
    
    // Process immediately for better UX
    await processImageFile(file)
    
    // Clear the input so the same file can be selected again
    e.target.value = ''
    selectedFile.value = null
  }
}

// File size validation helper
const validateFileSize = (file) => {
  const maxSize = 5 * 1024 * 1024; // 5MB in bytes
  return file.size <= maxSize;
}

// Format file size for display
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Main image processing function
const processImageFile = async (file) => {
  // Check if server is ready
  if (!isServerReady.value) {
    error.value = serverError.value || 'Server is not ready. Please wait...'
    return
  }

  // Immediate file size validation with user-friendly message
  if (!validateFileSize(file)) {
    const fileSize = formatFileSize(file.size);
    error.value = `File too large: ${fileSize}. Maximum allowed: 5MB. Please choose a smaller image.`;
    return
  }
  
  try {
    // Reset states
    error.value = null
    currentProgress.value = 0
    currentStep.value = 0
    showProgress.value = true
    
    // Simulate progress steps
    simulateProgress()
    
    // Process the image
    const result = await colorizationStore.colorizeImage(file)
    
    if (result) {
      // Success - ensure we reach 100% and final step
      currentProgress.value = 100
      currentStep.value = 4
      
      // Show completion for a moment before transitioning
      setTimeout(() => {
        showProgress.value = false
        showResult.value = true
      }, 1200)
    } else {
      // Error occurred
      throw new Error(colorizationStore.error || 'Failed to process image')
    }
    
  } catch (err) {
    showProgress.value = false
    clearProgressSimulation()
    error.value = err.message || 'An error occurred while processing the image'
    console.error('Image processing error:', err)
  }
}

// Smart progress simulation that syncs with real processing
const simulateProgress = () => {
  let step = 0
  const steps = [
    { progress: 15, step: 0, minTime: 500 },   // Analyzing image structure
    { progress: 35, step: 1, minTime: 800 },   // Detecting objects and features
    { progress: 60, step: 2, minTime: 1200 },  // Applying AI colorization
    { progress: 85, step: 3, minTime: 1000 }   // Enhancing color vibrancy
  ]
  
  const advanceStep = () => {
    if (step < steps.length) {
      currentProgress.value = steps[step].progress
      currentStep.value = steps[step].step
      
      // Wait minimum time for this step
      setTimeout(() => {
        step++
        advanceStep()
      }, steps[step]?.minTime || 500)
    }
  }
  
  advanceStep()
}

const clearProgressSimulation = () => {
  // No need to clear intervals anymore since we use timeouts
  currentProgress.value = 0
  currentStep.value = 0
}

// Result handlers
const handleDownload = () => {
  colorizationStore.downloadColorizedImage()
}

const handleTryAnother = () => {
  showResult.value = false
  colorizationStore.clearImages()
}

const handleCloseResult = () => {
  showResult.value = false
  colorizationStore.clearImages()
}

const handleCancelProgress = () => {
  showProgress.value = false
  clearProgressSimulation()
  colorizationStore.clearImages()
  // TODO: Cancel actual image processing request if possible
}

// Create particles dynamically
const createParticles = () => {
  if (!particlesContainer.value) return
  
  const colors = [
    'from-purple-400/60 to-purple-600/60',
    'from-pink-400/50 to-pink-600/50',
    'from-blue-400/50 to-blue-600/50',
    'from-emerald-400/40 to-emerald-600/40',
    'from-amber-400/40 to-amber-600/40'
  ]
  
  const sizes = ['w-3 h-3', 'w-2 h-2', 'w-2 h-2', 'w-1 h-1', 'w-2 h-2']
  
  for (let i = 0; i < 30; i++) {
    const particle = document.createElement('div')
    const colorIndex = i % 5
    particle.className = `absolute rounded-full bg-gradient-to-br ${colors[colorIndex]} ${sizes[colorIndex]}`
    particle.style.left = `${Math.random() * 100}%`
    particle.style.top = `${Math.random() * 100}%`
    particlesContainer.value.appendChild(particle)
    
    // Animate particle
    gsap.to(particle, {
      x: Math.random() * 200 - 100,
      y: Math.random() * 200 - 100,
      duration: 15 + Math.random() * 20,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      delay: i * 0.1
    })
    
    gsap.to(particle, {
      rotate: 360 * (Math.random() > 0.5 ? 1 : -1),
      scale: 0.5 + Math.random(),
      duration: 10 + Math.random() * 15,
      repeat: -1,
      yoyo: true,
      ease: "power1.inOut",
      delay: i * 0.05
    })
  }
}

// Animations
onMounted(() => {
  // Create particles
  createParticles()
  
  // Main timeline
  const tl = gsap.timeline()
  
  // Entry animation
  tl.from(chromaText.value, {
    x: -100,
    opacity: 0,
    duration: 0.8,
    ease: "power4.out"
  })
  .from(flowText.value, {
    x: 100,
    opacity: 0,
    duration: 0.8,
    ease: "power4.out"
  }, "-=0.6")
  .to(underline.value, {
    width: "100%",
    duration: 0.8,
    ease: "power2.inOut"
  }, "-=0.4")
  .to(subtitle.value, {
    opacity: 1,
    y: -20,
    duration: 0.6,
    ease: "power2.out"
  })
  .to(dropZone.value, {
    opacity: 1,
    y: -20,
    duration: 0.8,
    ease: "power3.out"
  })
  .to(features.value, {
    opacity: 1,
    y: -10,
    duration: 0.6,
    ease: "power2.out"
  })
  
  // Gradient animation
  gsap.to(gradient1.value, {
    x: 100,
    y: 100,
    duration: 20,
    repeat: -1,
    yoyo: true,
    ease: "none"
  })
  
  gsap.to(gradient2.value, {
    x: -100,
    y: -100,
    duration: 25,
    repeat: -1,
    yoyo: true,
    ease: "none"
  })
  
  gsap.to(gradient3.value, {
    x: 50,
    y: -50,
    duration: 30,
    repeat: -1,
    yoyo: true,
    ease: "none"
  })
  
  // Color blobs animation
  const animateBlob = (element, duration) => {
    gsap.to(element, {
      x: gsap.utils.random(-150, 150),
      y: gsap.utils.random(-150, 150),
      scale: gsap.utils.random(0.7, 1.3),
      duration: duration,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    })
  }
  
  animateBlob(colorBlob1.value, gsap.utils.random(15, 25))
  animateBlob(colorBlob2.value, gsap.utils.random(20, 30))
  animateBlob(colorBlob3.value, gsap.utils.random(18, 28))
  animateBlob(colorBlob4.value, gsap.utils.random(22, 32))
  animateBlob(colorBlob5.value, gsap.utils.random(25, 35))
  
  // Floating icon animation
  gsap.to(uploadIcon.value, {
    y: -10,
    duration: 2,
    repeat: -1,
    yoyo: true,
    ease: "power1.inOut"
  })
  
  // Improved hover
  const dropZoneEl = dropZone.value?.querySelector('.group')
  if (dropZoneEl) {
    dropZoneEl.addEventListener('mouseenter', () => {
      gsap.to(uploadIcon.value, {
        scale: 1.1,
        rotate: 5,
        duration: 0.3
      })
    })
    
    dropZoneEl.addEventListener('mouseleave', () => {
      gsap.to(uploadIcon.value, {
        scale: 1,
        rotate: 0,
        duration: 0.3
      })
    })
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

* {
  font-family: 'Outfit', sans-serif;
}

/* Custom shadow */
.shadow-3xl {
  box-shadow: 0 35px 60px -15px rgba(0, 0, 0, 0.1),
              0 0 40px -10px rgba(147, 51, 234, 0.1),
              0 0 40px -10px rgba(236, 72, 153, 0.1);
}

/* Grid pattern */
.grid-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='grid' width='60' height='60' patternUnits='userSpaceOnUse'%3E%3Cpath d='M 60 0 L 0 0 0 60' fill='none' stroke='%23e5e7eb' stroke-width='0.5'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23grid)' /%3E%3C/svg%3E");
}

/* Animated gradient for text */
.animated-gradient-text {
  background: linear-gradient(90deg, #c4b5fd 0%, #f9a8d4 50%, #c4b5fd 100%);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  animation: gradient-shift 10s ease-in-out infinite alternate;
  text-shadow: 0 0 2px rgba(0,0,0,0.05);
}

/* Animated gradient for underline */
.animated-gradient-bg {
  background: linear-gradient(90deg, #c4b5fd 0%, #f9a8d4 50%, #c4b5fd 100%);
  background-size: 300% 100%;
  animation: gradient-shift 10s ease-in-out infinite alternate;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 200% 0%;
  }
}
</style>