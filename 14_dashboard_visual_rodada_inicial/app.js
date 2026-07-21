const state = {
  data: null,
  mode: "executiva",
  page: 1,
  pageSize: 12,
  filters: {
    lote: "",
    perfil: "",
    natureza: "",
    eixo: "",
    prioridade: "",
    polaridade: "",
    categoria: "",
    entidade: "",
    search: ""
  }
};

const priorityRank = { alta: 0, media: 1, baixa: 2, monitorar: 3 };

const displayLabels = {
  acao: "a\u00e7\u00e3o",
  atendimento: "atendimento",
  banheiro: "banheiro",
  bar: "bar",
  baixa: "baixa",
  climatizacao: "climatiza\u00e7\u00e3o",
  compra: "compra",
  comunicacional: "comunicacional",
  decepcao: "decep\u00e7\u00e3o",
  desejo: "desejo",
  encanto: "encanto",
  entrada: "entrada",
  experiencia: "experi\u00eancia",
  experiencia_do_publico: "experi\u00eancia do p\u00fablico",
  experiencial: "experiencial",
  expectativa: "expectativa",
  fila: "fila",
  frustracao: "frustra\u00e7\u00e3o",
  gestao_do_evento: "gest\u00e3o do evento",
  identificacao: "identifica\u00e7\u00e3o",
  iluminacao: "ilumina\u00e7\u00e3o",
  intencao_de_retorno: "inten\u00e7\u00e3o de retorno",
  lotacao: "lota\u00e7\u00e3o",
  media: "m\u00e9dia",
  memoria_afetiva: "mem\u00f3ria afetiva",
  misto: "misto",
  monitoramento: "monitoramento",
  operacional: "operacional",
  operacao: "opera\u00e7\u00e3o",
  palco: "palco",
  pertencimento: "pertencimento",
  preco: "pre\u00e7o",
  producao: "produ\u00e7\u00e3o",
  recomendacao_espontanea: "recomenda\u00e7\u00e3o espont\u00e2nea",
  rejeicao: "rejei\u00e7\u00e3o",
  relacional: "relacional",
  reputacional: "reputa\u00e7\u00e3o",
  revista: "revista",
  seguranca: "seguran\u00e7a",
  sinalizacao: "sinaliza\u00e7\u00e3o",
  som: "som",
  status: "status",
  transporte: "transporte"
};

