/**
 * Landing Page - Mapa da Noite
 * Interactive Logic, Data Visualizations & Web Audio API
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // 1. Audio Player Elements (Declared at the top to prevent TDZ ReferenceErrors)
    // -------------------------------------------------------------
    const audio = document.getElementById('bgAudio');
    const audioPlayerContainer = document.getElementById('audioPlayerContainer');
    const audioToggleBtn = document.getElementById('audioToggleBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const playerStatus = audioPlayerContainer ? audioPlayerContainer.querySelector('.player-status') : null;

    let audioCtx = null;
    let analyser = null;
    let sourceNode = null;
    let freqDataArray = null;
    let beatScale = 1.0;

    // Helper functions for Audio Context
    function initAudioContext() {
        if (audioCtx) return;
        if (!audio) return;
        
        try {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioCtx.createAnalyser();
            analyser.fftSize = 64; // Small fft for fast beat detection
            
            // Connect audio element to analyser and destination
            sourceNode = audioCtx.createMediaElementSource(audio);
            sourceNode.connect(analyser);
            analyser.connect(audioCtx.destination);
            
            freqDataArray = new Uint8Array(analyser.frequencyBinCount);
        } catch (e) {
            console.warn("Web Audio API not supported or blocked: ", e);
        }
    }

    function updateBeatScale() {
        if (!analyser || !audio || audio.paused) {
            // Smoothly decrease beatScale back to 1.0 when audio is paused/inactive
            beatScale = beatScale * 0.9 + 1.0 * 0.1;
            return;
        }
        
        if (freqDataArray) {
            analyser.getByteFrequencyData(freqDataArray);
            
            // Tribal house kick lives in the lowest bins (sub & mid bass)
            let bassSum = 0;
            const binsToUse = 6;
            for (let i = 0; i < binsToUse; i++) {
                bassSum += freqDataArray[i];
            }
            const bassAvg = bassSum / binsToUse; // 0 - 255
            
            // Map average bass to a visual multiplier (1.0 to 1.25)
            const targetScale = 1.0 + (bassAvg / 255) * 0.25;
            // Smooth transition
            beatScale = beatScale * 0.75 + targetScale * 0.25;
        }
    }

    // -------------------------------------------------------------
    // 2. Interactive Radar Visual (Canvas)
    // -------------------------------------------------------------
    const canvas = document.getElementById('radarCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('radarTooltip');
        const tooltipId = tooltip ? tooltip.querySelector('.tooltip-id') : null;
        const tooltipText = tooltip ? tooltip.querySelector('.tooltip-text') : null;
        const tooltipMeta = tooltip ? tooltip.querySelector('.tooltip-meta') : null;

        // Resize Canvas to container
        let width = 0;
        let height = 0;
        let centerX = 0;
        let centerY = 0;
        let maxRadius = 0;

        function resizeCanvas() {
            const rect = canvas.getBoundingClientRect();
            width = rect.width * window.devicePixelRatio;
            height = rect.height * window.devicePixelRatio;
            canvas.width = width;
            canvas.height = height;
            centerX = width / 2;
            centerY = height / 2;
            maxRadius = Math.min(centerX, centerY) - 20;
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
            // Draw initial frames
            centerX /= window.devicePixelRatio;
            centerY /= window.devicePixelRatio;
            maxRadius /= window.devicePixelRatio;
        }

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Raw observation data
        // Raw observation data (with English translations)
        const observations = [
            { id: 'OBS-001', text: 'Pista open air maravilhosa, a acústica e a vibração musical estavam impecáveis...', textEn: 'Wonderful open air dancefloor, acoustics and musical vibration were flawless...', category: 'Experiência', categoryEn: 'Experience', color: '#F1C40F', radius: 0.22, angle: 1.2, speed: 0.0008 },
            { id: 'OBS-002', text: 'Fila do bar na pista principal impossível, mais de 40 minutos para conseguir água...', textEn: 'Main floor bar line impossible, over 40 minutes to get water...', category: 'Operação', categoryEn: 'Operation', color: '#00D2FF', radius: 0.55, angle: 2.1, speed: -0.001 },
            { id: 'OBS-003', text: 'O deslocamento na saída da Barra Funda de madrugada é muito difícil, poucos táxis...', textEn: 'Late night transit leaving Barra Funda is very difficult, few taxis available...', category: 'Território', categoryEn: 'Territory', color: '#9B59B6', radius: 0.78, angle: 3.4, speed: 0.0012 },
            { id: 'OBS-004', text: 'O acolhimento e a energia da pista tribal house trazem um senso único de comunidade...', textEn: 'The welcoming vibe and energy of the tribal house floor bring a unique sense of community...', category: 'Experiência', categoryEn: 'Experience', color: '#F1C40F', radius: 0.35, angle: 4.8, speed: -0.0009 },
            { id: 'OBS-005', text: 'Falta de caixas móveis para reduzir o gargalo na hora de comprar as fichas...', textEn: 'Lack of mobile cashiers to reduce bottlenecks during drink token sales...', category: 'Operação', categoryEn: 'Operation', color: '#00D2FF', radius: 0.62, angle: 0.5, speed: 0.0015 },
            { id: 'OBS-006', text: 'O entorno industrial do evento precisava de melhor iluminação externa de segurança...', textEn: 'The industrial surroundings of the venue needed better external safety lighting...', category: 'Território', categoryEn: 'Territory', color: '#9B59B6', radius: 0.85, angle: 5.6, speed: -0.0007 },
            { id: 'OBS-007', text: 'A curadoria musical com DJs locais de altíssimo nível foi o ponto alto da noite...', textEn: 'Super high-level music curation with local DJs was the high point of the night...', category: 'Experiência', categoryEn: 'Experience', color: '#F1C40F', radius: 0.44, angle: 2.8, speed: 0.0011 },
            { id: 'OBS-008', text: 'Chapelaria muito lenta para receber e devolver os pertences, gerando fila desnecessária...', textEn: 'Coat check very slow to receive and return belongings, generating unnecessary queues...', category: 'Operação', categoryEn: 'Operation', color: '#00D2FF', radius: 0.50, angle: 6.1, speed: -0.0014 },
            { id: 'OBS-009', text: 'O acesso por transporte público é limitado nessa área industrial nas primeiras horas da manhã...', textEn: 'Public transit access is limited in this industrial area during early morning hours...', category: 'Território', categoryEn: 'Territory', color: '#9B59B6', radius: 0.71, angle: 1.8, speed: 0.0009 }
        ];

        let sweepAngle = 0;
        let hoveredDot = null;
        let mouseX = -999;
        let mouseY = -999;

        // Mouse Move interactions
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouseX = e.clientX - rect.left;
            mouseY = e.clientY - rect.top;
        });

        canvas.addEventListener('mouseleave', () => {
            mouseX = -999;
            mouseY = -999;
            hoveredDot = null;
            if (tooltip) tooltip.classList.remove('active');
        });

        // Animation Loop
        function animate() {
            ctx.clearRect(0, 0, width, height);

            // Update beat scale
            updateBeatScale();

            // 1. Draw Radar Background Grid
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
            ctx.lineWidth = 1;

            // Concentric Orbits (reactive to audio beat)
            const orbits = [0.25, 0.5, 0.75, 1.0];
            orbits.forEach(orbit => {
                ctx.beginPath();
                const orbitBeatMultiplier = 1.0 + (beatScale - 1.0) * 0.12;
                ctx.arc(centerX, centerY, maxRadius * orbit * orbitBeatMultiplier, 0, Math.PI * 2);
                ctx.stroke();
            });

            // Grid Lines (Crosshairs)
            ctx.beginPath();
            ctx.moveTo(centerX - maxRadius, centerY);
            ctx.lineTo(centerX + maxRadius, centerY);
            ctx.moveTo(centerX, centerY - maxRadius);
            ctx.lineTo(centerX, centerY + maxRadius);
            ctx.stroke();

            // 2. Draw Radar Sweep
            sweepAngle += 0.005;
            if (sweepAngle > Math.PI * 2) sweepAngle = 0;

            const sweepGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, maxRadius);
            sweepGradient.addColorStop(0, 'rgba(241, 196, 15, 0.15)');
            sweepGradient.addColorStop(1, 'rgba(241, 196, 15, 0)');

            ctx.fillStyle = sweepGradient;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, maxRadius, sweepAngle - 0.25, sweepAngle, false);
            ctx.lineTo(centerX, centerY);
            ctx.fill();

            // Draw sweep line edge
            ctx.strokeStyle = 'rgba(241, 196, 15, 0.3)';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(
                centerX + maxRadius * Math.cos(sweepAngle),
                centerY + maxRadius * Math.sin(sweepAngle)
            );
            ctx.stroke();

            // 3. Draw & Update Orbiting Observations
            let currentHover = null;
            let minDistance = 15;

            observations.forEach(dot => {
                dot.angle += dot.speed;

                // Orbit radius bounces slightly on beat
                const bounceFactor = 1.0 + (beatScale - 1.0) * 0.08;
                const orbitRadius = maxRadius * dot.radius * bounceFactor;
                const x = centerX + orbitRadius * Math.cos(dot.angle);
                const y = centerY + orbitRadius * Math.sin(dot.angle);

                dot.pulse = (dot.pulse || 0) + 0.05;
                const glowSize = (3 + Math.sin(dot.pulse) * 1.5) * beatScale;

                const dx = x - mouseX;
                const dy = y - mouseY;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < minDistance) {
                    minDistance = distance;
                    currentHover = dot;
                }

                // Draw glow
                ctx.beginPath();
                ctx.arc(x, y, glowSize + 2, 0, Math.PI * 2);
                ctx.fillStyle = dot.color === '#F1C40F' ? 'rgba(241, 196, 15, 0.25)' : 'rgba(0, 210, 255, 0.25)';
                ctx.fill();

                // Draw core
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, Math.PI * 2);
                ctx.fillStyle = dot.color;
                ctx.fill();
            });

            // 4. Handle Hover / Tooltip (with multilingual support)
            if (currentHover && tooltip && tooltipId && tooltipText && tooltipMeta) {
                if (hoveredDot !== currentHover) {
                    hoveredDot = currentHover;
                    tooltipId.textContent = hoveredDot.id;
                    const isEn = (window.currentLanguage === 'en');
                    tooltipText.textContent = `“${isEn ? (hoveredDot.textEn || hoveredDot.text) : hoveredDot.text}”`;
                    tooltipMeta.textContent = isEn ? (hoveredDot.categoryEn || hoveredDot.category) : hoveredDot.category;
                    tooltipMeta.style.color = hoveredDot.color;
                    tooltip.classList.add('active');
                }
            }

            requestAnimationFrame(animate);
        }

        animate();
    }

    // -------------------------------------------------------------
    // 3. Count Up Metrics Animation
    // -------------------------------------------------------------
    const metricNumbers = document.querySelectorAll('.metric-num');
    
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'), 10);
        const duration = 2000;
        let startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            
            const easeProgress = progress * (2 - progress);
            const current = Math.floor(easeProgress * target);
            
            element.textContent = current.toLocaleString('pt-BR');

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = target.toLocaleString('pt-BR');
            }
        }
        requestAnimationFrame(step);
    }

    const metricsSection = document.querySelector('.metrics-banner');
    if (metricsSection) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    metricNumbers.forEach(num => animateCounter(num));
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        observer.observe(metricsSection);
    }

    // -------------------------------------------------------------
    // 4. Evidence Cards Filter Logic
    // -------------------------------------------------------------
    const filterButtons = document.querySelectorAll('.filter-btn');
    const signalCards = document.querySelectorAll('.signal-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            signalCards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'flex';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0) scale(1)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(15px) scale(0.95)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // -------------------------------------------------------------
    // 5. Sentiment Chart Bar Filling
    // -------------------------------------------------------------
    const sentimentChart = document.querySelector('.sentiment-chart');
    const barFills = document.querySelectorAll('.bar-fill');

    if (sentimentChart) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const total = 7468;
                    barFills.forEach(bar => {
                        const val = parseInt(bar.getAttribute('data-value'), 10);
                        const percentage = (val / total) * 100;
                        bar.style.width = `${percentage}%`;
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        observer.observe(sentimentChart);
    }

    // -------------------------------------------------------------
    // 6. Scroll to Top Behavior
    // -------------------------------------------------------------
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // -------------------------------------------------------------
    // 7. Navigation Smooth Scroll
    // -------------------------------------------------------------
    const navLinks = document.querySelectorAll('.nav-link, .hero-actions a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const targetSec = document.querySelector(targetId);
                if (targetSec) {
                    const offsetTop = targetSec.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // -------------------------------------------------------------
    // 8. Background Audio Controls Integration
    // -------------------------------------------------------------
    if (audioToggleBtn && audio && audioPlayerContainer && playIcon && pauseIcon && playerStatus) {
        function togglePlay() {
            initAudioContext();
            if (audioCtx && audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            if (audio.paused) {
                audio.play()
                    .then(() => {
                        audioPlayerContainer.classList.add('playing');
                        playerStatus.textContent = 'Tocando';
                        playIcon.style.display = 'none';
                        pauseIcon.style.display = 'block';
                    })
                    .catch(err => {
                        console.warn("Autoplay blocked by browser:", err);
                        playerStatus.textContent = 'Ativar Som';
                    });
            } else {
                audio.pause();
                audioPlayerContainer.classList.remove('playing');
                playerStatus.textContent = 'Pausado';
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }
        }

        audioToggleBtn.addEventListener('click', togglePlay);

        // Auto-play attempt on first click anywhere on the page
        function handleFirstInteraction() {
            initAudioContext();
            if (audioCtx && audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            
            if (audio.paused) {
                audio.play()
                    .then(() => {
                        audioPlayerContainer.classList.add('playing');
                        playerStatus.textContent = 'Tocando';
                        playIcon.style.display = 'none';
                        pauseIcon.style.display = 'block';
                    })
                    .catch(() => {
                        // Fail silently, wait for button click
                    });
            }
            document.removeEventListener('click', handleFirstInteraction);
        }
        
        document.addEventListener('click', handleFirstInteraction);
    }

    // -------------------------------------------------------------
    // 9. Multilingual Translation System (PT/EN)
    // -------------------------------------------------------------
    window.currentLanguage = 'pt';

    const i18n = {
        en: {
            // Navigation
            "nav-projeto": "The Project",
            "nav-evidencias": "Evidence",
            "nav-metodo": "Method",
            "nav-principios": "Principles",
            "nav-avaliacao": "Access & Test",
            
            // Top Badge
            "header-badge": '<span class="badge-dot" style="background-color: #10b981;"></span> Ground Zero (MDN-RPP01)',
            
            // Hero
            "hero-tag": '<span class="tag-pin"></span> São Paulo · Electronic & Tribal House Scene',
            "hero-title": 'What does the night reveal when comments stop being <span class="highlight-text">noise?</span>',
            "hero-subtitle": 'The Night Map is a nightlife collective intelligence platform designed to transform public comments, reviews, reports, and records into evidence of experiences, behaviors, perceptions, silences, risks, and opportunities related to parties, events, territories, and audiences. The project encompasses collection, document organization, database cleaning, thematic classification, pattern analysis, sociocultural reading, experience analysis, dashboard production, and public communication of results.',
            "btn-view-exploratory": 'View exploratory scope <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
            "btn-understand-path": 'Understand path <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>',
            
            // Radar Panel
            "radar-title": "GROUND ZERO (RPP01)",
            "radar-status": "VALIDATED",
            "radar-tooltip-default": "Hover over the radar points to listen to the night...",
            "radar-footer-posts": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> POSTS: JUN 01—30, 2026',
            "radar-footer-audited": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> AUDITED: JUL 20—21, 2026',
            
            // Metrics Banner
            "metrics-lead": "A reading begins with scale. It gains meaning through interpretation.",
            "metrics-sublead": "This Ground Zero round (MDN-RPP01) investigates the perception of attendees, artists, and workers regarding posts published from June 1st to 30th, 2026, with data extraction and technical auditing executed on July 20th and 21st, 2026.",
            "metrics-badge": "PROCESSED BASE · GROUND ZERO (MDN-RPP01)",
            "metric-label-observed": "Observed Profiles",
            "metric-label-sources": "Source Files",
            "metric-label-preserved": "Preserved Comments",
            "metric-label-consolidated": "Consolidated Records",
            "metrics-footer": "The totals presented document the processing path and may be refined during technical validation.",
            
            // Section 1: O Projeto
            "proj-num": "01 / THE PROJECT",
            "proj-title": 'Not a party guide. A <span class="gradient-text-gold">collective intelligence platform.</span>',
            "proj-lead": "The Night Map observes public comments, identifies recurring patterns, and organizes evidence about São Paulo's electronic and tribal house scene.",
            "proj-body": "The focus is not to expose individuals or rate personal experiences. It lies in understanding what repeats, what changes, and what the collective conversation reveals about belonging, operation, territory, and culture.",
            "feat-patterns": "Collective Patterns",
            "feat-auditable": "Auditable Evidence",
            "feat-privacy": "Privacy by Design",
            
            // Section 2: Evidências
            "evid-num": "02 / EVIDENCE",
            "evid-tag": "EXPLORATORY SCOPE",
            "evid-title": 'When a comment repeats, it can become a <span class="highlight-text-gold">signal</span>.',
            "evid-desc": "The examples below show how recurrences help raise questions. They do not represent definitive conclusions.",
            
            // Filters
            "filter-all": "All signals",
            "filter-experiencia": "Experience",
            "filter-operacao": "Operation",
            "filter-territorio": "Territory",
            "filter-musica": "Music & Curation",
            "filter-saude": "Health & Safety",
            "filter-economia": "Economy & Value",
            "filter-sociocultural": "Sociocultural",
            "filter-bastidores": "Work & Backstage",
            "filter-governanca": "Governance & Ethics",
            
            // Signal Cards (categories mapped dynamically in function)
            "card-tag-experiencia": "Experience",
            "card-title-experiencia": "The dancefloor is also memory",
            "card-desc-experiencia": "Comments about encounters, belonging, and enchantment reveal how the experience remains after the party.",
            "card-count-experiencia": "2,850 MENTIONS",
            
            "card-tag-operacao": "Operation",
            "card-title-operacao": "The queue changes the reading of the night",
            "card-desc-operacao": "Wait times, entry, and organization appear as recurring signals that affect public perception.",
            "card-count-operacao": "3,190 OCCURRENCES",
            
            "card-tag-territorio": "Territory",
            "card-title-territorio": "São Paulo does not live just one night",
            "card-desc-territorio": "Transit, access, and urban context help explain different experiences within the same scene.",
            "card-count-territorio": "1,428 OCCURRENCES",
            
            "card-tag-musica": "Curation",
            "card-title-musica": "Sonic identity as an anchor",
            "card-desc-musica": "Line-ups, genres, and musical expectations guide public choices and loyalty in the tribal scene.",
            "card-count-musica": "1,105 OCCURRENCES",
            
            "card-tag-saude": "Safety",
            "card-title-saude": "The invisible care that sustains the night",
            "card-desc-saude": "Mentions of harm reduction, welcoming space, and security point to the ethics of care as a priority.",
            "card-count-saude": "850 OCCURRENCES",
            
            "card-tag-economia": "Economy",
            "card-title-economia": "Pricing and the scale of value",
            "card-desc-economia": "Ticket prices, bar consumption, and logistics costs trace the tension between commercialization and accessibility.",
            "card-count-economia": "940 OCCURRENCES",
            
            "card-tag-sociocultural": "Sociocultural",
            "card-title-sociocultural": "Pajubá and the dancefloor codes",
            "card-desc-sociocultural": "Linguistic expressions, scene slang, and collective rituals show how the dancefloor builds identity and symbolic capital.",
            "card-count-sociocultural": "785 OCCURRENCES",
            
            "card-tag-bastidores": "Backstage",
            "card-title-bastidores": "Who makes the night happen",
            "card-desc-bastidores": "Comments about staff, promoters, DJs, and support crew highlight the importance of backstage labor relations.",
            "card-count-bastidores": "620 OCCURRENCES",
            
            "card-tag-governanca": "Governance",
            "card-title-governanca": "Ethics, protection, and limits",
            "card-desc-governanca": "Mentions of consent, privacy, and legal responsibility show the active search for safety and compliance on the dancefloor.",
            "card-count-governanca": "410 OCCURRENCES",
            
            // Sentiment Consolidation
            "chart-tag": "SENTIMENT CONSOLIDATION",
            "chart-title": "The conversation tone also leaves clues.",
            "chart-desc": "Within the universe of 7,468 comments of the MDN-RPP01 round, the quantitative classification reveals the exact balance of factual urban behavior perceptions.",
            "chart-pos": "Positive",
            "chart-neu": "Neutral",
            "chart-neg": "Negative",
            
            // Section 3: Método
            "method-num": "03 / METHOD",
            "method-title": "From scattered conversation to evidence that can be a rule or signal.",
            "method-desc": "Each step preserves the connection between origin, treatment, and interpretation. Thus, the final reading does not rely on an isolated impression.",
            
            "step-title-1": "Listen",
            "step-desc-1": "Public comments are gathered as spontaneous signals of collective experience.",
            "step-title-2": "Organize",
            "step-desc-2": "Records undergo cleaning, standardization, and protection of identifiable information.",
            "step-title-3": "Interpret",
            "step-desc-3": "Recurrences are classified by themes to separate isolated episodes from collective patterns.",
            "step-title-4": "Deliver",
            "step-desc-4": "Findings return to the scene in clear, traceable, and in-depth readable formats.",
            
            // Section 4: Princípios
            "principles-num": "04 / PRINCIPLES",
            "principles-title": "See the collective without exposing the individual.",
            "principles-lead": "The map's strength lies in the quality of the journey — and the limits it respects.",
            
            "princ-title-1": "Privacy",
            "princ-desc-1": "Identities are not the object of analysis.",
            "princ-title-2": "Traceability",
            "princ-desc-2": "Results can be checked and revisited.",
            "princ-title-3": "Context",
            "princ-desc-3": "Numbers are interpreted within the culture of the scene.",
            
            // Section 5: Acesso & Teste
            "access-num": "05 / ACCESS & TEST",
            "access-title": "Methodological validation in a secure environment.",
            "access-lead": "The Night Map was designed for academic, technical, and institutional evaluation. Reviewers can inspect the infrastructure without local database processing.",
            
            "access-card-title-1": "Sandbox Environment",
            "access-card-desc-1": "Inspect ALCATEIA's analytical panel (Audit Dashboard) with full reactive polymorphism, without installing anything.",
            "access-btn-1": 'Access Audit Dashboard <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
            
            "access-card-title-2": "Supported Platforms",
            "access-card-item-1": "<strong>Browsers:</strong> Chrome, Edge, Firefox, Safari (Modern)",
            "access-card-item-2": "<strong>Devices:</strong> Responsive for Desktop (1920p) and Mobile",
            "access-card-item-3": "<strong>Accessibility:</strong> Support for screen readers and WCAG AAA contrast",
            
            "access-card-title-3": "Local Installation (Optional)",
            "access-card-desc-3": "For development or end-to-end replication of the infrastructure:",
            
            // Quote Banner
            "quote-tag": "NIGHTLIFE AS A SOURCE OF KNOWLEDGE",
            "quote-text": "“The map does not speak for each individual. It shows what begins to appear when many voices are read together.”",
            "btn-scroll-top": 'Back to top <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>',
            
            // Footer
            "footer-desc": "Collective intelligence applied to São Paulo's nightlife.",
            "footer-meta": "Initial scope · 2026",
            
            // Accessibility Sidebar
            "acc-title": "Accessibility",
            "acc-font-size": "Text Size",
            "acc-contrast": "Contrast",
            "acc-high-contrast": "High Contrast",
            "acc-spacing": "Spacing",
            "acc-generous-spacing": "Generous Spacing",
            "acc-links": "Links",
            "acc-underline-links": "Underline Links",
            "acc-dyslexia": "Legibility",
            "acc-dyslexia-font": "Dyslexia Font",
            "acc-reset-all": "Reset All Adjustments"
        },
        pt: {
            // Navigation
            "nav-projeto": "O projeto",
            "nav-evidencias": "Evidências",
            "nav-metodo": "Método",
            "nav-principios": "Princípios",
            "nav-avaliacao": "Acesso & Teste",
            
            // Top Badge
            "header-badge": '<span class="badge-dot" style="background-color: #10b981;"></span> Marco Zero (MDN-RPP01)',
            
            // Hero
            "hero-tag": '<span class="tag-pin"></span> São Paulo · Cena Eletrônica e Tribal House',
            "hero-title": 'O que a noite revela quando os comentários deixam de ser <span class="highlight-text">ruído?</span>',
            "hero-subtitle": 'O Mapa da Noite é uma plataforma de inteligência coletiva da vida noturna, criada para transformar comentários, avaliações, relatos e registros públicos em evidências sobre experiências, comportamentos, percepções, silêncios, riscos e oportunidades associados a festas, eventos, territórios e públicos. O percurso compreende extração, organização documental, higienização de bases, classificação temática, análise de recorrências, leitura sociocultural, análise de experiência, produção de dashboards e comunicação pública dos resultados.',
            "btn-view-exploratory": 'Ver o recorte exploratório <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
            "btn-understand-path": 'Entender o percurso <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>',
            
            // Radar Panel
            "radar-title": "MARCO ZERO (RPP01)",
            "radar-status": "VALIDADO",
            "radar-tooltip-default": "Passe o mouse pelos pontos do radar para escutar a noite...",
            "radar-footer-posts": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> POSTS: 01—30 JUN 2026',
            "radar-footer-audited": '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg> AUDITADO: 20—21 JUL 2026',
            
            // Metrics Banner
            "metrics-lead": "Uma leitura começa pela escala. Ganha sentido pela interpretação.",
            "metrics-sublead": "Esta rodada de Marco Zero (MDN-RPP01) investiga a percepção de frequentadores, artistas e trabalhadores sobre posts publicados de 1º a 30 de Junho de 2026, com extrações e auditoria técnica de dados executadas em 20 e 21 de Julho de 2026.",
            "metrics-badge": "BASE PROCESSADA · MARCO ZERO (MDN-RPP01)",
            "metric-label-observed": "Perfis Observados",
            "metric-label-sources": "Arquivos de Origem",
            "metric-label-preserved": "Comentários Preservados",
            "metric-label-consolidated": "Registros Consolidados",
            "metrics-footer": "Os totais apresentados documentam o percurso de processamento e podem ser refinados durante a validação metodológica.",
            
            // Section 1: O Projeto
            "proj-num": "01 / O PROJETO",
            "proj-title": 'Não é um guia de festas. É uma <span class="gradient-text-gold">plataforma de inteligência coletiva.</span>',
            "proj-lead": "O Mapa da Noite observa comentários públicos, identifica padrões recorrentes e organiza evidências sobre a cena eletrônica e tribal house de São Paulo.",
            "proj-body": "O foco não é expor pessoas ou avaliar experiências individuais. Está em compreender o que se repete, o que muda e o que a conversa coletiva pode revelar sobre pertencimento, operação, território e cultura.",
            "feat-patterns": "Padrões Coletivos",
            "feat-auditable": "Evidências Auditáveis",
            "feat-privacy": "Privacidade por Princípio",
            
            // Section 2: Evidências
            "evid-num": "02 / EVIDÊNCIAS",
            "evid-tag": "RECORTE EXPLORATÓRIO",
            "evid-title": 'Quando um comentário se repete, ele pode se tornar um <span class="highlight-text-gold">sinal</span>.',
            "evid-desc": "Os exemplos abaixo mostram como recorrências ajudam a abrir perguntas. Eles não representam conclusões definitivas.",
            
            // Filters
            "filter-all": "Todos os sinais",
            "filter-experiencia": "Experiência",
            "filter-operacao": "Operação",
            "filter-territorio": "Território",
            "filter-musica": "Música e Curadoria",
            "filter-saude": "Saúde e Segurança",
            "filter-economia": "Economia e Valor",
            "filter-sociocultural": "Sociocultural",
            "filter-bastidores": "Trabalho e Bastidores",
            "filter-governanca": "Governança e Ética",
            
            // Signal Cards
            "card-tag-experiencia": "Experiência",
            "card-title-experiencia": "A pista também é memória",
            "card-desc-experiencia": "Comentários sobre encontro, pertencimento e encanto revelam como a experiência permanece depois da festa.",
            "card-count-experiencia": "2.850 MENÇÕES",
            
            "card-tag-operacao": "Operação",
            "card-title-operacao": "A fila muda a leitura da noite",
            "card-desc-operacao": "Tempo de espera, entrada e organização aparecem como sinais recorrentes que afetam a percepção do público.",
            "card-count-operacao": "3.190 OCORRÊNCIAS",
            
            "card-tag-territorio": "Território",
            "card-title-territorio": "São Paulo não vive uma noite só",
            "card-desc-territorio": "Deslocamento, acesso e contexto urbano ajudam a explicar experiências diferentes dentro da mesma cena.",
            "card-count-territorio": "1.428 OCORRÊNCIAS",
            
            "card-tag-musica": "Curadoria",
            "card-title-musica": "A identidade sonora como âncora",
            "card-desc-musica": "Line-ups, gêneros e expectativas musicais guiam as escolhas e a fidelização do público na cena tribal.",
            "card-count-musica": "1.105 OCORRÊNCIAS",
            
            "card-tag-saude": "Segurança",
            "card-title-saude": "O cuidado invisível que sustenta a noite",
            "card-desc-saude": "Menções a redução de danos, acolhimento e segurança apontam a ética do cuidado como prioridade.",
            "card-count-saude": "850 OCORRÊNCIAS",
            
            "card-tag-economia": "Economia",
            "card-title-economia": "Precificação e a balança de valor",
            "card-desc-economia": "Ingressos, consumo no bar e custos logísticos desenham a tensão entre comercialização e acessibilidade.",
            "card-count-economia": "940 OCORRÊNCIAS",
            
            "card-tag-sociocultural": "Sociocultural",
            "card-title-sociocultural": "O Pajubá e os códigos da pista",
            "card-desc-sociocultural": "Manifestações linguísticas, gírias da cena e rituais coletivos mostram como a pista constrói identidade e capital simbólico.",
            "card-count-sociocultural": "785 OCORRÊNCIAS",
            
            "card-tag-bastidores": "Bastidores",
            "card-title-bastidores": "Quem faz a noite acontecer",
            "card-desc-bastidores": "Comentários sobre staff, promoters, DJs e a equipe de apoio evidenciam a importância das relações de trabalho nos bastidores.",
            "card-count-bastidores": "620 OCORRÊNCIAS",
            
            "card-tag-governanca": "Governança",
            "card-title-governanca": "Ética, proteção e limites",
            "card-desc-governanca": "Menções a consentimento, privacidade e responsabilidade jurídica mostram a busca ativa por segurança e conformidade na pista.",
            "card-count-governanca": "410 OCORRÊNCIAS",
            
            // Sentiment Consolidation
            "chart-tag": "CONSOLIDAÇÃO DE SENTIMENTOS",
            "chart-title": "O tom da conversa também deixa pistas.",
            "chart-desc": "No universo de 7.468 comentários da rodada MDN-RPP01, a classificação quantitativa revela o equilíbrio exato das percepções fáticas de comportamento urbano.",
            "chart-pos": "Positivos",
            "chart-neu": "Neutros",
            "chart-neg": "Negativos",
            
            // Section 3: Método
            "method-num": "03 / MÉTODO",
            "method-title": "Da conversa dispersa à evidência que pode ser regra ou sinal.",
            "method-desc": "Cada etapa preserva a ligação entre origem, treatment e interpretação. Assim, a leitura final não depende de uma impressão isolada.",
            
            "step-title-1": "Escutar",
            "step-desc-1": "Comentários públicos são reunidos como sinais espontâneos da experiência coletiva.",
            "step-title-2": "Organizar",
            "step-desc-2": "Registros passam por limpeza, padronização e proteção de informações identificáveis.",
            "step-title-3": "Interpretar",
            "step-desc-3": "Recorrências são classificadas por temas para separar episódios isolados de padrões coletivos.",
            "step-title-4": "Devolver",
            "step-desc-4": "Os achados retornam à cena em leituras claras, rastreáveis e abertas ao aprofundamento.",
            
            // Section 4: Princípios
            "principles-num": "04 / PRINCÍPIOS",
            "principles-title": "Ver o coletivo sem expor o indivíduo.",
            "principles-lead": "A força do mapa está na qualidade do percurso — e nos limites que ele respeita.",
            
            "princ-title-1": "Privacidade",
            "princ-desc-1": "Identidades não são o objeto da análise.",
            "princ-title-2": "Rastreabilidade",
            "princ-desc-2": "Resultados podem ser conferidos e revisited.",
            "princ-title-3": "Context",
            "princ-desc-3": "Números são interpretados dentro da cultura da cena.",
            
            // Section 5: Acesso & Teste
            "access-num": "05 / ACESSO & TESTE",
            "access-title": "Validação metodológica em ambiente seguro.",
            "access-lead": "O Mapa da Noite foi projetado para avaliação acadêmica, técnica e institucional. Avaliadores podem inspecionar a infraestrutura sem necessidade de processar bases locais.",
            
            "access-card-title-1": "Ambiente de Testes",
            "access-card-desc-1": "Inspecione o painel analítico da ALCATEIA (Dashboard de Auditoria) com o polimorfismo reativo completo, sem precisar instalar nada.",
            "access-btn-1": 'Acessar Dashboard de Auditoria <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
            
            "access-card-title-2": "Plataformas Suportadas",
            "access-card-item-1": "<strong>Navegadores:</strong> Chrome, Edge, Firefox, Safari (Modernos)",
            "access-card-item-2": "<strong>Dispositivos:</strong> Responsivo para Desktop (1920p) e Mobile",
            "access-card-item-3": "<strong>Acessibilidade:</strong> Suporte a leitores de tela e contraste WCAG AAA",
            
            "access-card-title-3": "Instalação Local (Opcional)",
            "access-card-desc-3": "Para desenvolvimento ou replicação da infraestrutura de ponta a ponta:",
            
            // Quote Banner
            "quote-tag": "A NOITE COMO FONTE DE CONHECIMENTO",
            "quote-text": "“O mapa não fala por cada pessoa. Ele mostra o que começa a aparecer quando muitas vozes são lidas em conjunto.”",
            "btn-scroll-top": 'Voltar ao início <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>',
            
            // Footer
            "footer-desc": "Inteligência coletiva aplicada à vida noturna de São Paulo.",
            "footer-meta": "Recorte inicial · 2026",
            
            // Accessibility Sidebar
            "acc-title": "Acessibilidade",
            "acc-font-size": "Tamanho do Texto",
            "acc-contrast": "Contraste",
            "acc-high-contrast": "Alto Contraste",
            "acc-spacing": "Espaçamento",
            "acc-generous-spacing": "Espaçamento Ampliado",
            "acc-links": "Links",
            "acc-underline-links": "Sublinhar Links",
            "acc-dyslexia": "Legibilidade",
            "acc-dyslexia-font": "Fonte p/ Dislexia",
            "acc-reset-all": "Resetar Ajustes"
        }
    };

    const selectorMap = {
        // Nav links
        '.nav-menu .nav-link[href="#projeto"]': "nav-projeto",
        '.nav-menu .nav-link[href="#evidencias"]': "nav-evidencias",
        '.nav-menu .nav-link[href="#metodo"]': "nav-metodo",
        '.nav-menu .nav-link[href="#principios"]': "nav-principios",
        '.nav-menu .nav-link[href="#avaliacao"]': "nav-avaliacao",
        
        // Badge & Hero
        '.header-badge': "header-badge",
        '.hero-tag': "hero-tag",
        '.hero-title': "hero-title",
        '.hero-subtitle': "hero-subtitle",
        '.hero-actions .btn-primary': "btn-view-exploratory",
        '.hero-actions .btn-secondary': "btn-understand-path",
        
        // Radar
        '.radar-header .radar-title': "radar-title",
        '.radar-header .radar-status': "radar-status",
        '.radar-footer .radar-date': "radar-footer-posts",
        '.radar-footer .radar-aggregate': "radar-footer-audited",
        
        // Metrics
        '.metrics-lead': "metrics-lead",
        '.metrics-sublead': "metrics-sublead",
        '.metrics-badge': "metrics-badge",
        '.metric-item:nth-child(1) .metric-label': "metric-label-observed",
        '.metric-item:nth-child(2) .metric-label': "metric-label-sources",
        '.metric-item:nth-child(3) .metric-label': "metric-label-preserved",
        '.metric-item:nth-child(4) .metric-label': "metric-label-consolidated",
        '.metrics-footer': "metrics-footer",
        
        // Section 1
        '#projeto .section-number': "proj-num",
        '#projeto .section-title': "proj-title",
        '#projeto .lead-text': "proj-lead",
        '#projeto .body-text': "proj-body",
        '.features-row .feature-card:nth-child(1) h3': "feat-patterns",
        '.features-row .feature-card:nth-child(2) h3': "feat-auditable",
        '.features-row .feature-card:nth-child(3) h3': "feat-privacy",
        
        // Section 2 intro
        '.evidences-intro .section-number': "evid-num",
        '.evidences-intro .section-tag': "evid-tag",
        '.evidences-intro .section-title': "evid-title",
        '.evidences-intro .body-text': "evid-desc",
        
        // Filters
        '.filters-container .filter-btn[data-filter="all"]': "filter-all",
        '.filters-container .filter-btn[data-filter="experiencia"]': "filter-experiencia",
        '.filters-container .filter-btn[data-filter="operacao"]': "filter-operacao",
        '.filters-container .filter-btn[data-filter="territorio"]': "filter-territorio",
        '.filters-container .filter-btn[data-filter="musica"]': "filter-musica",
        '.filters-container .filter-btn[data-filter="saude"]': "filter-saude",
        '.filters-container .filter-btn[data-filter="economia"]': "filter-economia",
        '.filters-container .filter-btn[data-filter="sociocultural"]': "filter-sociocultural",
        '.filters-container .filter-btn[data-filter="bastidores"]': "filter-bastidores",
        '.filters-container .filter-btn[data-filter="governanca"]': "filter-governanca",
        
        // Sentiment
        '.sentiment-info .chart-tag': "chart-tag",
        '.sentiment-info h3': "chart-title",
        '.sentiment-info p': "chart-desc",
        '.sentiment-chart .chart-row:nth-child(1) .row-label span:nth-child(1)': "chart-pos",
        '.sentiment-chart .chart-row:nth-child(2) .row-label span:nth-child(1)': "chart-neu",
        '.sentiment-chart .chart-row:nth-child(3) .row-label span:nth-child(1)': "chart-neg",
        
        // Section 3
        '#metodo .section-number': "method-num",
        '#metodo .section-title': "method-title",
        '#metodo .body-text': "method-desc",
        '.steps-grid .step-card:nth-child(1) h3': "step-title-1",
        '.steps-grid .step-card:nth-child(1) p': "step-desc-1",
        '.steps-grid .step-card:nth-child(2) h3': "step-title-2",
        '.steps-grid .step-card:nth-child(2) p': "step-desc-2",
        '.steps-grid .step-card:nth-child(3) h3': "step-title-3",
        '.steps-grid .step-card:nth-child(3) p': "step-desc-3",
        '.steps-grid .step-card:nth-child(4) h3': "step-title-4",
        '.steps-grid .step-card:nth-child(4) p': "step-desc-4",
        
        // Section 4
        '#principios .section-number': "principles-num",
        '#principios .section-title': "principles-title",
        '#principios .lead-text': "principles-lead",
        '.principles-list .principle-item:nth-child(1) h3': "princ-title-1",
        '.principles-list .principle-item:nth-child(1) p': "princ-desc-1",
        '.principles-list .principle-item:nth-child(2) h3': "princ-title-2",
        '.principles-list .principle-item:nth-child(2) p': "princ-desc-2",
        '.principles-list .principle-item:nth-child(3) h3': "princ-title-3",
        '.principles-list .principle-item:nth-child(3) p': "princ-desc-3",
        
        // Section 5
        '#avaliacao .section-number': "access-num",
        '#avaliacao .section-title': "access-title",
        '.avaliacao-header .body-text': "access-lead",
        
        '.avaliacao-grid .avaliacao-card:nth-child(1) h3': "access-card-title-1",
        '.avaliacao-grid .avaliacao-card:nth-child(1) p': "access-card-desc-1",
        '.avaliacao-grid .avaliacao-card:nth-child(1) .btn-primary': "access-btn-1",
        
        '.avaliacao-grid .avaliacao-card:nth-child(2) h3': "access-card-title-2",
        '.avaliacao-grid .avaliacao-card:nth-child(2) .avaliacao-list li:nth-child(1)': "access-card-item-1",
        '.avaliacao-grid .avaliacao-card:nth-child(2) .avaliacao-list li:nth-child(2)': "access-card-item-2",
        '.avaliacao-grid .avaliacao-card:nth-child(2) .avaliacao-list li:nth-child(3)': "access-card-item-3",
        
        '.avaliacao-grid .avaliacao-card:nth-child(3) h3': "access-card-title-3",
        '.avaliacao-grid .avaliacao-card:nth-child(3) p': "access-card-desc-3",
        
        // Quote & Footer
        '.quote-tag': "quote-tag",
        '.quote-text': "quote-text",
        '#scrollTopBtn': "btn-scroll-top",
        '.footer-brand p': "footer-desc",
        '.footer-meta span': "footer-meta",

        // Accessibility Sidebar elements
        '#accSidebar [data-i18n="acc-title"]': "acc-title",
        '#accSidebar [data-i18n="acc-font-size"]': "acc-font-size",
        '#accSidebar [data-i18n="acc-contrast"]': "acc-contrast",
        '#accSidebar [data-i18n="acc-high-contrast"]': "acc-high-contrast",
        '#accSidebar [data-i18n="acc-spacing"]': "acc-spacing",
        '#accSidebar [data-i18n="acc-generous-spacing"]': "acc-generous-spacing",
        '#accSidebar [data-i18n="acc-links"]': "acc-links",
        '#accSidebar [data-i18n="acc-underline-links"]': "acc-underline-links",
        '#accSidebar [data-i18n="acc-dyslexia"]': "acc-dyslexia",
        '#accSidebar [data-i18n="acc-dyslexia-font"]': "acc-dyslexia-font",
        '#accSidebar [data-i18n="acc-reset-all"]': "acc-reset-all"
    };

    function translatePage(lang) {
        window.currentLanguage = lang;
        
        // 1. Translate standard selectors
        for (const selector in selectorMap) {
            const key = selectorMap[selector];
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (i18n[lang] && i18n[lang][key]) {
                    el.innerHTML = i18n[lang][key];
                }
            });
        }
        
        // 2. Translate 9 Signal Cards (including counts and tags)
        const categories = ["experiencia", "operacao", "territorio", "musica", "saude", "economia", "sociocultural", "bastidores", "governanca"];
        categories.forEach(cat => {
            const card = document.querySelector(`.signal-card[data-category="${cat}"]`);
            if (card) {
                const tagEl = card.querySelector('.card-tag');
                const h3El = card.querySelector('.card-content h3');
                const pEl = card.querySelector('.card-content p');
                const countEl = card.querySelector('.badge-count');
                
                if (tagEl) tagEl.textContent = i18n[lang][`card-tag-${cat}`];
                if (h3El) h3El.textContent = i18n[lang][`card-title-${cat}`];
                if (pEl) pEl.textContent = i18n[lang][`card-desc-${cat}`];
                if (countEl) countEl.textContent = i18n[lang][`card-count-${cat}`];
            }
        });
        
        // 3. Translate radar default tooltip text
        const tooltipText = document.querySelector('#radarTooltip .tooltip-text');
        if (tooltipText && (!hoveredDot)) {
            tooltipText.textContent = i18n[lang]["radar-tooltip-default"];
        }
    }

    const langBtns = document.querySelectorAll('.lang-btn');
    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            langBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const selectedLang = btn.getAttribute('data-lang');
            translatePage(selectedLang);
        });
    });

    // -------------------------------------------------------------
    // 10. Accessibility Sidebar & Controls
    // -------------------------------------------------------------
    const accTriggerBtn = document.getElementById('accTriggerBtn');
    const accSidebar = document.getElementById('accSidebar');
    const accCloseBtn = document.getElementById('accCloseBtn');
    const accOverlay = document.getElementById('accOverlay');

    if (accTriggerBtn && accSidebar && accCloseBtn && accOverlay) {
        // Toggle Sidebar
        function openSidebar() {
            accSidebar.classList.add('open');
            accOverlay.classList.add('open');
        }

        function closeSidebar() {
            accSidebar.classList.remove('open');
            accOverlay.classList.remove('open');
        }

        accTriggerBtn.addEventListener('click', openSidebar);
        accCloseBtn.addEventListener('click', closeSidebar);
        accOverlay.addEventListener('click', closeSidebar);

        // Escape key to close sidebar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeSidebar();
            }
        });

        // Accessibility Tools Logic
        let fontScaleLevel = 0; // -1: small, 0: normal, 1: large, 2: extra large
        const scaleValues = { '-1': '85%', '0': '100%', '1': '115%', '2': '130%' };

        const btnFontDec = document.getElementById('btnFontDec');
        const btnFontReset = document.getElementById('btnFontReset');
        const btnFontInc = document.getElementById('btnFontInc');
        const btnContrastToggle = document.getElementById('btnContrastToggle');
        const btnSpacingToggle = document.getElementById('btnSpacingToggle');
        const btnLinksToggle = document.getElementById('btnLinksToggle');
        const btnDyslexiaToggle = document.getElementById('btnDyslexiaToggle');
        const btnAccReset = document.getElementById('btnAccReset');

        function updateFontScaleButtons() {
            [btnFontDec, btnFontReset, btnFontInc].forEach(b => {
                if (b) b.classList.remove('active');
            });
            if (fontScaleLevel === -1 && btnFontDec) btnFontDec.classList.add('active');
            if (fontScaleLevel === 0 && btnFontReset) btnFontReset.classList.add('active');
            if (fontScaleLevel === 1 && btnFontInc) btnFontInc.classList.add('active');
            if (fontScaleLevel === 2 && btnFontInc) btnFontInc.classList.add('active');
        }

        function setFontScale(level) {
            fontScaleLevel = Math.max(-1, Math.min(2, level));
            document.documentElement.style.fontSize = scaleValues[fontScaleLevel];
            updateFontScaleButtons();
        }

        if (btnFontDec) {
            btnFontDec.addEventListener('click', () => setFontScale(fontScaleLevel - 1));
        }
        if (btnFontReset) {
            btnFontReset.addEventListener('click', () => setFontScale(0));
        }
        if (btnFontInc) {
            btnFontInc.addEventListener('click', () => setFontScale(fontScaleLevel + 1));
        }

        // Contrast
        if (btnContrastToggle) {
            btnContrastToggle.addEventListener('click', () => {
                document.body.classList.toggle('high-contrast');
                btnContrastToggle.classList.toggle('active', document.body.classList.contains('high-contrast'));
            });
        }

        // Spacing
        if (btnSpacingToggle) {
            btnSpacingToggle.addEventListener('click', () => {
                document.body.classList.toggle('generous-spacing');
                btnSpacingToggle.classList.toggle('active', document.body.classList.contains('generous-spacing'));
            });
        }

        // Links underline
        if (btnLinksToggle) {
            btnLinksToggle.addEventListener('click', () => {
                document.body.classList.toggle('links-underlined');
                btnLinksToggle.classList.toggle('active', document.body.classList.contains('links-underlined'));
            });
        }

        // Dyslexia
        if (btnDyslexiaToggle) {
            btnDyslexiaToggle.addEventListener('click', () => {
                document.body.classList.toggle('font-dyslexia');
                btnDyslexiaToggle.classList.toggle('active', document.body.classList.contains('font-dyslexia'));
            });
        }

        // Reset
        if (btnAccReset) {
            btnAccReset.addEventListener('click', () => {
                setFontScale(0);
                document.body.classList.remove('high-contrast', 'generous-spacing', 'links-underlined', 'font-dyslexia');
                [btnContrastToggle, btnSpacingToggle, btnLinksToggle, btnDyslexiaToggle].forEach(b => {
                    if (b) b.classList.remove('active');
                });
            });
        }
    }
});
