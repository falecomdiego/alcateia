const axisFilters = [
  { label: "Todos", type: "all", value: "all" },
  { label: "Operação", type: "axis", value: "operacao" },
  { label: "Experiência", type: "axis", value: "experiencia" },
  { label: "Sinais complementares com blindagem", type: "axis", value: "blindagem" }
];

const operationFields = [
  "fila",
  "entrada",
  "bar",
  "banheiro",
  "circulação",
  "som",
  "acesso",
  "estrutura",
  "organização"
];

const experienceFields = [
  "clima",
  "vibe",
  "encantamento",
  "frustração",
  "acolhimento",
  "desejo de retorno",
  "valor percebido",
  "experiência geral"
];

const publicSignals = [
  {
    id: "op-entrada",
    axis: "operacao",
    axisLabel: "Operação",
    field: "entrada",
    title: "Entrada",
    type: "Sinal operacional agregado",
    recurrence: 92,
    reading: "Recorrências indicam a entrada como ponto de atenção no funcionamento da experiência.",
    care: "Leitura agregada sobre fluxo e chegada, sem atribuição pública de causa."
  },
  {
    id: "op-fila",
    axis: "operacao",
    axisLabel: "Operação",
    field: "fila",
    title: "Fila",
    type: "Sinal operacional agregado",
    recurrence: 76,
    reading: "Percepções recorrentes apontam fila e tempo de espera como sinais de operação a acompanhar.",
    care: "A recorrência indica percepção pública, não avaliação automática de agentes."
  },
  {
    id: "op-bar",
    axis: "operacao",
    axisLabel: "Operação",
    field: "bar",
    title: "Bar",
    type: "Sinal operacional agregado",
    recurrence: 64,
    reading: "Sinais agregados conectam bar, atendimento e ritmo de serviço à experiência percebida.",
    care: "O dado é apresentado em conjunto e não funciona como comparação entre espaços."
  },
  {
    id: "op-som",
    axis: "operacao",
    axisLabel: "Operação",
    field: "som",
    title: "Som",
    type: "Sinal operacional agregado",
    recurrence: 36,
    reading: "Percepções sobre som aparecem como sinal operacional ligado à experiência da noite.",
    care: "A leitura não atribui causa pública a equipe, artista, casa ou marca."
  },
  {
    id: "op-banheiro",
    axis: "operacao",
    axisLabel: "Operação",
    field: "banheiro",
    title: "Banheiro",
    type: "Sinal operacional agregado",
    recurrence: 9,
    reading: "Comentários agregados indicam banheiro como campo operacional com efeito sobre conforto e circulação.",
    care: "A recorrência é baixa e deve ser lida com cuidado de exposição."
  },
  {
    id: "op-acesso",
    axis: "operacao",
    axisLabel: "Operação",
    field: "acesso",
    title: "Acesso",
    type: "Sinal operacional agregado",
    recurrence: 9,
    reading: "Acesso aparece como sinal agregado associado à chegada e orientação do público.",
    care: "Sinal público agregado, sem inferência acusatória e sem individualização."
  },
  {
    id: "ex-desejo-retorno",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "desejo de retorno",
    title: "Desejo de retorno",
    type: "Sinal experiencial agregado",
    recurrence: 200,
    reading: "A vontade de retornar aparece como percepção forte na leitura agregada da rodada.",
    care: "O sinal indica tendência de percepção, não medida totalizante da cena."
  },
  {
    id: "ex-encantamento",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "encantamento",
    title: "Encantamento",
    type: "Sinal experiencial agregado",
    recurrence: 62,
    reading: "Encantamento aparece ligado a surpresa positiva, memória e brilho percebido.",
    care: "A leitura preserva o caráter subjetivo das percepções públicas."
  },
  {
    id: "ex-frustracao",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "frustração",
    title: "Frustração",
    type: "Sinal experiencial agregado",
    recurrence: 48,
    reading: "Frustração aparece como percepção vivida associada a expectativas e atritos da experiência.",
    care: "Recorrência não é acusação e não identifica agentes públicos."
  },
  {
    id: "ex-acolhimento",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "acolhimento",
    title: "Acolhimento",
    type: "Sinal experiencial agregado",
    recurrence: 28,
    reading: "Acolhimento aparece como sinal de pertencimento, recepção e conforto social.",
    care: "O sinal é agregado e não substitui escutas qualitativas aprofundadas."
  },
  {
    id: "ex-valor",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "valor percebido",
    title: "Valor percebido",
    type: "Sinal experiencial agregado",
    recurrence: 7,
    reading: "Valor percebido aparece como relação entre expectativa, entrega e satisfação pública.",
    care: "A baixa recorrência exibida pede leitura cautelosa e sem afirmação forte."
  },
  {
    id: "ex-geral",
    axis: "experiencia",
    axisLabel: "Experiência",
    field: "experiência geral",
    title: "Experiência geral",
    type: "Sinal experiencial agregado",
    recurrence: 4,
    reading: "Sinais gerais ajudam a contextualizar a vivência sem reduzir a noite a uma nota única.",
    care: "Campo de leitura ampla, usado apenas como percepção pública agregada."
  },
  {
    id: "bl-cuidado",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "saúde, cuidado e segurança",
    title: "Cuidado e segurança",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Tema complementar tratado apenas como contexto de cuidado, sem exposição de pessoas ou situações identificáveis.",
    care: "Não há atribuição pública de causa e não há individualização de agentes."
  },
  {
    id: "bl-curadoria",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "histórico-musical e curatorial",
    title: "Histórico-musical e curatorial",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Percepções musicais e curatoriais aparecem apenas como apoio de contexto da experiência.",
    care: "O painel não compara artistas, casas, festas ou marcas."
  },
  {
    id: "bl-reputacao",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "reputação e decisão estratégica",
    title: "Reputação e decisão estratégica",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Sinais reputacionais entram apenas como leitura agregada de percepção pública.",
    care: "Sem leitura acusatória e sem individualização de organizações."
  },
  {
    id: "bl-economia",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "economia da experiência",
    title: "Economia da experiência",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Percepções sobre valor e entrega aparecem como contexto, sem transformar comentários em juízo público.",
    care: "Sinal complementar, agregado e sem conclusão forte sobre agentes."
  },
  {
    id: "bl-bastidores",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "trabalho, bastidores e cadeia produtiva",
    title: "Trabalho e bastidores",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Temas de bastidores ficam protegidos e aparecem apenas quando ajudam a contextualizar a leitura pública.",
    care: "Sem exposição de equipes, trabalhadores, produtores ou organizações."
  },
  {
    id: "bl-sociocultural",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "sociocultural e linguística",
    title: "Sociocultural e linguística",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Termos e códigos da cena são tratados com cautela, sem leitura pública forte.",
    care: "Uso condicionado para evitar interpretação indevida ou exposição simbólica."
  },
  {
    id: "bl-governanca",
    axis: "blindagem",
    axisLabel: "Sinais complementares com blindagem",
    field: "governança, ética e proteção de dados",
    title: "Governança e dados",
    type: "Sinal complementar com blindagem",
    recurrence: null,
    reading: "Governança aparece como transparência metodológica sobre anonimização, agregação e cuidado de exposição.",
    care: "Bloco de apoio, não eixo narrativo principal."
  }
];