const textReplacements = [
  [/\bNao\b/g, "N\u00e3o"],
  [/\bnao\b/g, "n\u00e3o"],
  [/\bProxima\b/g, "Pr\u00f3xima"],
  [/\bRecomendacoes\b/g, "Recomenda\u00e7\u00f5es"],
  [/\brecomendacoes\b/g, "recomenda\u00e7\u00f5es"],
  [/\bRecomendacao\b/g, "Recomenda\u00e7\u00e3o"],
  [/\brecomendacao\b/g, "recomenda\u00e7\u00e3o"],
  [/\bEvidencias\b/g, "Evid\u00eancias"],
  [/\bevidencias\b/g, "evid\u00eancias"],
  [/\bevidencia\b/g, "evid\u00eancia"],
  [/\bocorrencias\b/g, "ocorr\u00eancias"],
  [/\bunicas\b/g, "\u00fanicas"],
  [/\bMencao\b/g, "Men\u00e7\u00e3o"],
  [/\bmencao\b/g, "men\u00e7\u00e3o"],
  [/\bMencoes\b/g, "Men\u00e7\u00f5es"],
  [/\bmencoes\b/g, "men\u00e7\u00f5es"],
  [/\bextraida\b/g, "extra\u00edda"],
  [/\bextraidas\b/g, "extra\u00eddas"],
  [/\btecnico\b/g, "t\u00e9cnico"],
  [/\btecnicos\b/g, "t\u00e9cnicos"],
  [/\bnavegavel\b/g, "naveg\u00e1vel"],
  [/\bmetodologica\b/g, "metodol\u00f3gica"],
  [/\bmetodologicas\b/g, "metodol\u00f3gicas"],
  [/\bpossivel\b/g, "poss\u00edvel"],
  [/\bcomentarios\b/g, "coment\u00e1rios"],
  [/\bcomentario\b/g, "coment\u00e1rio"],
  [/\bexperiencia\b/g, "experi\u00eancia"],
  [/\boperacao\b/g, "opera\u00e7\u00e3o"],
  [/\breducao\b/g, "redu\u00e7\u00e3o"],
  [/\brecorrencia\b/g, "recorr\u00eancia"],
  [/\bacao\b/g, "a\u00e7\u00e3o"],
  [/\bpreco\b/g, "pre\u00e7o"],
  [/\bseguranca\b/g, "seguran\u00e7a"],
  [/\brejeicao\b/g, "rejei\u00e7\u00e3o"],
  [/\bidentificacao\b/g, "identifica\u00e7\u00e3o"],
  [/\blotacao\b/g, "lota\u00e7\u00e3o"],
  [/\bsinalizacao\b/g, "sinaliza\u00e7\u00e3o"],
  [/\bclimatizacao\b/g, "climatiza\u00e7\u00e3o"],
  [/\bdecepcao\b/g, "decep\u00e7\u00e3o"],
  [/\bpublico\b/g, "p\u00fablico"],
  [/\bvalidacao\b/g, "valida\u00e7\u00e3o"],
  [/\batribuicao\b/g, "atribui\u00e7\u00e3o"],
  [/\borganizacoes\b/g, "organiza\u00e7\u00f5es"],
  [/\bavaliacao\b/g, "avalia\u00e7\u00e3o"],
  [/\bdiagnostico\b/g, "diagn\u00f3stico"],
  [/\bproducao\b/g, "produ\u00e7\u00e3o"],
  [/recomendacao_espontanea/g, "recomenda\u00e7\u00e3o espont\u00e2nea"],
  [/intencao_de_retorno/g, "inten\u00e7\u00e3o de retorno"],
  [/memoria_afetiva/g, "mem\u00f3ria afetiva"],
  [/gestao_do_evento/g, "gest\u00e3o do evento"],
  [/experiencia_do_publico/g, "experi\u00eancia do p\u00fablico"],
  [/arquivo_origem/g, "arquivo de origem"],
  [/perfil_proxy/g, "perfil proxy"],
  [/categorias_relacionadas/g, "categorias relacionadas"],
  [/total_comentarios_considerados/g, "total de coment\u00e1rios considerados"],
  [/total_perfis_monitorados/g, "total de perfis monitorados"],
  [/entidade_monitorada/g, "entidade monitorada"],
  [/categoria_principal/g, "categoria principal"],
  [/categoria_secundaria/g, "categoria secund\u00e1ria"]
];

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function normalize(value) {
  return String(value ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function formatNumber(value) {
  return new Intl.NumberFormat("pt-BR").format(Number(value || 0));
}

function displayLabel(value) {
  const raw = String(value ?? "");
  const key = normalize(raw).replace(/[\s-]+/g, "_");
  return displayLabels[key] || raw;
}

function displayText(value) {
  const raw = String(value ?? "");
  const exact = displayLabel(raw);
  let text = exact !== raw ? exact : raw;
  textReplacements.forEach(([pattern, replacement]) => {
    text = text.replace(pattern, replacement);
  });
  return text;
}

function displayArea(value) {
  if (!value) return "sem \u00e1rea sugerida";
  const area = displayText(value);
  return area === "sem responsavel" || area === "sem respons\u00e1vel" ? "sem \u00e1rea sugerida" : area;
}

function labelValue(row) {
  return row.label ?? row.eixo ?? row.macroproblema ?? row.perfil_proxy ?? row.entidade_textual ?? "";
}

function numericValue(row) {
  return Number(row.value ?? row.volume ?? row.ocorrencias_vinculadas ?? row.mencoes_em_evidencias ?? 0);
}

function badgeClass(priority) {
  const p = normalize(priority);
  if (p === "alta") return "badge high";
  if (p === "media") return "badge medium";
  if (p === "baixa") return "badge low";
  return "badge";
}

async function loadData() {
  if (window.MAPA_DA_NOITE_DATA) return window.MAPA_DA_NOITE_DATA;
  const response = await fetch("data/dashboard_data.json");
  if (!response.ok) throw new Error("N\u00e3o foi poss\u00edvel carregar os dados do painel.");
  return response.json();
}

function fillSelect(id, values, firstLabel) {
  const select = $(id);
  select.innerHTML = "";
  const first = document.createElement("option");
  first.value = "";
  first.textContent = firstLabel;
  select.appendChild(first);
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = displayText(value);
    select.appendChild(option);
  });
}

