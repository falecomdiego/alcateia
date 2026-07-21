/* ==========================================
   ALCATEIA — ENGINE DE VISUALIZAÇÃO (v1.0)
   ========================================== */

// BASE DE DADOS DO MARCO ZERO (CASOS 1 E 2)
const domainData = {
    mapa_da_noite: {
        total_comentarios: "7.468",
        lbl_comentarios: "Interações humanas limpas",
        fontes_count: "30",
        pii_expurgado: "100%",
        latencia: "0.18s",
        badge_modelo: "GPT 5.6",
        badge_confianca: "Confiança Alta",
        rec_title: "Ampliar em 30% os caixas móveis e redistribuir pontos de hidratação na pista open air.",
        rec_hypothesis: "Demonstrado aumento de comentários críticos sobre filas prolongadas no atendimento de bar e escassez de água na pista de dança aberta.",
        sig_hash: "SHA-256: 4df8b65357efba30d690d5ed47b4b392b0c3b3a844d59e90fa84b1986e2e8fcb",
        sig_meta: "Assinado eletronicamente por Diego da Silva (Pesquisador-Chefe)",
        fontes: [
            { nome: "MDN-RPP01-COL-001.xlsx", hash: "a3f5b721e582d921b8c1..." },
            { nome: "MDN-RPP01-COL-002.xlsx", hash: "e28d4b901fc38201a09d..." },
            { nome: "MDN-RPP01-COL-003.xlsx", hash: "f8c5a201bcf392c10a4d..." },
            { nome: "MDN-RPP01-COL-004.xlsx", hash: "9d3a4c2810fec5b190a4..." },
            { nome: "MDN-RPP01-COL-005.xlsx", hash: "b20e4d101afc9201d0a5..." },
            { nome: "MDN-RPP01-COL-006.xlsx", hash: "c8e21a48ffc201a93b4f..." },
            { nome: "MDN-RPP01-COL-007.xlsx", hash: "20fa3c1b928fcc201b4e..." }
        ],
        evidencias: [
            {
                arquivo: "MDN-RPP01-COL-001.xlsx",
                linha: 142,
                lote: "lote_01",
                texto: "fiquei mais de 45 minutos na fila do bar do open air... o atendimento estava péssimo e a água acabou antes do show acabar... [PII_EMAIL_REMOVED]"
            },
            {
                arquivo: "MDN-RPP01-COL-003.xlsx",
                linha: 89,
                lote: "lote_01",
                texto: "a pista de dança open air é excelente, mas não tinha nenhum ponto de água ou hidratação por perto, fila do bar impossível [PII_PHONE_REMOVED]"
            },
            {
                arquivo: "MDN-RPP01-COL-006.xlsx",
                linha: 305,
                lote: "lote_02",
                texto: "filas gigantescas para comprar ficha e depois outra fila gigante para pegar a bebida... organização de atendimento falhou feio"
            }
        ],
        pipeline_steps: {
            1: {
                title: "Investigação (Discovery Service)",
                producer: "Discovery Agent (DiscoveryService)",
                model: "Codex Assistido",
                script: "alcateia/core/discovery.py",
                doc: "ALCATEIA-ARC-001-V1.0.md • Gate G0",
                reproduce: "python -m alcateia.main --context mapa_da_noite --question \"Como está a infraestrutura...\""
            },
            2: {
                title: "Execução (Execution Service — LGPD)",
                producer: "Saneador de Dados (ExecutionService)",
                model: "Expressões Regulares",
                script: "alcateia/core/execution.py",
                doc: "Regras 1, 2 e 5 do AGENTS.md • Gate G1",
                reproduce: "Módulo interno chamado automaticamente na execução em memória."
            },
            3: {
                title: "Evidências (Evidence Service)",
                producer: "Auditor de Origens (EvidenceService)",
                model: "Auditoria Criptográfica SHA-256",
                script: "alcateia/core/evidence.py",
                doc: "Regras de Integridade do Mapa da Noite • Gate G2",
                reproduce: "python -m unittest alcateia.tests.test_flow"
            },
            4: {
                title: "Recomendação (Reasoning Service)",
                producer: "Cognitive Agent (ReasoningService)",
                model: "GPT 5.6 (OpenAI API)",
                script: "alcateia/core/reasoning.py",
                doc: "Taxonomia Mestre V1.1 (Congelada) • Gate G3",
                reproduce: "python -m alcateia.main --context mapa_da_noite --question \"...\" --live"
            },
            5: {
                title: "Auditoria (Audit Service)",
                producer: "Selador de Linhagem (AuditService)",
                model: "Assinatura Criptográfica da MUE",
                script: "alcateia/core/audit.py",
                doc: "Relatório de Auditoria ALC-AUD-001 • Gate G4",
                reproduce: "Gera o arquivo físico 'alcateia/output/mue_latest.json' em disco."
            }
        }
    },
    saude_territorial: {
        total_comentarios: "2",
        lbl_comentarios: "Linhas de dados de UBS monitoradas",
        fontes_count: "2",
        pii_expurgado: "100%",
        latencia: "0.11s",
        badge_modelo: "GPT-5.6-Turbo",
        badge_confianca: "Confiança Crítica",
        rec_title: "Remanejar 3 equipes de Clínica Geral para a UBS Central e reforçar os insumos para asma.",
        rec_hypothesis: "Identificado congestionamento crítico no atendimento pediátrico respiratório durante as semanas de baixa temperatura na UBS Central.",
        sig_hash: "SHA-256: e8b9f65357efba30d690d5ed47b4b392b0c3b3a844d59e90fa84b1986e2e8e0c",
        sig_meta: "Assinado eletronicamente por Kacia Oliveira (Revisora Independente)",
        fontes: [
            { nome: "hospital_atendimento.xlsx", hash: "d8c1b9201fcf201a09df..." },
            { nome: "clinica_geral.xlsx", hash: "bc14d9201afc9201d0a5..." }
        ],
        evidencias: [
            {
                arquivo: "hospital_atendimento.xlsx",
                linha: 2,
                lote: "lote_saude_01",
                texto: "UBS Central sem pediatra de plantão hoje à noite... Fila de nebulização gigante e medicação em falta... [PII_EMAIL_REMOVED]"
            },
            {
                arquivo: "clinica_geral.xlsx",
                linha: 15,
                lote: "lote_saude_01",
                texto: "fila de espera para atendimento infantil de sintomas respiratórios passando de 3 horas na ubs... medicação para asma acabou [PII_PHONE_REMOVED]"
            }
        ],
        pipeline_steps: {
            1: {
                title: "Investigação (Discovery Service)",
                producer: "Discovery Agent (DiscoveryService)",
                model: "Codex Assistido",
                script: "alcateia/core/discovery.py",
                doc: "ALCATEIA-ARC-001-V1.0.md • Gate G0",
                reproduce: "python -m alcateia.main --context saude_territorial --question \"Mapear gargalos...\""
            },
            2: {
                title: "Execução (Execution Service)",
                producer: "Saneador de Dados (ExecutionService)",
                model: "Expressões Regulares",
                script: "alcateia/core/execution.py",
                doc: "Regras de Saneamento de Saúde Pública • Gate G1",
                reproduce: "Filtra dados de pacientes para estrita conformidade da LGPD na Saúde."
            },
            3: {
                title: "Evidências (Evidence Service)",
                producer: "Auditor de Origens (EvidenceService)",
                model: "Auditoria Criptográfica SHA-256",
                script: "alcateia/core/evidence.py",
                doc: "Tabela Relacional de Integridade • Gate G2",
                reproduce: "python -m unittest alcateia.tests.test_flow"
            },
            4: {
                title: "Recomendação (Reasoning Service)",
                producer: "Cognitive Agent (ReasoningService)",
                model: "GPT-5.6-Turbo (OpenAI API)",
                script: "alcateia/core/reasoning.py",
                doc: "Taxonomia de Gargalos Hospitalares • Gate G3",
                reproduce: "python -m alcateia.main --context saude_territorial --question \"...\" --live"
            },
            5: {
                title: "Auditoria (Audit Service)",
                producer: "Selador de Linhagem (AuditService)",
                model: "Assinatura Criptográfica da MUE",
                script: "alcateia/core/audit.py",
                doc: "Relatório de Auditoria ALC-AUD-001 • Gate G4",
                reproduce: "Gera o arquivo físico de MUE na pasta 'alcateia/output/'."
            }
        }
    }
};

