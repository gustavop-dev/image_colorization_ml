<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-md">
    <!-- Contenedor principal -->
    <div ref="container" class="relative bg-white/95 backdrop-blur-xl rounded-3xl p-12 shadow-2xl max-w-lg w-full mx-8 opacity-0 scale-90">
      
      <!-- Gradiente de fondo animado -->
      <div ref="bgGradient" class="absolute inset-0 bg-gradient-to-br from-purple-400/20 via-pink-400/20 to-blue-400/20 rounded-3xl blur-2xl"></div>
      
      <!-- Contenido -->
      <div class="relative z-10 text-center space-y-8">
        
        <!-- Icono de cerebro de IA animado -->
        <div ref="iconContainer" class="relative mx-auto w-24 h-24">
          <!-- Anillos pulsantes -->
          <div ref="ring1" class="absolute inset-0 bg-purple-400/30 rounded-full"></div>
          <div ref="ring2" class="absolute inset-0 bg-pink-400/30 rounded-full"></div>
          <div ref="ring3" class="absolute inset-0 bg-blue-400/30 rounded-full"></div>
          
          <!-- Icono principal -->
          <div ref="mainIcon" class="relative bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-5 shadow-lg">
            <svg class="w-14 h-14 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
          </div>
        </div>

        <!-- Título principal con efecto de escritura -->
        <div>
          <h2 ref="title" class="text-3xl font-bold text-gray-800 mb-2">
            {{ currentTitle }}
          </h2>
          <p ref="subtitle" class="text-gray-600 text-lg">
            {{ currentSubtitle }}
          </p>
        </div>

        <!-- Barra de progreso -->
        <div class="space-y-4">
          <div ref="progressContainer" class="relative bg-gray-200 rounded-full h-3 overflow-hidden">
            <div ref="progressBar" class="absolute left-0 top-0 h-full bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 rounded-full transition-all duration-300 ease-out"
                 :style="{ width: `${progress}%` }">
            </div>
                         <!-- Efecto de brillo -->
             <div ref="progressShine" class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent transform -translate-x-full">
             </div>
           </div>
           
           <!-- Texto de progreso -->
          <div class="flex justify-between text-sm text-gray-500">
            <span>{{ progressText }}</span>
            <span>{{ progress }}%</span>
          </div>
        </div>

        <!-- Pasos del procesamiento -->
        <div ref="stepsContainer" class="space-y-3">
          <div v-for="(step, index) in steps" :key="index" 
               :ref="el => stepElements[index] = el"
               class="flex items-center space-x-3 text-left opacity-30 transition-all duration-500"
               :class="{ 'opacity-100 text-purple-600': currentStep >= index }">
            <div class="w-6 h-6 rounded-full border-2 transition-all duration-300"
                 :class="currentStep > index ? 'bg-purple-500 border-purple-500' : 
                         currentStep === index ? 'border-purple-500 animate-pulse' : 'border-gray-300'">
              <svg v-if="currentStep > index" class="w-4 h-4 text-white m-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <span class="font-medium">{{ step }}</span>
          </div>
        </div>

        <!-- Botón de cancelar -->
        <button 
          @click="$emit('cancel')"
          ref="cancelBtn"
          class="px-6 py-2 text-gray-500 hover:text-gray-700 transition-colors duration-200 font-medium">
          Cancelar
        </button>
      </div>

      <!-- Partículas flotantes -->
      <div ref="particlesContainer" class="absolute inset-0 pointer-events-none">
        <div v-for="i in 20" :key="i" 
             :ref="el => particles[i-1] = el"
             class="absolute w-2 h-2 rounded-full opacity-0"
             :class="getParticleClass(i)">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { gsap } from 'gsap'

// Props
const props = defineProps({
  progress: {
    type: Number,
    default: 0
  },
  currentStep: {
    type: Number,
    default: 0
  }
})

// Emits
const emit = defineEmits(['cancel'])