function setupFilters() {
  const filtros = state.data.filtros;
  fillSelect("#filter-lote", filtros.lote, "Todos");
  fillSelect("#filter-perfil", filtros.perfil_proxy, "Todos");
  fillSelect("#filter-natureza", filtros.natureza, "Todas");
  fillSelect("#filter-eixo", filtros.eixo, "Todos");
  fillSelect("#filter-prioridade", filtros.prioridade, "Todas");
  fillSelect("#filter-polaridade", filtros.polaridade, "Todas");
  fillSelect("#filter-categoria", filtros.categoria_validada, "Todas");
  fillSelect("#filter-entidade", filtros.entidade_textual, "Todas");

  const map = {
    "#filter-lote": "lote",
    "#filter-perfil": "perfil",
    "#filter-natureza": "natureza",
    "#filter-eixo": "eixo",
    "#filter-prioridade": "prioridade",
    "#filter-polaridade": "polaridade",
    "#filter-categoria": "categoria",
    "#filter-entidade": "entidade"
  };

  Object.entries(map).forEach(([selector, key]) => {
    $(selector).addEventListener("change", (event) => {
      state.filters[key] = event.target.value;
      state.page = 1;
      renderDynamicViews();
    });
  });

  $("#filter-search").addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    state.page = 1;
    renderDynamicViews();
  });

  $("#clear-filters").addEventListener("click", () => {
    Object.keys(state.filters).forEach((key) => {
      state.filters[key] = "";
    });
    Object.keys(map).forEach((selector) => {
      $(selector).value = "";
    });
    $("#filter-search").value = "";
    state.page = 1;
    renderDynamicViews();
  });
}

function setupModeButtons() {
  $$(".mode-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      state.page = 1;
      $$(".mode-button").forEach((item) => item.classList.toggle("active", item === button));
      renderTable();
      renderRecommendations();
    });
  });

  $("#prev-page").addEventListener("click", () => {
    state.page = Math.max(1, state.page - 1);
    renderTable();
  });

  $("#next-page").addEventListener("click", () => {
    state.page += 1;
    renderTable();
  });
}

function renderStatus() {
  const meta = state.data.metadata;
  $("#status-strip").innerHTML = [
    ["Lotes usados", meta.lotes_incluidos.join(" | ")],
    ["N\u00e3o pertencem a esta rodada", meta.lotes_excluidos.join(" | ")],
    ["Fonte", "5 arquivos oficiais validados"]
  ]
    .map(([label, value]) => `<div class="status-pill"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`)
    .join("");
}

function renderKpis() {
  const totals = state.data.totais;
  const high = state.data.sumarios.prioridades_executivas.find((row) => normalize(row.label) === "alta");
  $("#kpi-problems").textContent = formatNumber(totals.problemas_resolutivos);
  $("#kpi-macro").textContent = formatNumber(totals.macroproblemas);
  $("#kpi-profiles").textContent = formatNumber(totals.perfis_proxy_rastreados);
  $("#kpi-lines").textContent = formatNumber(totals.linhas_evidencia_unicas_proxy);
  $("#kpi-high").textContent = formatNumber(high?.value || 0);
  $("#kpi-no-evidence").textContent = formatNumber(totals.recomendacoes_executivas_sem_evidencia);
}

