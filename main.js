document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    const navItems = document.querySelectorAll('.nav-item');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
            // Add active class to parent if it's a dropdown
            const parentNavItem = link.closest('.nav-item');
            if (parentNavItem) {
                parentNavItem.classList.add('active');
            }
        }
    });
    
    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Countdown timer for upcoming matches
    const countdownElements = document.querySelectorAll('.match-countdown');
    
    countdownElements.forEach(element => {
        const matchTime = new Date(element.getAttribute('data-match-time')).getTime();
        
        const countdownFunction = setInterval(function() {
            const now = new Date().getTime();
            const distance = matchTime - now;
            
            if (distance < 0) {
                clearInterval(countdownFunction);
                element.innerHTML = "MATCH STARTED";
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            let countdownText = '';
            
            if (days > 0) {
                countdownText += `${days}d `;
            }
            
            countdownText += ${hours}h ${minutes}m ${seconds}s;
            element.innerHTML = countdownText;
        }, 1000);
    });
    
    // Team color applying
    const teamElements = document.querySelectorAll('.team-card');
    
    teamElements.forEach(element => {
        const primaryColor = element.getAttribute('data-primary-color');
        const secondaryColor = element.getAttribute('data-secondary-color');
        
        if (primaryColor) {
            element.style.borderColor = primaryColor;
            const headerEl = element.querySelector('.card-header');
            if (headerEl) {
                headerEl.style.backgroundColor = primaryColor;
                headerEl.style.color = getContrastColor(primaryColor);
            }
        }
        
        if (secondaryColor) {
            const footerEl = element.querySelector('.card-footer');
            if (footerEl) {
                footerEl.style.backgroundColor = secondaryColor;
                footerEl.style.color = getContrastColor(secondaryColor);
            }
        }
    });
    
    // Function to determine contrasting text color (black or white) based on background
    function getContrastColor(hexColor) {
        // If it's not a hex color, return black
        if (!hexColor || hexColor[0] !== '#') {
            return '#000000';
        }
        
        // Convert hex to RGB
        let r, g, b;
        if (hexColor.length === 4) {
            r = parseInt(hexColor[1] + hexColor[1], 16);
            g = parseInt(hexColor[2] + hexColor[2], 16);
            b = parseInt(hexColor[3] + hexColor[3], 16);
        } else {
            r = parseInt(hexColor.substr(1, 2), 16);
            g = parseInt(hexColor.substr(3, 2), 16);
            b = parseInt(hexColor.substr(5, 2), 16);
        }
        
        // Calculate brightness (YIQ formula)
        const brightness = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        
        // Return black for bright colors, white for dark colors
        return brightness > 128 ? '#000000' : '#ffffff';
    }
    
    // Initialize any carousels
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carouselEl => {
        new bootstrap.Carousel(carouselEl, {
            interval: 5000,
            wrap: true
        });
    });
    
    // Handle match filter selection
    const matchFilterSelect = document.getElementById('matchFilterSelect');
    if (matchFilterSelect) {
        matchFilterSelect.addEventListener('change', function() {
            window.location.href = /matches?status=${this.value};
        });
    }
    
    // Live match simulation
    const liveMatchElements = document.querySelectorAll('.live-match');
    
    liveMatchElements.forEach(element => {
        // Only run simulation for matches that are live
        if (element.getAttribute('data-match-status') === 'Live') {
            let homeScore = parseInt(element.getAttribute('data-home-score') || '0');
            let awayScore = parseInt(element.getAttribute('data-away-score') || '0');
            let homeWickets = parseInt(element.getAttribute('data-home-wickets') || '0');
            let awayWickets = parseInt(element.getAttribute('data-away-wickets') || '0');
            
            const homeScoreElement = element.querySelector('.home-score');
            const awayScoreElement = element.querySelector('.away-score');
            
            // Simulate score updates every few seconds
            const scoreInterval = setInterval(function() {
                // Random chance to update score
                if (Math.random() > 0.7) {
                    // 20% chance of a wicket falling (if less than 10 wickets)
                    if (Math.random() > 0.8 && homeWickets < 10) {
                        homeWickets++;
                    } else {
                        // Add between 1-6 runs
                        homeScore += Math.floor(Math.random() * 6) + 1;
                    }
                    
                    if (homeScoreElement) {
                        homeScoreElement.textContent = ${homeScore}/${homeWickets};
                    }
                }
                
                if (Math.random() > 0.7) {
                    // 20% chance of a wicket falling (if less than 10 wickets)
                    if (Math.random() > 0.8 && awayWickets < 10) {
                        awayWickets++;
                    } else {
                        // Add between 1-6 runs
                        awayScore += Math.floor(Math.random() * 6) + 1;
                    }
                    
                    if (awayScoreElement) {
                        awayScoreElement.textContent = ${awayScore}/${awayWickets};
                    }
                }
            }, 5000);
            
            // Clear interval when leaving the page
            window.addEventListener('beforeunload', function() {
                clearInterval(scoreInterval);
            });
        }
    });
});
