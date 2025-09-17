// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Get the form element
    const form = document.getElementById('analysisForm');
    
    if (form) {
        // Add submit event listener to the form
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const videoUrl = document.getElementById('videoUrl').value.trim();
            const email = document.getElementById('email').value.trim();
            
            // Simple validation
            if (!videoUrl || !email) {
                showError('Please fill in all required fields.');
                return;
            }
            
            // Validate YouTube URL
            if (!isValidYouTubeUrl(videoUrl)) {
                showError('Please enter a valid YouTube URL.');
                return;
            }
            
            // Validate email
            if (!isValidEmail(email)) {
                showError('Please enter a valid email address.');
                return;
            }
            
            // Show loading overlay
            showLoading();
            
            // Prepare form data
            const formData = new FormData();
            formData.append('video_url', videoUrl);
            formData.append('email', email);
            
            // Send data to the server
            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Hide loading overlay
                hideLoading();
                
                // Show success message
                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                successModal.show();
                
                // Reset form
                form.reset();
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                showError(error.message || 'An error occurred while processing your request. Please try again later.');
            });
        });
    }
    
    // Function to validate YouTube URL
    function isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
    
    // Function to validate email
    function isValidEmail(email) {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(email);
    }
    
    // Function to show loading overlay
    function showLoading() {
        const loadingOverlay = document.querySelector('.loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    }
    
    // Function to hide loading overlay
    function hideLoading() {
        const loadingOverlay = document.querySelector('.loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }
    
    // Function to show error message in modal
    function showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
            errorMessage.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                </div>
            `;
            
            const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
            errorModal.show();
        } else {
            alert(message);
        }
    }
    
    // Add animation to cards on scroll
    const animateOnScroll = function() {
        const cards = document.querySelectorAll('.card');
        
        cards.forEach(card => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (cardPosition < screenPosition) {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Add scroll event listener for animations
    window.addEventListener('scroll', animateOnScroll);
    
    // Initial animation check
    animateOnScroll();
});