// Refs
const container = ref(null)
const bgGradient = ref(null)
const iconContainer = ref(null)
const ring1 = ref(null)
const ring2 = ref(null)
const ring3 = ref(null)
const mainIcon = ref(null)
const title = ref(null)
const subtitle = ref(null)
const progressContainer = ref(null)
const progressBar = ref(null)
const progressShine = ref(null)
const stepsContainer = ref(null)
const stepElements = ref([])
const cancelBtn = ref(null)
const particlesContainer = ref(null)
const particles = ref([])

// Data
const steps = [
  'Analizando estructura de la imagen',
  'Detectando objetos y características', 
  'Aplicando colorización con IA',
  'Mejorando vibración del color',
  'Finalizando tu obra maestra'
]

const titles = [
  'Procesando tu imagen...',
  'La IA está trabajando su magia...',
  'Añadiendo colores vibrantes...',
  'Casi listo...',
  '¡Creando tu obra maestra!'
]

const subtitles = [
  'Nuestra IA está analizando tu imagen',
  'Colorización inteligente en progreso', 
  'Aplicando hermosas paletas de colores',
  'Ajustando los detalles finales',
  '¡Tu imagen colorizada está lista!'
]

// Computed
const currentTitle = computed(() => titles[props.currentStep] || titles[0])
const currentSubtitle = computed(() => subtitles[props.currentStep] || subtitles[0])
const progressText = computed(() => steps[props.currentStep] || 'Procesando...')

// Methods
const getParticleClass = (index) => {
  const classes = [
    'bg-purple-400',
    'bg-pink-400', 
    'bg-blue-400',
    'bg-indigo-400',
    'bg-violet-400'
  ]
  return classes[index % classes.length]
}

// Watch progress changes
watch(() => props.progress, (newProgress) => {
  // Animate progress shine
  if (newProgress > 0) {
    gsap.fromTo(progressShine.value, 
      { x: '-100%' },
      { x: '100%', duration: 1, ease: 'power2.out' }
    )
  }
})

// Watch step changes
watch(() => props.currentStep, (newStep) => {
  // Animate step completion
  if (stepElements.value[newStep]) {
    gsap.to(stepElements.value[newStep], {
      scale: 1.05,
      duration: 0.2,
      yoyo: true,
      repeat: 1
    })
  }
})

onMounted(() => {
  // Entry animation
  const tl = gsap.timeline()
  
  tl.to(container.value, {
    opacity: 1,
    scale: 1,
    duration: 0.5,
    ease: 'back.out(1.2)'
  })
  .to(mainIcon.value, {
    rotate: 360,
    duration: 0.8,
    ease: 'power2.out'
  }, '-=0.3')

  // Background gradient animation
  gsap.to(bgGradient.value, {
    scale: 1.1,
    duration: 3,
    repeat: -1,
    yoyo: true,
    ease: 'sine.inOut'
  })

  // Pulsing rings animation
  const ringsTimeline = gsap.timeline({ repeat: -1 })
  ringsTimeline
    .to(ring1.value, { scale: 2, opacity: 0, duration: 2 })
    .to(ring2.value, { scale: 2, opacity: 0, duration: 2 }, '-=1.5')
    .to(ring3.value, { scale: 2, opacity: 0, duration: 2 }, '-=1.5')

  // Main icon floating animation
  gsap.to(mainIcon.value, {
    y: -10,
    duration: 2,
    repeat: -1,
    yoyo: true,
    ease: 'sine.inOut'
  })

  // Particles animation
  particles.value.forEach((particle, i) => {
    if (particle) {
      gsap.set(particle, {
        left: '50%',
        top: '50%',
        x: '-50%',
        y: '-50%'
      })
      
      const angle = (i / particles.value.length) * Math.PI * 2
      const radius = 100 + Math.random() * 50
      
      gsap.to(particle, {
        opacity: 0.6,
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        duration: 3 + Math.random() * 2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: i * 0.1
      })
    }
  })
})
</script> 