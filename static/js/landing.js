/* ============================================================
   StartupLens Landing Page – JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* ── Sticky Navbar ──────────────────────────────────────── */
    const navbar = document.querySelector('.landing-navbar');
    if (navbar) {
        const onScroll = () => {
            navbar.classList.toggle('scrolled', window.scrollY > 40);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Smooth Scroll for Anchor Links ─────────────────────── */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', e => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
                // Close mobile nav
                const navCollapse = document.querySelector('.navbar-collapse.show');
                if (navCollapse) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) bsCollapse.hide();
                }
            }
        });
    });

    /* ── Scroll Reveal ──────────────────────────────────────── */
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    /* ── Animate Progress Bars on Scroll ────────────────────── */
    const progressBars = document.querySelectorAll('.progress-bar-sl .bar');
    if (progressBars.length > 0) {
        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const width = entry.target.dataset.width;
                    if (width) entry.target.style.width = width;
                    barObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => {
            bar.style.width = '0%';
            barObserver.observe(bar);
        });
    }

    /* ── Animate ML Rings on Scroll ─────────────────────────── */
    const mlRings = document.querySelectorAll('.ml-ring svg circle.progress-ring');
    if (mlRings.length > 0) {
        const ringObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const circle = entry.target;
                    const pct = parseFloat(circle.dataset.pct || 0);
                    const circumference = parseFloat(circle.getAttribute('stroke-dasharray'));
                    circle.style.strokeDashoffset = circumference - (circumference * pct / 100);
                    ringObserver.unobserve(circle);
                }
            });
        }, { threshold: 0.5 });

        mlRings.forEach(ring => {
            ringObserver.observe(ring);
        });
    }

    /* ── Active Nav Link Highlight ───────────────────────────── */
    const sections = document.querySelectorAll('section[id]');
    if (sections.length > 0) {
        const navLinks = document.querySelectorAll('.landing-navbar .nav-link[href^="#"]');
        const activeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    navLinks.forEach(link => link.classList.remove('active'));
                    const activeLink = document.querySelector(
                        `.landing-navbar .nav-link[href="#${entry.target.id}"]`
                    );
                    if (activeLink) activeLink.classList.add('active');
                }
            });
        }, { threshold: 0.3, rootMargin: '-80px 0px -60% 0px' });

        sections.forEach(section => activeObserver.observe(section));
    }

    /* ── Counter Animation ──────────────────────────────────── */
    const counters = document.querySelectorAll('[data-count]');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.count, 10);
                    const suffix = el.dataset.suffix || '';
                    let current = 0;
                    const step = Math.ceil(target / 40);
                    const timer = setInterval(() => {
                        current += step;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        el.textContent = current + suffix;
                    }, 30);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(c => counterObserver.observe(c));
    }
});
