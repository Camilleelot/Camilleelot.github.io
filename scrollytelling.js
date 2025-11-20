/**
 * Sticky Scrollytelling JavaScript
 * Uses Intersection Observer API to track scroll position and update charts
 */

class ScrollyTelling {
  constructor(options = {}) {
    this.container = options.container || '.scrolly-section';
    this.steps = options.steps || '.step';
    this.chart = options.chart || '.scrolly-chart';
    this.onStepEnter = options.onStepEnter || null;
    this.onStepExit = options.onStepExit || null;
    this.offset = options.offset || 0.5; // Trigger when 50% of step is in view

    this.currentStep = null;
    this.observer = null;

    this.init();
  }

  init() {
    // Setup Intersection Observer
    const observerOptions = {
      root: null, // viewport
      rootMargin: '0px',
      threshold: this.offset
    };

    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.handleStepEnter(entry.target);
        } else {
          this.handleStepExit(entry.target);
        }
      });
    }, observerOptions);

    // Observe all steps
    const stepElements = document.querySelectorAll(this.steps);
    stepElements.forEach(step => {
      this.observer.observe(step);
    });

    // Initialize progress bar if it exists
    this.initProgressBar();
  }

  handleStepEnter(step) {
    // Remove active class from all steps
    document.querySelectorAll(this.steps).forEach(s => {
      s.classList.remove('active');
    });

    // Add active class to current step
    step.classList.add('active');
    this.currentStep = step;

    // Get step index
    const stepIndex = parseInt(step.dataset.step);

    // Update chart based on step
    this.updateChart(stepIndex);

    // Call custom callback if provided
    if (this.onStepEnter) {
      this.onStepEnter(step, stepIndex);
    }

    // Update progress bar
    this.updateProgressBar(step);
  }

  handleStepExit(step) {
    // Call custom callback if provided
    if (this.onStepExit) {
      this.onStepExit(step);
    }
  }

  updateChart(stepIndex) {
    // Hide all chart states
    const chartStates = document.querySelectorAll('.chart-state');
    chartStates.forEach(state => {
      state.classList.remove('active');
    });

    // Show chart state for current step
    const activeState = document.querySelector(`.chart-state[data-step="${stepIndex}"]`);
    if (activeState) {
      activeState.classList.add('active');
    }

    // Trigger chart animation/update event
    const event = new CustomEvent('scrolly:stepChange', {
      detail: { step: stepIndex }
    });
    document.dispatchEvent(event);
  }

  initProgressBar() {
    const progressBar = document.querySelector('.scrolly-progress-bar');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
      this.updateProgressBar();
    });
  }

  updateProgressBar(currentStep = null) {
    const progressBar = document.querySelector('.scrolly-progress-bar');
    if (!progressBar) return;

    const steps = document.querySelectorAll(this.steps);
    const totalSteps = steps.length;

    if (currentStep) {
      const stepIndex = parseInt(currentStep.dataset.step);
      const progress = ((stepIndex + 1) / totalSteps) * 100;
      progressBar.style.width = `${progress}%`;
    } else {
      // Calculate based on scroll position
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const progress = (scrolled / scrollHeight) * 100;
      progressBar.style.width = `${progress}%`;
    }
  }

  destroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}

// Helper function to create simple chart updates
function createChartUpdater(chartId, updateFunction) {
  document.addEventListener('scrolly:stepChange', (e) => {
    const canvas = document.getElementById(chartId);
    if (canvas && updateFunction) {
      updateFunction(canvas, e.detail.step);
    }
  });
}

// Export for use in modules or attach to window for direct use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ScrollyTelling, createChartUpdater };
} else {
  window.ScrollyTelling = ScrollyTelling;
  window.createChartUpdater = createChartUpdater;
}

// Auto-initialize if data-scrollytelling attribute is present
document.addEventListener('DOMContentLoaded', () => {
  const autoInit = document.querySelector('[data-scrollytelling="auto"]');
  if (autoInit) {
    new ScrollyTelling();
  }
});
