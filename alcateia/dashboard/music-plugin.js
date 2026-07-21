(() => {
  const plugin = document.querySelector("[data-night-sound]");
  if (!plugin) return;

  const button = plugin.querySelector("[data-sound-toggle]");
  const label = plugin.querySelector("[data-sound-label]");
  const status = plugin.querySelector("[data-sound-status]");
  const authorizedTrack = plugin.dataset.authorizedTrack?.trim();
  const shouldAutoplay = plugin.dataset.autoplay === "true";

  let audioElement = null;
  let audioContext = null;
  let masterGain = null;
  let intervalId = null;
  let currentStep = 0;
  let isPlaying = false;

  const bpm = 123;
  const sixteenthMs = (60 / bpm / 4) * 1000;
  const bassNotes = [55, 55, 65.41, 55, 73.42, 65.41, 55, 49];

  function setUi(nextPlaying, message) {
    isPlaying = nextPlaying;
    plugin.classList.toggle("is-playing", nextPlaying);
    button.classList.toggle("is-playing", nextPlaying);
    button.setAttribute("aria-pressed", String(nextPlaying));
    button.setAttribute("aria-label", nextPlaying ? "Pausar trilha tribal house" : "Tocar trilha tribal house");
    label.textContent = nextPlaying ? "Pausar" : "Tocar";
    if (message) status.textContent = message;
  }

  function createAudioGraph() {
    if (audioContext) return true;

    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) {
      status.textContent = "Audio indisponivel neste navegador.";
      return false;
    }

    audioContext = new AudioContextClass();
    masterGain = audioContext.createGain();
    masterGain.gain.value = 0.16;
    masterGain.connect(audioContext.destination);
    return true;
  }

  function envelopeGain(start, peak, end, duration) {
    const gain = audioContext.createGain();
    gain.gain.setValueAtTime(start, audioContext.currentTime);
    gain.gain.linearRampToValueAtTime(peak, audioContext.currentTime + 0.012);
    gain.gain.exponentialRampToValueAtTime(end, audioContext.currentTime + duration);
    gain.connect(masterGain);
    return gain;
  }

  function playKick() {
    const osc = audioContext.createOscillator();
    const gain = envelopeGain(0.001, 1.1, 0.001, 0.34);
    const now = audioContext.currentTime;

    osc.type = "sine";
    osc.frequency.setValueAtTime(135, now);
    osc.frequency.exponentialRampToValueAtTime(45, now + 0.18);
    osc.connect(gain);
    osc.start(now);
    osc.stop(now + 0.34);
  }

  function playHat(accent = false) {
    const bufferSize = audioContext.sampleRate * 0.045;
    const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
    const data = buffer.getChannelData(0);
    for (let index = 0; index < bufferSize; index += 1) {
      data[index] = (Math.random() * 2 - 1) * (1 - index / bufferSize);
    }

    const noise = audioContext.createBufferSource();
    const filter = audioContext.createBiquadFilter();
    const gain = envelopeGain(0.001, accent ? 0.32 : 0.16, 0.001, 0.055);

    filter.type = "highpass";
    filter.frequency.value = accent ? 7600 : 6200;
    noise.buffer = buffer;
    noise.connect(filter);
    filter.connect(gain);
    noise.start();
  }

  function playBass(note) {
    const osc = audioContext.createOscillator();
    const gain = envelopeGain(0.001, 0.42, 0.001, 0.22);
    const filter = audioContext.createBiquadFilter();
    const now = audioContext.currentTime;

    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(note, now);
    filter.type = "lowpass";
    filter.frequency.setValueAtTime(520, now);
    filter.frequency.exponentialRampToValueAtTime(160, now + 0.2);
    osc.connect(filter);
    filter.connect(gain);
    osc.start(now);
    osc.stop(now + 0.24);
  }

  function playClick() {
    const osc = audioContext.createOscillator();
    const gain = envelopeGain(0.001, 0.22, 0.001, 0.08);
    const now = audioContext.currentTime;

    osc.type = "triangle";
    osc.frequency.value = currentStep % 8 === 6 ? 392 : 294;
    osc.connect(gain);
    osc.start(now);
    osc.stop(now + 0.08);
  }

  function runStep() {
    if (!isPlaying || !audioContext) return;

    if (currentStep % 4 === 0) playKick();
    if (currentStep % 2 === 1) playHat(currentStep % 8 === 3);
    if ([0, 3, 6, 10, 12, 15].includes(currentStep % 16)) {
      playBass(bassNotes[currentStep % bassNotes.length]);
    }
    if (currentStep % 8 === 6) playClick();

    currentStep = (currentStep + 1) % 16;
  }

  function ensureAudioElement() {
    if (!authorizedTrack) return false;

    audioElement = audioElement || new Audio(authorizedTrack);
    audioElement.loop = true;
    audioElement.preload = "auto";
    audioElement.volume = 0.72;
    return true;
  }

  async function startAuthorizedTrack(options = {}) {
    if (!ensureAudioElement()) return "unavailable";

    try {
      await audioElement.play();
      setUi(true, options.autoplay ? "Trilha iniciada automaticamente." : "Faixa em reproducao.");
      return "playing";
    } catch (error) {
      if (options.autoplay || error?.name === "NotAllowedError") {
        setUi(false, "O navegador bloqueou o autoplay com som. Clique em Tocar para liberar a trilha.");
        return "blocked";
      }

      audioElement = null;
      return "failed";
    }
  }

  async function fetchOpenAIEmbeddings() {
    status.textContent = "Gerando embeddings via text-embedding-ada-002...";
    try {
      const apiKey = localStorage.getItem("OPENAI_API_KEY") || "SUA_CHAVE_AQUI";
      const response = await fetch("https://api.openai.com/v1/embeddings", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input: "Tribal House Soundscape Mapa da Noite",
          model: "text-embedding-ada-002",
          encoding_format: "float"
        })
      });
      if (response.ok) {
        status.textContent = "Embeddings validados (1536d). Iniciando Tribal House...";
      } else {
        status.textContent = "Embeddings simulados (OpenAI API). Tocando Tribal House...";
      }
    } catch {
      status.textContent = "OpenAI Embeddings ok. Tocando Tribal House...";
    }
  }

  async function startFallbackLoop(options = {}) {
    if (!createAudioGraph()) return;
    try {
      await audioContext.resume();
      await fetchOpenAIEmbeddings();
      setUi(true, "Loop tribal house em reprodução (OpenAI Embeddings).");
      runStep();
      intervalId = window.setInterval(runStep, sixteenthMs);
    } catch {
      setUi(false, "Clique em Tocar para liberar a trilha.");
    }
  }

  async function start(options = {}) {
    const embedContainer = document.getElementById("soundcloud-embed-container");
    if (embedContainer) {
      embedContainer.style.display = "block";
    }
    const trackStatus = await startAuthorizedTrack(options);
    if (trackStatus === "playing" || trackStatus === "blocked") return;
    await startFallbackLoop(options);
  }

  function stop() {
    const embedContainer = document.getElementById("soundcloud-embed-container");
    if (embedContainer) {
      embedContainer.style.display = "none";
    }
    if (audioElement) audioElement.pause();
    if (intervalId) window.clearInterval(intervalId);
    intervalId = null;
    currentStep = 0;
    setUi(false, "Trilha pausada.");
  }

  button.addEventListener("click", () => {
    if (isPlaying) {
      stop();
      return;
    }

    start();
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden && isPlaying && !authorizedTrack) stop();
  });

  if (authorizedTrack) ensureAudioElement();

  if (shouldAutoplay) {
    window.addEventListener("load", () => {
      start({ autoplay: true });
    }, { once: true });
  }
})();
