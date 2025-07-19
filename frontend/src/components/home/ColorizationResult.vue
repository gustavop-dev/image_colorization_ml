<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-md">
    <!-- Main container -->
    <div ref="container" class="relative bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl max-w-6xl w-full mx-8 p-8 opacity-0 scale-90">
      
      <!-- Header -->
      <div ref="header" class="text-center mb-8 opacity-0">
        <h2 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 mb-2">
          ¡Transformación Completada! 🎨
        </h2>
        <p class="text-gray-600 text-lg">
          Tu imagen ha sido colorizada con inteligencia artificial
        </p>
      </div>

      <!-- Images comparison -->
      <div ref="imagesContainer" class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 opacity-0">
        
        <!-- Original Image -->
        <div ref="originalContainer" class="space-y-4">
          <div class="text-center">
            <h3 class="text-xl font-semibold text-gray-700 mb-2">Original</h3>
            <div class="w-16 h-1 bg-gray-400 rounded-full mx-auto"></div>
          </div>
          
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-br from-gray-300/30 to-gray-500/30 rounded-2xl blur-xl opacity-50"></div>
            <div class="relative bg-white rounded-2xl p-4 shadow-xl">
              <img 
                :src="originalImage" 
                :alt="'Original image'"
                class="w-full h-auto rounded-xl shadow-lg transition-transform duration-300 group-hover:scale-[1.02]"
                @load="onOriginalLoad"
              />
            </div>
          </div>
        </div>

        <!-- Colorized Image -->
        <div ref="colorizedContainer" class="space-y-4">
          <div class="text-center">
            <h3 class="text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 mb-2">
              Colorizada
            </h3>
            <div class="w-16 h-1 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full mx-auto"></div>
          </div>
          
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-br from-purple-400/30 via-pink-400/30 to-blue-400/30 rounded-2xl blur-xl opacity-50"></div>
            <div class="relative bg-white rounded-2xl p-4 shadow-xl">
              <img 
                :src="colorizedImage" 
                :alt="'Colorized image'"
                class="w-full h-auto rounded-xl shadow-lg transition-transform duration-300 group-hover:scale-[1.02]"
                @load="onColorizedLoad"
              />
              
              <!-- Success badge -->
              <div ref="successBadge" class="absolute top-6 right-6 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg opacity-0">
                <svg class="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                </svg>
                Listo
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div ref="actionsContainer" class="flex flex-col sm:flex-row gap-4 justify-center items-center opacity-0">
        
        <!-- Download button -->
        <button 
          @click="downloadImage"
          ref="downloadBtn"
          class="flex items-center gap-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 group">
          <svg class="w-5 h-5 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Descargar Imagen
        </button>

        <!-- Try another button -->
        <button 
          @click="$emit('try-another')"
          ref="tryAnotherBtn"
          class="flex items-center gap-2 bg-white text-gray-700 px-8 py-3 rounded-xl font-semibold border-2 border-gray-200 hover:border-purple-300 transition-all duration-300 hover:scale-105 group">
          <svg class="w-5 h-5 group-hover:rotate-180 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Probar Otra
        </button>

        <!-- Close button -->
        <button 
          @click="$emit('close')"
          ref="closeBtn"
          class="text-gray-500 hover:text-gray-700 px-4 py-2 transition-colors duration-200 font-medium">
          Cerrar
        </button>
      </div>

      <!-- Floating celebration particles -->
      <div ref="celebrationContainer" class="absolute inset-0 pointer-events-none">
        <div v-for="i in 25" :key="i" 
             :ref="el => celebrationParticles[i-1] = el"
             class="absolute w-3 h-3 rounded-full opacity-0"
             :class="getCelebrationParticleClass(i)">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

