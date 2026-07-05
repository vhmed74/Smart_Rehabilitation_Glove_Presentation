document.addEventListener('DOMContentLoaded', () => {
    
    // Initialize Swiper with Vertical Direction
    const swiper = new Swiper('.mySwiper', {
        direction: 'vertical',
        slidesPerView: 1,
        spaceBetween: 0,
        mousewheel: true,
        keyboard: {
            enabled: true,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        speed: 800,
        on: {
            init: function () {
                animateSlide(this.slides[this.activeIndex]);
                updateProgressBar(this);
            },
            slideChangeTransitionStart: function () {
                // Reset animations for all slides
                resetAnimations(this.slides);
            },
            slideChangeTransitionEnd: function () {
                // Trigger animation for the active slide
                animateSlide(this.slides[this.activeIndex]);
                updateProgressBar(this);
            }
        }
    });

    // Update Progress Bar
    function updateProgressBar(swiperInstance) {
        const total = swiperInstance.slides.length - 1;
        const current = swiperInstance.activeIndex;
        const percentage = (current / total) * 100;
        document.getElementById('progressBar').style.width = percentage + '%';
    }

    // GSAP Animation Logic
    function resetAnimations(slides) {
        slides.forEach(slide => {
            gsap.set(slide.querySelectorAll('.fade-in-element, .slide-left-element, .slide-right-element, .scale-up-element, .stagger-elements > *'), {
                opacity: 0,
                clearProps: "transform"
            });
        });
    }

    function animateSlide(slide) {
        const tl = gsap.timeline();

        // Fade in elements
        const fadeEls = slide.querySelectorAll('.fade-in-element');
        if (fadeEls.length > 0) {
            tl.fromTo(fadeEls, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out", stagger: 0.2 }, 0);
        }

        // Slide from left
        const leftEls = slide.querySelectorAll('.slide-left-element');
        if (leftEls.length > 0) {
            tl.fromTo(leftEls, { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 0.2);
        }

        // Slide from right
        const rightEls = slide.querySelectorAll('.slide-right-element');
        if (rightEls.length > 0) {
            tl.fromTo(rightEls, { opacity: 0, x: 50 }, { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 0.2);
        }

        // Scale up
        const scaleEls = slide.querySelectorAll('.scale-up-element');
        if (scaleEls.length > 0) {
            tl.fromTo(scaleEls, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.7)" }, 0.3);
        }

        // Stagger elements (grids, lists)
        const staggerParents = slide.querySelectorAll('.stagger-elements');
        staggerParents.forEach(parent => {
            const children = parent.children;
            if (children.length > 0) {
                tl.fromTo(children, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: "power2.out" }, 0.4);
            }
        });
    }
});
