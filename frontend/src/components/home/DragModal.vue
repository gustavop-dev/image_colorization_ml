<template>
    <div ref="modalOverlay" class="fixed inset-0 z-50 pointer-events-none">
      <!-- Overlay with blur effect -->
      <div ref="backdrop" class="absolute inset-0 bg-white/70 backdrop-blur-md"></div>
      
      <!-- Modal content -->
      <div class="relative h-full flex items-center justify-center p-8">
        <div ref="modalContent" class="relative scale-0">
          <!-- Animated glow effect -->
          <div ref="glowEffect" class="absolute inset-0 bg-gradient-to-br from-purple-400 via-pink-400 to-blue-400 rounded-3xl opacity-40 blur-3xl scale-110"></div>
          
          <!-- Main container -->
          <div class="relative bg-white/95 backdrop-blur-xl rounded-3xl border-2 border-dashed border-transparent bg-clip-padding p-20 flex flex-col items-center space-y-8 shadow-2xl overflow-hidden">
            <!-- (Gradient border removed) -->
            
            <!-- Floating decorative elements -->
            <div ref="floatingElements" class="absolute inset-0 pointer-events-none">
              <div ref="float1" class="absolute top-10 left-10 w-20 h-20 bg-gradient-to-br from-purple-200/50 to-transparent rounded-full blur-md"></div>
              <div ref="float2" class="absolute bottom-10 right-10 w-32 h-32 bg-gradient-to-br from-pink-200/50 to-transparent rounded-full blur-md"></div>
              <div ref="float3" class="absolute top-1/2 left-1/3 w-24 h-24 bg-gradient-to-br from-blue-200/50 to-transparent rounded-full blur-md"></div>
            </div>
            
            <!-- Main animated icon (placed behind texts) -->
            <div ref="iconContainer" class="relative z-0">
              <!-- Pulse rings -->
              <div ref="ring1" class="absolute inset-0 bg-purple-400/20 rounded-full scale-0"></div>
              <div ref="ring2" class="absolute inset-0 bg-pink-400/20 rounded-full scale-0"></div>
              <div ref="ring3" class="absolute inset-0 bg-blue-400/20 rounded-full scale-0"></div>
              
              <!-- Central icon -->
              <div ref="mainIcon" class="relative bg-gradient-to-br from-purple-500 to-pink-500 p-8 rounded-3xl shadow-2xl">
                <svg class="w-20 h-20 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
              </div>
            </div>
            
            <!-- Main text -->
            <h2 ref="mainText" class="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 text-center opacity-0 z-10">
              ¡Suéltala aquí!
            </h2>
            
            <!-- Secondary text -->
            <p ref="subText" class="text-xl text-gray-600 text-center max-w-md leading-relaxed opacity-0 z-10">
              Tu imagen está a punto de transformarse en una explosión de colores vibrantes
            </p>
            
            <!-- Animated decorative particles -->
            <div ref="particlesWrapper" class="absolute inset-0 pointer-events-none">
              <div v-for="i in 15" :key="i" 
                   :ref="el => modalParticles[i-1] = el"
                   class="absolute w-3 h-3 rounded-full opacity-0"
                   :class="['bg-gradient-to-br', getParticleGradient(i)]"
                   :style="{
                     left: '50%',
                     top: '50%'
                   }">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { gsap } from 'gsap'
  
  // Refs
  const modalOverlay = ref(null)
  const backdrop = ref(null)
  const modalContent = ref(null)
  const glowEffect = ref(null)
  const floatingElements = ref(null)
  const float1 = ref(null)
  const float2 = ref(null)
  const float3 = ref(null)
  const iconContainer = ref(null)
  const ring1 = ref(null)
  const ring2 = ref(null)
  const ring3 = ref(null)
  const mainIcon = ref(null)
  const mainText = ref(null)
  const subText = ref(null)
  const modalParticles = ref([])
  
  // Helper to get random gradients for particles
  const getParticleGradient = (index) => {
    const gradients = [
      'from-purple-400 to-purple-600',
      'from-pink-400 to-pink-600',
      'from-blue-400 to-blue-600',
      'from-indigo-400 to-indigo-600',
      'from-violet-400 to-violet-600'
    ]
    return gradients[index % gradients.length]
  }
  
  onMounted(() => {
    // Entry timeline
    const tl = gsap.timeline()
    
    // Modal entry animation
    tl.to(modalContent.value, {
      scale: 1,
      duration: 0.5,
      ease: "back.out(1.5)"
    })
    .to(mainIcon.value, {
      rotate: 360,
      duration: 0.8,
      ease: "power2.out"
    }, "-=0.3")
    .to(mainText.value, {
      opacity: 1,
      y: -10,
      duration: 0.5,
      ease: "power2.out"
    }, "-=0.4")
    .to(subText.value, {
      opacity: 1,
      y: -10,
      duration: 0.5,
      ease: "power2.out"
    }, "-=0.3")
  
    // Pulse rings animation
    const ringTl = gsap.timeline({ repeat: -1 })
    ringTl.to(ring1.value, {
      scale: 3,
      opacity: 0,
      duration: 2,
      ease: "power2.out"
    })
    .to(ring2.value, {
      scale: 3,
      opacity: 0,
      duration: 2,
      ease: "power2.out"
    }, "-=1.7")
    .to(ring3.value, {
      scale: 3,
      opacity: 0,
      duration: 2,
      ease: "power2.out"
    }, "-=1.7")
  
    // Glow effect animation
    gsap.to(glowEffect.value, {
      scale: 1.2,
      opacity: 0.6,
      duration: 2,
      repeat: -1,
      yoyo: true,
      ease: "power1.inOut"
    })
  
    // Floating elements animation
    gsap.to(float1.value, {
      x: 50,
      y: -30,
      duration: 4,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    })
  
    gsap.to(float2.value, {
      x: -40,
      y: 20,
      duration: 5,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    })
  
    gsap.to(float3.value, {
      x: 30,
      y: -40,
      duration: 6,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    })
  
    // Main icon animation
    gsap.to(mainIcon.value, {
      y: -15,
      duration: 1.5,
      repeat: -1,
      yoyo: true,
      ease: "power1.inOut"
    })
  
    // Function to start particles animation after entry timeline ends
    const startParticles = () => {
      modalParticles.value.forEach((particle, i) => {
        gsap.set(particle, { opacity: 1 })

        const angle = (i / modalParticles.value.length) * Math.PI * 2
        const distance = 150 + Math.random() * 100

        gsap.to(particle, {
          x: Math.cos(angle) * distance,
          y: Math.sin(angle) * distance,
          opacity: 0,
          scale: 0.5,
          duration: 2 + Math.random(),
          repeat: -1,
          delay: i * 0.1,
          ease: "power2.out"
        })
      })
    }

    // Launch particles once the main entry timeline is complete
    tl.eventCallback("onComplete", startParticles)
  })
  </script>
  
  <style scoped>
  /* Continuous gradient border animation */
  @keyframes gradient-rotate {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
  
  .bg-gradient-animated {
    background-size: 200% 200%;
    animation: gradient-rotate 3s ease infinite;
  }
  </style>