function renderBars(selector, rows, options = {}) {
  const mutedLabels = new Set((options.mutedLabels || []).map(normalize));
  const max = Math.max(1, ...rows.map(numericValue));
  $(selector).innerHTML = rows
    .map((row) => {
      const label = labelValue(row);
      const value = numericValue(row);
      const width = Math.max(3, Math.round((value / max) * 100));
      const muted = mutedLabels.has(normalize(label)) ? " muted-datum" : "";
      return `
        <div class="bar-row${muted}">
          <span class="bar-label">${escapeHtml(displayText(label))}</span>
          <span class="bar-track"><span class="bar-fill" style="width:${width}%"></span></span>
          <strong class="bar-value">${formatNumber(value)}</strong>
        </div>
      `;
    })
    .join("");
}

function renderStaticCharts() {
  renderBars("#chart-priority", state.data.sumarios.prioridades_executivas);
  renderBars("#chart-nature", state.data.sumarios.naturezas_executivas);
  renderBars("#chart-axis", state.data.sumarios.eixos_executivos);
  renderBars("#chart-op-exp", state.data.sumarios.operacao_experiencia, { mutedLabels: ["indefinido"] });
}

function renderRankList(selector, rows, valueKey, subtitleBuilder) {
  $(selector).innerHTML = rows
    .slice(0, 10)
    .map((row) => {
      const title = row.perfil_proxy || row.entidade_textual || row.macroproblema || "";
      const subtitle = subtitleBuilder(row);
      const value = row[valueKey] || 0;
      const safeTitle = row.perfil_proxy || row.entidade_textual ? title : displayText(title);
      return `
        <article class="rank-item">
          <div>
            <div class="rank-title">${escapeHtml(safeTitle)}</div>
            <div class="rank-subtitle">${escapeHtml(subtitle)}</div>
          </div>
          <strong class="rank-value">${formatNumber(value)}</strong>
        </article>
      `;
    })
    .join("");
}

function renderRankings() {
  renderRankList(
    "#ranking-best",
    state.data.rankings.perfis_mais_bem_avaliados_proxy,
    "polaridade_positiva",
    (row) => `${row.linhas_unicas} linhas \u00fanicas rastreadas | ${row.problemas_vinculados} problemas vinculados`
  );
  renderRankList(
    "#ranking-critical",
    state.data.rankings.perfis_maior_criticidade_proxy,
    "prioridade_alta",
    (row) => `${row.ocorrencias_vinculadas} ocorr\u00eancias vinculadas | ${row.polaridade_negativa} polaridade negativa`
  );
  renderRankList(
    "#ranking-entities",
    state.data.rankings.djs_entidades_textuais_proxy,
    "mencoes_em_evidencias",
    () => "Men\u00e7\u00e3o textual agregada, sem atribui\u00e7\u00e3o p\u00fablica de causa"
  );
}

function renderCompactList(selector, rows) {
  $(selector).innerHTML = rows
    .map((row) => `
      <article class="compact-item">
        <strong>${escapeHtml(displayText(row.macroproblema))}</strong>
        <div class="meta-line">${escapeHtml(displayText(row.eixo))} | ${escapeHtml(displayText(row.natureza))} | ${formatNumber(row.volume)} ocorr\u00eancias no universo analisado</div>
      </article>
    `)
    .join("");
}

function renderOperationExperience() {
  renderCompactList("#top-operational", state.data.rankings.problemas_operacionais);
  renderCompactList("#top-experiential", state.data.rankings.problemas_experienciais);
}

function rowText(row) {
  return [
    row.id,
    row.macroproblema,
    row.problema,
    row.problemas_agrupados,
    row.recomendacao,
    row.evidencia_textual,
    row.eixo,
    row.natureza,
    row.prioridade,
    row.polaridade,
    row.responsavel,
    row.indicador,
    (row.perfis_proxy || []).join(" "),
    (row.categorias || []).join(" ")
  ].join(" ");
}