// Props
const props = defineProps({
  originalImage: {
    type: String,
    required: true
  },
  colorizedImage: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['download', 'try-another', 'close'])

// Refs
const container = ref(null)
const header = ref(null)
const imagesContainer = ref(null)
const originalContainer = ref(null)
const colorizedContainer = ref(null)
const actionsContainer = ref(null)
const successBadge = ref(null)
const downloadBtn = ref(null)
const tryAnotherBtn = ref(null)
const closeBtn = ref(null)
const celebrationContainer = ref(null)
const celebrationParticles = ref([])

// State
const originalLoaded = ref(false)
const colorizedLoaded = ref(false)

// Methods
const getCelebrationParticleClass = (index) => {
  const classes = [
    'bg-purple-400',
    'bg-pink-400', 
    'bg-blue-400',
    'bg-yellow-400',
    'bg-green-400',
    'bg-indigo-400',
    'bg-red-400'
  ]
  return classes[index % classes.length]
}

const onOriginalLoad = () => {
  originalLoaded.value = true
  checkIfBothLoaded()
}

const onColorizedLoad = () => {
  colorizedLoaded.value = true
  checkIfBothLoaded()
}

const checkIfBothLoaded = () => {
  if (originalLoaded.value && colorizedLoaded.value) {
    startCelebrationAnimation()
  }
}

const downloadImage = () => {
  emit('download')
  
  // Button feedback animation
  gsap.to(downloadBtn.value, {
    scale: 0.95,
    duration: 0.1,
    yoyo: true,
    repeat: 1
  })
}

const startCelebrationAnimation = () => {
  // Show success badge
  gsap.to(successBadge.value, {
    opacity: 1,
    scale: 1.1,
    duration: 0.5,
    ease: 'back.out(1.3)',
    delay: 0.5
  })

  // Launch celebration particles
  celebrationParticles.value.forEach((particle, i) => {
    if (particle) {
      gsap.set(particle, {
        left: '50%',
        top: '50%',
        x: '-50%',
        y: '-50%'
      })
      
      const angle = (i / celebrationParticles.value.length) * Math.PI * 2
      const distance = 200 + Math.random() * 150
      const duration = 1.5 + Math.random() * 1
      
      gsap.to(particle, {
        opacity: 1,
        x: Math.cos(angle) * distance,
        y: Math.sin(angle) * distance,
        scale: 0.5 + Math.random() * 0.5,
        duration: duration,
        ease: 'power2.out',
        delay: 0.8 + i * 0.02
      })
      
      gsap.to(particle, {
        opacity: 0,
        duration: 0.5,
        delay: 0.8 + duration + i * 0.02
      })
    }
  })
}

onMounted(() => {
  // Entry animation timeline
  const tl = gsap.timeline()
  
  tl.to(container.value, {
    opacity: 1,
    scale: 1,
    duration: 0.6,
    ease: 'back.out(1.2)'
  })
  .to(header.value, {
    opacity: 1,
    y: -10,
    duration: 0.5,
    ease: 'power2.out'
  }, '-=0.3')
  .to(imagesContainer.value, {
    opacity: 1,
    y: -20,
    duration: 0.6,
    ease: 'power2.out'
  }, '-=0.2')
  .to(actionsContainer.value, {
    opacity: 1,
    y: -10,
    duration: 0.5,
    ease: 'power2.out'
  }, '-=0.3')

  // Individual image container animations
  gsap.from(originalContainer.value, {
    x: -50,
    duration: 0.8,
    ease: 'power2.out',
    delay: 0.4
  })
  
  gsap.from(colorizedContainer.value, {
    x: 50,
    duration: 0.8,
    ease: 'power2.out',
    delay: 0.6
  })

  // Button hover effects
  const buttons = [downloadBtn.value, tryAnotherBtn.value]
  buttons.forEach(btn => {
    if (btn) {
      btn.addEventListener('mouseenter', () => {
        gsap.to(btn, { y: -2, duration: 0.2 })
      })
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { y: 0, duration: 0.2 })
      })
    }
  })
})
</script> 