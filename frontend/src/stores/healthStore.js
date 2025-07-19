import { reactive } from 'vue';
import { get_request } from './services/request_http.js';

// Reactive state of the store
const state = reactive({
  isChecking: false,
  serverStatus: null, // 'healthy', 'unhealthy', 'error'
  modelLoaded: false,
  serviceName: '',
  error: null,
  lastCheckTime: null,
  isInitialized: false
});

/**
 * Store to handle server health check
 */
export const healthStore = {
  // Getters to access the state
  get isChecking() {
    return state.isChecking;
  },
  
  get serverStatus() {
    return state.serverStatus;
  },
  
  get modelLoaded() {
    return state.modelLoaded;
  },
  
  get serviceName() {
    return state.serviceName;
  },
  
  get error() {
    return state.error;
  },
  
  get lastCheckTime() {
    return state.lastCheckTime;
  },

  get isInitialized() {
    return state.isInitialized;
  },

  /**
   * Checks if the server is working correctly
   * @returns {Promise<boolean>} true if server is healthy, false otherwise
   */
  async checkServerHealth() {
    try {
      this.setChecking(true);
      this.clearError();

      const response = await get_request('health/');
      
      if (response.status === 200 && response.data) {
        const healthData = response.data;
        
        // Update state with server response
        state.serverStatus = healthData.status || 'unknown';
        state.modelLoaded = healthData.model_loaded || false;
        state.serviceName = healthData.service || 'Unknown service';
        state.lastCheckTime = new Date().toISOString();
        
        // Mark as initialized after first successful check
        if (!state.isInitialized) {
          state.isInitialized = true;
        }

        console.log('Health check successful:', healthData);
        return healthData.status === 'healthy';
      } else {
        throw new Error('Invalid server response');
      }

    } catch (error) {
      console.error('Error in health check:', error);
      
      // Handle different types of errors
      if (error.response) {
        const status = error.response.status;
        
        if (status === 503) {
          this.setError('Service is temporarily unavailable');
          state.serverStatus = 'unhealthy';
        } else if (status === 500) {
          this.setError('Internal server error');
          state.serverStatus = 'error';
        } else {
          this.setError(`Server error: ${status}`);
          state.serverStatus = 'error';
        }
      } else if (error.request) {
        this.setError('Could not connect to server');
        state.serverStatus = 'error';
      } else {
        this.setError('Request error: ' + error.message);
        state.serverStatus = 'error';
      }

      state.modelLoaded = false;
      state.lastCheckTime = new Date().toISOString();
      
      return false;
    } finally {
      this.setChecking(false);
    }
  },

  /**
   * Initializes health check when loading the application
   * Runs automatically when importing the store
   */
  async initialize() {
    console.log('Initializing server health check...');
    
    const isHealthy = await this.checkServerHealth();
    
    if (isHealthy) {
      console.log('✅ Server initialized correctly');
    } else {
      console.warn('⚠️ Problems detected on server');
    }
    
    return isHealthy;
  },

  /**
   * Sets up a periodic health check
   * @param {number} intervalMinutes - Interval in minutes for automatic check
   * @returns {function} Function to stop the interval
   */
  startPeriodicHealthCheck(intervalMinutes = 5) {
    const intervalMs = intervalMinutes * 60 * 1000;
    
    console.log(`Setting up automatic health check every ${intervalMinutes} minutes`);
    
    const intervalId = setInterval(async () => {
      console.log('Running periodic health check...');
      await this.checkServerHealth();
    }, intervalMs);

    // Return function to stop the interval
    return () => {
      clearInterval(intervalId);
      console.log('Periodic health check stopped');
    };
  },

  /**
   * Gets a summary of the current server state
   * @returns {object} Object with state summary
   */
  getHealthSummary() {
    return {
      isHealthy: state.serverStatus === 'healthy',
      status: state.serverStatus,
      modelLoaded: state.modelLoaded,
      serviceName: state.serviceName,
      lastCheck: state.lastCheckTime,
      error: state.error,
      canColorize: state.serverStatus === 'healthy' && state.modelLoaded
    };
  },

  /**
   * Checks if the service is ready to colorize images
   * @returns {boolean} true if ready, false otherwise
   */
  isReadyForColorization() {
    return state.serverStatus === 'healthy' && state.modelLoaded && !state.isChecking;
  },

  // Helper methods to modify state
  setChecking(checking) {
    state.isChecking = checking;
  },

  setError(error) {
    state.error = error;
  },

  clearError() {
    state.error = null;
  },

  /**
   * Resets the store state
   */
  reset() {
    state.isChecking = false;
    state.serverStatus = null;
    state.modelLoaded = false;
    state.serviceName = '';
    state.error = null;
    state.lastCheckTime = null;
    state.isInitialized = false;
  }
};

// Auto-initialize when importing the store
// Only in browser (not in SSR)
if (typeof window !== 'undefined') {
  // Use nextTick to ensure Vue is fully initialized
  import('vue').then(({ nextTick }) => {
    nextTick(() => {
      healthStore.initialize();
    });
  });
} 