let currentDomain = "mapa_da_noite";
let activeStep = 1;

// FUNÇÃO PARA TROCAR O DOMÍNIO (ESCALABILIDADE METODOLÓGICA)
function switchDomain(domain) {
    currentDomain = domain;
    
    // Atualiza botões
    document.getElementById("btn-caso1").classList.toggle("active", domain === "mapa_da_noite");
    document.getElementById("btn-caso2").classList.toggle("active", domain === "saude_territorial");
    
    // Aplica tema CSS no body
    document.body.classList.toggle("health-theme", domain === "saude_territorial");
    
    // Mostra painel do SoundCloud apenas no Mapa da Noite
    const soundcloudCard = document.getElementById("soundcloud-card");
    if (soundcloudCard) {
        soundcloudCard.style.display = domain === "mapa_da_noite" ? "block" : "none";
    }
    
    // Atualiza Métricas
    document.getElementById("val-total-comentarios").innerText = domainData[domain].total_comentarios;
    document.getElementById("lbl-total-comentarios").innerText = domainData[domain].lbl_comentarios;
    document.getElementById("val-fontes-auditadas").innerText = domainData[domain].fontes_count;
    document.getElementById("val-pii-expurgado").innerText = domainData[domain].pii_expurgado;
    document.getElementById("val-latencia").innerText = domainData[domain].latencia;
    
    // Atualiza Recomendação Principal
    document.getElementById("val-badge-modelo").innerText = domainData[domain].badge_modelo;
    document.getElementById("val-badge-confianca").innerText = domainData[domain].badge_confianca;
    document.getElementById("val-rec-title").innerText = domainData[domain].rec_title;
    document.getElementById("val-rec-hypothesis").innerHTML = `<strong>Hipótese Formulada:</strong> ${domainData[domain].rec_hypothesis}`;
    
    // Atualiza Selo de Assinatura
    document.getElementById("val-sig-hash").innerText = domainData[domain].sig_hash;
    document.getElementById("val-sig-meta").innerText = domainData[domain].sig_meta;
    
    // Renderiza Fontes
    renderSources(domain);
    
    // Renderiza Evidências
    renderEvidences(domain);
    
    // Atualiza detalhes do pipeline na etapa ativa
    showPipelineDetail(activeStep);
}