function rowMatches(row) {
  const f = state.filters;
  if (f.lote && !(row.lotes || []).includes(f.lote)) return false;
  if (f.perfil && !(row.perfis_proxy || []).includes(f.perfil)) return false;
  if (f.natureza && row.natureza !== f.natureza) return false;
  if (f.eixo && row.eixo !== f.eixo) return false;
  if (f.prioridade && row.prioridade !== f.prioridade) return false;
  if (f.polaridade && row.polaridade !== f.polaridade) return false;
  if (f.categoria && !(row.categorias || []).includes(f.categoria)) return false;
  if (f.entidade && !normalize(row.evidencia_textual).includes(normalize(f.entidade))) return false;
  if (f.search && !normalize(rowText(row)).includes(normalize(f.search))) return false;
  return true;
}

function currentRows() {
  const source = state.mode === "executiva" ? state.data.matriz_executiva : state.data.matriz_detalhada;
  return source
    .filter(rowMatches)
    .sort((a, b) => {
      const byPriority = (priorityRank[normalize(a.prioridade)] ?? 9) - (priorityRank[normalize(b.prioridade)] ?? 9);
      if (byPriority !== 0) return byPriority;
      return (b.volume || 0) - (a.volume || 0);
    });
}

function renderTable() {
  const rows = currentRows();
  const totalPages = Math.max(1, Math.ceil(rows.length / state.pageSize));
  state.page = Math.min(state.page, totalPages);
  const start = (state.page - 1) * state.pageSize;
  const pageRows = rows.slice(start, start + state.pageSize);

  $("#table-count").textContent = `${formatNumber(rows.length)} registros filtrados`;
  $("#page-label").textContent = `${state.page} / ${totalPages}`;
  $("#prev-page").disabled = state.page <= 1;
  $("#next-page").disabled = state.page >= totalPages;

  const executive = state.mode === "executiva";
  const heads = executive
    ? ["Macroproblema", "Prioridade", "Ocorr\u00eancias no universo analisado", "Eixo", "Natureza", "Recomenda\u00e7\u00e3o", "Evid\u00eancias"]
    : ["Problema", "Prioridade", "Ocorr\u00eancias no universo analisado", "Eixo", "Natureza", "Recomenda\u00e7\u00e3o", "Evid\u00eancias"];

  $("#matrix-head").innerHTML = `<tr>${heads.map((h) => `<th>${escapeHtml(h)}</th>`).join("")}</tr>`;
  $("#matrix-body").innerHTML = pageRows
    .map((row, index) => {
      const title = executive ? row.macroproblema : row.problema;
      const evidence = row.evidencias?.[0] || "";
      return `
        <tr data-row-index="${start + index}">
          <td><strong>${escapeHtml(displayText(title))}</strong><div class="meta-line">${escapeHtml(row.id)}</div></td>
          <td><span class="${badgeClass(row.prioridade)}">${escapeHtml(displayText(row.prioridade || "sem prioridade"))}</span></td>
          <td>${formatNumber(row.volume)}</td>
          <td>${escapeHtml(displayText(row.eixo))}</td>
          <td>${escapeHtml(displayText(row.natureza))}</td>
          <td>${escapeHtml(displayText(row.recomendacao || "sem recomendacao registrada"))}</td>
          <td>${escapeHtml(evidence)}</td>
        </tr>
      `;
    })
    .join("");

  $$("#matrix-body tr").forEach((tr) => {
    tr.addEventListener("click", () => {
      const row = rows[Number(tr.dataset.rowIndex)];
      renderDetail(row);
    });
  });

  if (pageRows[0]) {
    renderDetail(pageRows[0]);
  } else {
    $("#detail-panel").hidden = false;
    $("#detail-panel").innerHTML = `<div class="empty-state">Nenhum registro encontrado para os filtros aplicados.</div>`;
  }
}

