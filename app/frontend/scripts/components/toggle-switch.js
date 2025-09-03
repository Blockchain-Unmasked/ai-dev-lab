/**
 * Professional Toggle Switch Component
 * AI/DEV Lab Design System
 * 
 * Features:
 * - Smooth animations and transitions
 * - Full accessibility support (ARIA, keyboard navigation)
 * - Multiple states (checked, disabled, loading, success, warning, error)
 * - Event handling and state management
 * - Customizable appearance and behavior
 */

class ToggleSwitch {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            checked: false,
            disabled: false,
            loading: false,
            state: 'default', // default, success, warning, error
            size: 'default', // small, default, large
            onChange: null,
            onToggle: null,
            ...options
        };
        
        this.state = {
            checked: this.options.checked,
            disabled: this.options.disabled,
            loading: this.options.loading,
            state: this.options.state
        };
        
        this.init();
    }
    
    init() {
        this.setupElement();
        this.bindEvents();
        this.updateVisualState();
        this.setupAccessibility();
    }
    
    setupElement() {
        // Ensure proper HTML structure
        if (!this.element.querySelector('.thumb')) {
            const thumb = document.createElement('div');
            thumb.className = 'thumb';
            this.element.appendChild(thumb);
        }
        
        // Add base classes
        this.element.classList.add('toggle-switch');
        this.element.classList.add(`toggle-switch-${this.options.size}`);
        
        // Set initial state
        if (this.state.checked) {
            this.element.classList.add('checked');
        }
        
        if (this.state.disabled) {
            this.element.classList.add('disabled');
            this.element.setAttribute('disabled', '');
        }
        
        if (this.state.loading) {
            this.element.classList.add('loading');
        }
        
        if (this.state.state !== 'default') {
            this.element.classList.add(this.state.state);
        }
    }
    
    bindEvents() {
        // Click event
        this.element.addEventListener('click', (e) => {
            if (this.state.disabled || this.state.loading) return;
            this.toggle();
        });
        
        // Keyboard events
        this.element.addEventListener('keydown', (e) => {
            if (this.state.disabled || this.state.loading) return;
            
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.toggle();
            }
        });
        
        // Focus events for accessibility
        this.element.addEventListener('focus', () => {
            this.element.classList.add('focused');
        });
        
        this.element.addEventListener('blur', () => {
            this.element.classList.remove('focused');
        });
    }
    
    setupAccessibility() {
        // Set ARIA attributes
        this.element.setAttribute('role', 'switch');
        this.element.setAttribute('tabindex', '0');
        this.element.setAttribute('aria-checked', this.state.checked);
        
        // Add label if not present
        if (!this.element.getAttribute('aria-labelledby') && !this.element.getAttribute('aria-label')) {
            const label = this.element.nextElementSibling;
            if (label && label.classList.contains('toggle-switch-label')) {
                const labelId = 'toggle-label-' + Math.random().toString(36).substr(2, 9);
                label.id = labelId;
                this.element.setAttribute('aria-labelledby', labelId);
            }
        }
        
        // Update ARIA state when changed
        this.element.addEventListener('change', () => {
            this.element.setAttribute('aria-checked', this.state.checked);
        });
    }
    
    toggle() {
        if (this.state.disabled || this.state.loading) return;
        
        this.state.checked = !this.state.checked;
        this.updateVisualState();
        this.triggerEvents();
    }
    
    setChecked(checked) {
        if (this.state.disabled || this.state.loading) return;
        
        this.state.checked = Boolean(checked);
        this.updateVisualState();
        this.triggerEvents();
    }
    
    setDisabled(disabled) {
        this.state.disabled = Boolean(disabled);
        this.updateVisualState();
        
        if (this.state.disabled) {
            this.element.setAttribute('disabled', '');
        } else {
            this.element.removeAttribute('disabled');
        }
    }
    
    setLoading(loading) {
        this.state.loading = Boolean(loading);
        this.updateVisualState();
    }
    
    setState(state) {
        const validStates = ['default', 'success', 'warning', 'error'];
        if (!validStates.includes(state)) return;
        
        // Remove previous state classes
        this.element.classList.remove('success', 'warning', 'error');
        
        this.state.state = state;
        this.updateVisualState();
    }
    
    setSize(size) {
        const validSizes = ['small', 'default', 'large'];
        if (!validSizes.includes(size)) return;
        
        // Remove previous size classes
        this.element.classList.remove('toggle-switch-small', 'toggle-switch-default', 'toggle-switch-large');
        
        this.options.size = size;
        this.element.classList.add(`toggle-switch-${size}`);
    }
    
    updateVisualState() {
        // Update checked state
        if (this.state.checked) {
            this.element.classList.add('checked');
        } else {
            this.element.classList.remove('checked');
        }
        
        // Update disabled state
        if (this.state.disabled) {
            this.element.classList.add('disabled');
        } else {
            this.element.classList.remove('disabled');
        }
        
        // Update loading state
        if (this.state.loading) {
            this.element.classList.add('loading');
        } else {
            this.element.classList.remove('loading');
        }
        
        // Update state classes
        this.element.classList.remove('success', 'warning', 'error');
        if (this.state.state !== 'default') {
            this.element.classList.add(this.state.state);
        }
        
        // Update ARIA attributes
        this.element.setAttribute('aria-checked', this.state.checked);
    }
    
    triggerEvents() {
        // Create custom event
        const event = new CustomEvent('toggleChange', {
            detail: {
                checked: this.state.checked,
                disabled: this.state.disabled,
                loading: this.state.loading,
                state: this.state.state,
                element: this.element
            },
            bubbles: true
        });
        
        this.element.dispatchEvent(event);
        
        // Call callback functions
        if (this.options.onChange && typeof this.options.onChange === 'function') {
            this.options.onChange(this.state.checked, this.state);
        }
        
        if (this.options.onToggle && typeof this.options.onToggle === 'function') {
            this.options.onToggle(this.state.checked, this.state);
        }
    }
    
    // Public methods
    getChecked() {
        return this.state.checked;
    }
    
    getDisabled() {
        return this.state.disabled;
    }
    
    getLoading() {
        return this.state.loading;
    }
    
    getState() {
        return this.state.state;
    }
    
    destroy() {
        // Remove event listeners
        this.element.removeEventListener('click', this.boundClickHandler);
        this.element.removeEventListener('keydown', this.boundKeydownHandler);
        
        // Remove classes
        this.element.classList.remove('toggle-switch', 'checked', 'disabled', 'loading', 'success', 'warning', 'error');
        
        // Remove ARIA attributes
        this.element.removeAttribute('role');
        this.element.removeAttribute('tabindex');
        this.element.removeAttribute('aria-checked');
        this.element.removeAttribute('aria-labelledby');
    }
}

// Factory function for easy creation
function createToggleSwitch(element, options = {}) {
    return new ToggleSwitch(element, options);
}

// Auto-initialize toggle switches
document.addEventListener('DOMContentLoaded', () => {
    const toggleSwitches = document.querySelectorAll('[data-toggle-switch]');
    
    toggleSwitches.forEach(element => {
        const options = {
            checked: element.hasAttribute('data-checked'),
            disabled: element.hasAttribute('data-disabled'),
            loading: element.hasAttribute('data-loading'),
            state: element.getAttribute('data-state') || 'default',
            size: element.getAttribute('data-size') || 'default',
            onChange: window[element.getAttribute('data-on-change')] || null,
            onToggle: window[element.getAttribute('data-on-toggle')] || null
        };
        
        createToggleSwitch(element, options);
    });
});

// Export for use in other modules
window.ToggleSwitch = ToggleSwitch;
window.createToggleSwitch = createToggleSwitch;