// RENDERIZA FONTES E HASHES (GOVERNANÇA)
function renderSources(domain) {
    const container = document.getElementById("sources-list-container");
    container.innerHTML = "";
    
    domainData[domain].fontes.forEach(f => {
        const row = document.createElement("div");
        row.className = "source-row";
        row.innerHTML = `
            <span class="source-name" title="${f.nome}">📄 ${f.nome}</span>
            <span class="source-hash">${f.hash}</span>
            <span class="text-green font-weight-bold">✓ VÁLIDO</span>
        `;
        container.appendChild(row);
    });
}

// RENDERIZA FRAGMENTOS DE EVIDÊNCIA (RASTREABILIDADE)
function renderEvidences(domain) {
    const container = document.getElementById("evidencies-list-container");
    container.innerHTML = "";
    
    domainData[domain].evidencias.forEach(e => {
        const item = document.createElement("div");
        item.className = "evidence-item";
        item.innerHTML = `
            <div class="evidence-meta">
                <span>📁 Origem: ${e.arquivo} • Linha: ${e.linha}</span>
                <span class="badge badge-green">${e.lote.toUpperCase()}</span>
            </div>
            <p class="evidence-text">"${e.texto}"</p>
        `;
        container.appendChild(item);
    });
}

// DETALHE DO TIMELINE (CONFIANÇA)
function showPipelineDetail(step) {
    activeStep = step;
    
    // Atualiza classes do timeline
    for (let i = 1; i <= 5; i++) {
        document.getElementById(`time-step${i}`).classList.toggle("active", i === step);
    }
    
    const stepData = domainData[currentDomain].pipeline_steps[step];
    
    document.getElementById("detail-title").innerText = stepData.title;
    document.getElementById("detail-producer").innerText = stepData.producer;
    document.getElementById("detail-model").innerText = stepData.model;
    document.getElementById("detail-script").innerHTML = `<code>${stepData.script}</code>`;
    document.getElementById("detail-doc").innerText = stepData.doc;
    document.getElementById("detail-reproduce").innerHTML = `<code>${stepData.reproduce}</code>`;
}

// INICIALIZAÇÃO DA PÁGINA
window.onload = function() {
    switchDomain("mapa_da_noite");
};