function renderDetail(row) {
  const title = row.macroproblema || row.problema;
  const evidences = (row.evidencias || []).slice(0, 8);
  $("#detail-panel").hidden = false;
  $("#detail-panel").innerHTML = `
    <h3>${escapeHtml(displayText(title))}</h3>
    <div class="meta-line">
      ${escapeHtml(row.id)} | ${escapeHtml(displayText(row.prioridade))} | ${formatNumber(row.volume)} ocorr\u00eancias no universo analisado | ${escapeHtml((row.lotes || []).join(" | "))}
    </div>
    <p class="recommendation-text"><strong>Recomenda\u00e7\u00e3o:</strong> ${escapeHtml(displayText(row.recomendacao || "sem recomendacao registrada"))}</p>
    <div class="meta-line"><strong>Recortes monitorados por proxy t\u00e9cnico:</strong> ${escapeHtml((row.perfis_proxy || []).slice(0, 12).join(" | ") || "n\u00e3o identificado")}</div>
    <div class="meta-line"><strong>Blindagem:</strong> leitura contextual, sem atribui\u00e7\u00e3o p\u00fablica de causa; valida\u00e7\u00e3o interna necess\u00e1ria.</div>
    <ul class="evidence-list">
      ${evidences.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
    </ul>
  `;
}

function renderRecommendations() {
  const rows = state.data.matriz_executiva
    .filter(rowMatches)
    .filter((row) => row.recomendacao && row.evidencia_textual)
    .sort((a, b) => {
      const byPriority = (priorityRank[normalize(a.prioridade)] ?? 9) - (priorityRank[normalize(b.prioridade)] ?? 9);
      if (byPriority !== 0) return byPriority;
      return (b.volume || 0) - (a.volume || 0);
    })
    .slice(0, 18);

  $("#recommendation-grid").innerHTML = rows.length
    ? rows.map((row) => `
      <article class="recommendation-card">
        <div>
          <span class="${badgeClass(row.prioridade)}">${escapeHtml(displayText(row.prioridade))}</span>
        </div>
        <h3>${escapeHtml(displayText(row.macroproblema))}</h3>
        <p class="recommendation-text">${escapeHtml(displayText(row.recomendacao))}</p>
        <div class="meta-line">${formatNumber(row.volume)} ocorr\u00eancias no universo analisado | \u00c1rea sugerida para valida\u00e7\u00e3o interna: ${escapeHtml(displayArea(row.responsavel))}</div>
        <ul class="evidence-list">
          ${(row.evidencias || []).slice(0, 3).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </article>
    `).join("")
    : `<div class="empty-state">Nenhuma recomenda\u00e7\u00e3o com evid\u00eancia textual no recorte filtrado.</div>`;
}

function renderMethodology() {
  const meta = state.data.metadata;
  $("#proxy-list").innerHTML = Object.entries(meta.campos_proxy)
    .map(([field, text]) => `
      <article class="method-item">
        <strong>${escapeHtml(displayText(field.replace(/_/g, " ")))}</strong>
        <div class="meta-line">${escapeHtml(displayText(text))}</div>
      </article>
    `)
    .join("");

  $("#source-list").innerHTML = meta.fontes_oficiais
    .map((source) => `
      <article class="method-item">
        <strong>${escapeHtml(source.nome)}</strong>
        <div class="meta-line">Fonte oficial interna validada; caminho local ocultado na interface.</div>
        <div class="meta-line">${formatNumber(source.bytes)} bytes | sha256 ${escapeHtml(source.sha256_12)}</div>
      </article>
    `)
    .join("");
}

function renderDynamicViews() {
  renderTable();
  renderRecommendations();
}

function renderAll() {
  renderStatus();
  renderKpis();
  renderStaticCharts();
  renderRankings();
  renderOperationExperience();
  renderMethodology();
  renderDynamicViews();
}

loadData()
  .then((data) => {
    state.data = data;
    setupFilters();
    setupModeButtons();
    renderAll();
  })
  .catch((error) => {
    document.body.innerHTML = `<main class="section-block"><h1>Mapa da Noite</h1><p>${escapeHtml(error.message)}</p></main>`;
  });