let activeFilter = { type: "all", value: "all", label: "Todos os sinais agregados" };

const $ = (selector, root = document) => root.querySelector(selector);

function formatNumber(value) {
  if (value === null || value === undefined) return "recorrência não exibida";
  return new Intl.NumberFormat("pt-BR").format(value);
}

function buttonMarkup(item, extraClass = "") {
  return `<button type="button" class="filter-button ${extraClass}" data-filter-type="${item.type}" data-filter-value="${item.value}">${item.label}</button>`;
}

function renderFilters() {
  $("#axis-filters").innerHTML = axisFilters.map((item) => buttonMarkup(item)).join("");
  $("#operation-filters").innerHTML = operationFields
    .map((field) => buttonMarkup({ label: field, type: "field", value: field }, "field-filter"))
    .join("");
  $("#experience-filters").innerHTML = experienceFields
    .map((field) => buttonMarkup({ label: field, type: "field", value: field }, "field-filter"))
    .join("");

  document.querySelectorAll(".filter-button").forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = {
        type: button.dataset.filterType,
        value: button.dataset.filterValue,
        label: button.textContent.trim()
      };
      renderDashboard();
    });
  });
}

function matchesFilter(signal) {
  if (activeFilter.type === "all") return true;
  if (activeFilter.type === "axis") return signal.axis === activeFilter.value;
  if (activeFilter.type === "field") return signal.field === activeFilter.value;
  return true;
}

