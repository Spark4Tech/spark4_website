// main.js

// Function to show toast notifications
function showToast(message, isSuccess = true) {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create the toast element
    const toast = document.createElement('div');
    toast.className = `fixed py-3 px-6 rounded-lg shadow-lg 
        ${isSuccess ? 'bg-blue-600' : 'bg-red-500'} text-white z-50`;
    
    // Set initial styles
    toast.style.transition = 'all 0.5s ease';
    toast.style.maxWidth = '90%';
    toast.style.textAlign = 'center';
    toast.style.opacity = '0';
    toast.style.left = '50%';
    toast.style.transform = 'translate(-50%, -50%)';  // Center horizontally and vertically
    toast.style.top = '50%';  // Start in middle
    toast.textContent = message;

    // Append to body
    document.body.appendChild(toast);

    // Trigger initial animation after a brief delay
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.top = '24px';  // Move to top
        toast.style.transform = 'translate(-50%, 0)';  // Keep centered horizontally
    });

    // Remove toast after delay
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, -20px)';  // Slight upward fade out
        
        setTimeout(() => {
            toast.remove();
        }, 500);
    }, 3000);
}

// Function to initialize Flatpickr for date inputs
function initializeDatePicker(elementId, defaultDate) {

    flatpickr(`#${elementId}`, {
        dateFormat: "Y-m-d",
        defaultDate: defaultDate || new Date(),
        altInput: true,
        altFormat: "F j, Y",
        allowInput: true,
        theme: "material_blue",
        static: true
    });
}

// Function to initialize Flatpickr for time inputs
function initializeTimePicker(elementId, defaultTime) {

    //const input = document.getElementById(elementId);
    //const existingValue = input.value;

    flatpickr(`#${elementId}`, {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",  // Save as 24-hour format
        altInput: true,
        altFormat: "h:i K",  // Display as 12-hour format
        time_24hr: false,  // Still let users see AM/PM
        defaultDate: defaultTime || getNextWholeHour(),
        minuteIncrement: 15,
        allowInput: true,
        theme: "material_blue",
        static: true
    });
}

// Function to open modals (if needed)
function openModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

// Function to close any modal by its ID
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        // Reset form if it exists
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Schedule Activity';
            }
        }

        // Hide modal
        modal.classList.add('hidden');
        
        // Reset container states
        const formContainer = document.getElementById('activity-form-container');
        const activitiesList = document.getElementById('activities-list');
        if (formContainer && activitiesList) {
            formContainer.classList.add('hidden');
            activitiesList.style.display = 'block';
        }
    }
}

function showSpinner() {
    const spinner = document.getElementById('spinnerOverlay');
    if (spinner) {
        spinner.classList.remove('hidden');
    } else {
        console.error('Spinner overlay element not found');
    }
}

function hideSpinner() {
    const spinner = document.getElementById('spinnerOverlay');
    if (spinner) {
        spinner.classList.add('hidden');
    } else {
        console.error('Spinner overlay element not found');
    }
}