function filteredSignals() {
  return publicSignals.filter(matchesFilter);
}

function renderCounts(signals) {
  $("#visible-count").textContent = formatNumber(signals.length);
  $("#active-filter-label").textContent = activeFilter.type === "all"
    ? "Todos os sinais agregados"
    : `Filtro ativo: ${activeFilter.label}`;
  $("#operation-count").textContent = formatNumber(publicSignals.filter((signal) => signal.axis === "operacao").length);
  $("#experience-count").textContent = formatNumber(publicSignals.filter((signal) => signal.axis === "experiencia").length);
  $("#protected-count").textContent = formatNumber(publicSignals.filter((signal) => signal.axis === "blindagem").length);
}

function renderActiveButtons() {
  document.querySelectorAll(".filter-button").forEach((button) => {
    const active = button.dataset.filterType === activeFilter.type && button.dataset.filterValue === activeFilter.value;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", active ? "true" : "false");
  });
}

function signalCard(signal) {
  const recurrence = signal.recurrence === null || signal.recurrence === undefined
    ? "Recorrência não exibida nesta versão"
    : `${formatNumber(signal.recurrence)} recorrências agregadas`;

  return `
    <article class="evidence-card" data-axis="${signal.axis}" data-field="${signal.field}">
      <div class="card-kicker">${signal.axisLabel}</div>
      <h3>${signal.title}</h3>
      <dl>
        <div><dt>Tipo de sinal</dt><dd>${signal.type}</dd></div>
        <div><dt>Quantidade</dt><dd>${recurrence}</dd></div>
      </dl>
      <p>${signal.reading}</p>
      <p class="care-note">${signal.care}</p>
      <p class="cause-note">Sem atribuição pública de causa.</p>
    </article>
  `;
}

function renderEvidence(signals) {
  const grid = $("#evidence-grid");
  const empty = $("#empty-state");
  $("#result-status").textContent = `${formatNumber(signals.length)} sinais exibidos`;
  grid.innerHTML = signals.map(signalCard).join("");
  empty.hidden = signals.length > 0;
}

function renderAxisGrid(selector, axis) {
  const rows = publicSignals.filter((signal) => signal.axis === axis);
  $(selector).innerHTML = rows.map(signalCard).join("");
}

function renderDashboard() {
  const signals = filteredSignals();
  renderCounts(signals);
  renderActiveButtons();
  renderEvidence(signals);
}

function setupNavigation() {
  const navLinks = Array.from(document.querySelectorAll(".desktop-nav a, .mobile-nav a"));
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const setActiveLink = (id) => {
    navLinks.forEach((link) => {
      link.toggleAttribute("aria-current", link.getAttribute("href") === `#${id}`);
    });
  };

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible?.target?.id) setActiveLink(visible.target.id);
      },
      { rootMargin: "-20% 0px -65% 0px", threshold: [0.12, 0.35, 0.6] }
    );
    sections.forEach((section) => observer.observe(section));
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", link.getAttribute("href"));
    });
  });
}

renderFilters();
renderAxisGrid("#operation-grid", "operacao");
renderAxisGrid("#experience-grid", "experiencia");
renderAxisGrid("#protected-grid", "blindagem");
renderDashboard();
setupNavigation();
