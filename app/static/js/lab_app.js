/**
 * ZIZIPHUS JUJUBA: Signal Intelligence Lab Frontend Controller.
 * Manages bilingual switching (RU/EN), Vis.js interactive network,
 * Plotly charts, dynamic tables, and custom event evaluation.
 */

// Bilingual dictionary
const I18N = {
  ru: {
    station_live: "4625 кГц | УВБ-76 | СТАТУС: АКТИВЕН",
    lang_toggle: "EN / RU",
    tab_overview: "ОБЗОР / СТАТИСТИКА",
    tab_targets: "ЗИЗИФУС И ЦЕЛЕВЫЕ СИГНАЛЫ",
    tab_graph: "ИНТЕРАКТИВНЫЙ ГРАФ",
    tab_models: "МАТЕМАТИЧЕСКИЕ МОДЕЛИ",
    tab_timeline: "ИСТОРИЧЕСКИЙ ТАЙМЛАЙН",
    tab_audit: "АУДИТ И ОЧИСТКА",
    tab_messages: "АРХИВ РАДИОГРАММ",
    tab_exports: "ЭКСПОРТ ДАННЫХ",
    
    // Overview
    ov_primary_msgs: "Основных радиограмм",
    ov_raw_entries: "Всего архивных записей",
    ov_duplicates: "Дубликатов / Аномалий",
    ov_blocks: "Распознанных кодоблоков",
    ov_codewords: "Уникальных кодовых слов",
    ov_numbers: "Уникальных 8-знаков",
    ov_audit_items: "Записей журнала аудита",
    ov_events: "Исторических событий",
    
    // Targets
    target_box_title: "ОПЕРАТИВНОЕ ПОДТВЕРЖДЕНИЕ СВЯЗИ ЗИЗИФУС — ПАСКОИТ (7724 8209)",
    target_box_desc: "Анализ первичных радиожурналов подтвердил: цифровая комбинация 7724 8209 была передана 4 сентября 2014 г. со словом ПАСКОИТ (13:24) и повторно передана ровно через 28 дней 2 октября 2014 г. со словом ЗИЗИФУС (12:14). Это подтверждает гипотезу о циклическом повторе кодовых сеток.",
    
    // Graph
    graph_search_placeholder: "Поиск слова или чисел (например, ЗИЗИФУС, 7724)...",
    btn_search: "Найти",
    btn_reset: "Сброс",
    btn_target_subgraph: "Кластер ЗИЗИФУС",
    graph_legend: "Легенда: Желтый/Оранжевый = Целевые слова | Фиолетовый = 8-значные группы | Красный = Мост 77248209 | Зеленый = Позывной",
    
    // Models
    model_modes_title: "Четыре операционных режима УВБ-76 (K-Means & PCA)",
    model_perm_title: "Тест перестановок Монте-Карло (2 000 итераций)",
    btn_run_perm: "Запустить тест",
    
    // Timeline
    timeline_title: "Исторический таймлайн и исследование событий (Event-Study)",
    timeline_desc: "Сравнение плотности радиопередач в окнах +/- 7, 14, 30, 90 дней вокруг ключевых событий кризиса 2013-2014 гг. с эмпирическим базовым распределением того же года.",
    custom_event_title: "Проверка пользовательского исторического события",
    custom_event_desc: "Введите любую дату и название события для расчета эмпирического p-value и процентиля:",
    btn_calc_event: "Рассчитать",
    
    // Table columns
    col_date: "Дата",
    col_time: "Время",
    col_callsign: "Позывной",
    col_header: "Заголовок",
    col_sequence: "Радиограмма (Кодовые слова и группы)",
    col_source: "Источник",
    col_event: "Историческое событие",
    col_window: "Окно (дней)",
    col_observed: "Факт (передач)",
    col_baseline: "Базовое среднее",
    col_percentile: "Процентиль",
    col_p_upper: "Эмпирич. p-value",
    
    // Phase 2: Navigation & Sections
    tab_traffic: "ПОВЕДЕНИЕ ТРАФИКА",
    tab_structural: "СТРУКТУРНЫЕ ИЗМЕНЕНИЯ",
    tab_anomalies: "АНАЛИЗ АНОМАЛИЙ",
    tab_net_evolution: "ЭВОЛЮЦИЯ СЕТИ",
    tab_findings: "РЕЗУЛЬТАТЫ ИССЛЕДОВАНИЯ",
    
    // Traffic Behavior
    traffic_title: "Поведение радиообмена во времени (Traffic Behavior Dynamics)",
    traffic_desc: "Многомасштабный анализ интенсивности передач: суточные ритмы, межпосылочные интервалы, всплесковость и автокорреляционные циклы.",
    tb_total_clean: "Чистых радиограмм",
    tb_mean_interval: "Средний интервал (Δt)",
    tb_fano: "Фактор Фано (Fano Factor)",
    tb_daytime_pct: "Дневная доля (07-18 UTC)",
    tb_vol_chart_title: "Дневная динамика радиопередач и скользящие средние (MA-7, MA-30)",
    tb_diurnal_title: "Суточный профиль (24 часа, UTC vs MSK)",
    tb_dow_title: "Распределение по дням недели",
    tb_intervals_title: "Распределение межпосылочных интервалов (Δt, часы)",
    tb_acf_title: "Автокорреляционная функция (ACF) и операционные циклы",
    
    // Structural Changes
    struct_title: "Структурные изменения и динамика лексикона (Structural Changes)",
    struct_desc: "Эволюция длины радиограмм, смена позывных, скорость пополнения словаря (закон Хипса) и совместная встречаемость кодовых слов.",
    sc_vocab_total: "Уникальный лексикон",
    sc_singletons: "Одиночных слов (Hapax)",
    sc_single_block: "Одноблочных радиограмм",
    sc_heaps_beta: "Показатель Хипса (β)",
    sc_heaps_chart_title: "Кривая накопления словаря и закон Хипса",
    sc_turnover_chart_title: "Пополнение словаря по годам (Новые vs Повторные слова)",
    sc_callsigns_chart_title: "Хронологическая смена позывных (УЗБ → МДЖБ → ЖУОЗ → АНВФ → НЖТИ)",
    sc_blocks_chart_title: "Распределение радиограмм по числу кодоблоков по годам",
    sc_cooccur_title: "Совместное появление слов в многоблочных передачах (Co-occurrence)",
    sc_cooccur_desc: "Пары кодовых слов, переданные в одной составной радиограмме в ходе комплексных учений или циркулярных приказов:",
    sc_col_word1: "Слово 1",
    sc_col_word2: "Слово 2",
    sc_col_cooccur_cnt: "Совместных передач",
    
    // Anomaly Explorer
    anom_title: "Исследование статистических аномалий (Anomaly Explorer)",
    anom_desc: "Выявление аномальных всплесков активности через медианное абсолютное отклонение (MAD), пуассоновские вероятности и форензик-аудит февраля 2022 года.",
    anom_table_title: "Статистически аномальные дни радиообмена",
    anom_col_count: "Передач за день",
    anom_col_z: "Modified Z-Score (MAD)",
    anom_col_poisson: "Пуассон p-value",
    anom_col_words: "Кодовые слова дня",
    anom_feb2022_title: "ФОРЕНЗИК-АУДИТ ФЕВРАЛЯ 2022 ГОДА",
    anom_gaps_title: "АУДИТ АРХИВНЫХ ЛАКУН И ПРОПУСКОВ (> 14 ДНЕЙ)",
    
    // Network Evolution
    net_title: "Развитие сети связей во времени (Network Evolution)",
    net_desc: "Топологические срезы графа кодовых слов и цифровых групп по четырём хронологическим эпохам УВБ-76.",
    net_nodes: "Узлов в эпохе |V|",
    net_edges: "Связей |E|",
    net_density: "Плотность (Density)",
    net_transitivity: "Кластеризация (Transitivity)",
    net_giant: "Гигантская компонента",
    net_graph_title: "Интерактивный срез графа выбранной эпохи",
    net_hubs_title: "Ключевые хабы эпохи (Наибольшая степень связности)",
    net_col_node: "Узел (Слово или Число)",
    net_col_type: "Тип сущности",
    net_col_degree: "Степень узла (Degree)",
    
    // Research Findings
    rf_title: "Подтверждённые результаты, опровергнутые гипотезы и ограничения",
    rf_desc: "Итоговый научный реестр доказательной базы исследования радиообмена УВБ-76 (ZIZIPHUS JUJUBA).",
    rf_download_report: "Скачать COMPREHENSIVE_RESEARCH_REPORT.md",
    rf_confirmed_head: "ПОДТВЕРЖДЁННЫЕ ЭМПИРИЧЕСКИЕ ФАКТЫ",
    rf_refuted_head: "ОПРОВЕРГНУТЫЕ И НЕ ПОДТВЕРЖДЁННЫЕ ГИПОТЕЗЫ",
    rf_limitations_head: "МЕТОДОЛОГИЧЕСКИЕ ОГРАНИЧЕНИЯ ИССЛЕДОВАНИЯ"
  },
  en: {
    station_live: "4625 kHz | UVB-76 | STATUS: ACTIVE",
    lang_toggle: "RU / EN",
    tab_overview: "OVERVIEW / METRICS",
    tab_traffic: "TRAFFIC BEHAVIOR",
    tab_structural: "STRUCTURAL CHANGES",
    tab_anomalies: "ANOMALY EXPLORER",
    tab_net_evolution: "NETWORK EVOLUTION",
    tab_findings: "RESEARCH FINDINGS",
    tab_targets: "ZIZIPHUS & TARGET SIGNALS",
    tab_graph: "NETWORK GRAPH",
    tab_models: "MATHEMATICAL MODELS",
    tab_timeline: "HISTORICAL TIMELINE",
    tab_audit: "AUDIT & DEDUPLICATION",
    tab_messages: "RADIOGRAM ARCHIVE",
    tab_exports: "EXPORTS",
    
    ov_primary_msgs: "Primary Radiograms",
    ov_raw_entries: "Total Raw Log Entries",
    ov_duplicates: "Duplicates / Anomalies",
    ov_blocks: "Parsed Code Blocks",
    ov_codewords: "Unique Codewords",
    ov_numbers: "Unique 8-Digit Numbers",
    ov_audit_items: "Audit Log Entries",
    ov_events: "Historical Events",
    
    target_box_title: "CONFIRMED SIGNAL INTELLIGENCE: ZIZIPHUS — PASKOIT (7724 8209)",
    target_box_desc: "Primary archive verification confirms: 8-digit sequence 7724 8209 was transmitted on Sep 04, 2014 with PASKOIT (13:24) and retransmitted exactly 28 days later on Oct 02, 2014 with ZIZIPHUS (12:14). This demonstrates cyclic codebook re-use in primary military logs.",
    
    graph_search_placeholder: "Search codeword or digits (e.g. ZIZIFUS, 7724)...",
    btn_search: "Search",
    btn_reset: "Reset",
    btn_target_subgraph: "ZIZIPHUS Cluster",
    graph_legend: "Legend: Amber/Cyan = Codewords | Purple = 8-Digit Numbers | Red = Bridge 77248209 | Green = Callsign",
    
    model_modes_title: "Four Operational Modes of UVB-76 (K-Means & PCA)",
    model_perm_title: "Monte Carlo Permutation Test (2,000 trials)",
    btn_run_perm: "Run Test",
    
    timeline_title: "Historical Timeline & Event-Study Module",
    timeline_desc: "Comparison of broadcast volume in +/- 7, 14, 30, 90 day windows around key 2013-2014 events against empirical same-year calendar baselines.",
    custom_event_title: "Evaluate Custom Historical Event",
    custom_event_desc: "Enter any historical date and event name to compute empirical p-value and percentile:",
    btn_calc_event: "Calculate",
    
    col_date: "Date",
    col_time: "Time",
    col_callsign: "Callsign",
    col_header: "Header",
    col_sequence: "Radiogram (Words & Digits)",
    col_source: "Source",
    col_event: "Historical Event",
    col_window: "Window (Days)",
    col_observed: "Observed",
    col_baseline: "Baseline Mean",
    col_percentile: "Percentile",
    col_p_upper: "Empirical p-value",
    
    // Phase 2: Navigation & Sections
    traffic_title: "Radio Traffic Behavior Dynamics",
    traffic_desc: "Multi-scale transmission dynamics: diurnal cycles, inter-arrival intervals, burstiness, and autocorrelation periodicity.",
    tb_total_clean: "Clean Radiograms",
    tb_mean_interval: "Mean Interval (Δt)",
    tb_fano: "Fano Factor",
    tb_daytime_pct: "Daytime Share (07-18 UTC)",
    tb_vol_chart_title: "Daily Radiogram Volume & Moving Averages (MA-7, MA-30)",
    tb_diurnal_title: "24-Hour Diurnal Profile (UTC vs MSK)",
    tb_dow_title: "Day-of-Week Distribution",
    tb_intervals_title: "Inter-Arrival Interval Distribution (Δt, Hours)",
    tb_acf_title: "Autocorrelation Function (ACF) & Operational Cycles",
    
    // Structural Changes
    struct_title: "Structural Dynamics & Lexical Evolution",
    struct_desc: "Evolution of radiogram length, callsign shifts, vocabulary discovery rates (Heaps' Law), and word co-occurrences.",
    sc_vocab_total: "Unique Vocabulary",
    sc_singletons: "Singletons (Hapax)",
    sc_single_block: "Single-Block Radiograms",
    sc_heaps_beta: "Heaps' Law Parameter (β)",
    sc_heaps_chart_title: "Cumulative Vocabulary Discovery & Heaps' Law Fit",
    sc_turnover_chart_title: "Annual Vocabulary Turnover (New vs Reused Words)",
    sc_callsigns_chart_title: "Callsign Succession (UZB → MDZhB → ZhUOZ → ANVF → NZhTI)",
    sc_blocks_chart_title: "Radiogram Code Block Length Distribution by Year",
    sc_cooccur_title: "Word Co-Occurrence in Multi-Block Radiograms",
    sc_cooccur_desc: "Pairs of codewords transmitted together within the same composite broadcast during command exercises:",
    sc_col_word1: "Codeword 1",
    sc_col_word2: "Codeword 2",
    sc_col_cooccur_cnt: "Co-Occurrences",
    
    // Anomaly Explorer
    anom_title: "Statistical Anomaly Explorer",
    anom_desc: "Detection of anomalous activity spikes via Median Absolute Deviation (MAD), Poisson probabilities, and Feb 2022 forensic audit.",
    anom_table_title: "Statistically Anomalous Transmission Days",
    anom_col_count: "Daily Broadcasts",
    anom_col_z: "Modified Z-Score (MAD)",
    anom_col_poisson: "Poisson p-value",
    anom_col_words: "Day's Codewords",
    anom_feb2022_title: "FEBRUARY 2022 FORENSIC AUDIT",
    anom_gaps_title: "ARCHIVAL COVERAGE & HIATUS AUDIT (> 14 DAYS)",
    
    // Network Evolution
    net_title: "Network Topological Evolution Across Epochs",
    net_desc: "Topological graph slices connecting codewords and 8-digit combinations across four chronological eras.",
    net_nodes: "Nodes in Epoch |V|",
    net_edges: "Edges |E|",
    net_density: "Density",
    net_transitivity: "Transitivity (Clustering)",
    net_giant: "Giant Component Share",
    net_graph_title: "Interactive Network Slice for Selected Epoch",
    net_hubs_title: "Epoch Hub Nodes (Highest Degree Centrality)",
    net_col_node: "Node (Word or Number)",
    net_col_type: "Entity Type",
    net_col_degree: "Node Degree",
    
    // Research Findings
    rf_title: "Empirical Findings, Refuted Hypotheses & Study Limitations",
    rf_desc: "Comprehensive evidentiary registry for UVB-76 signal intelligence research (ZIZIPHUS JUJUBA).",
    rf_download_report: "Download COMPREHENSIVE_RESEARCH_REPORT.md",
    rf_confirmed_head: "CONFIRMED EMPIRICAL FACTS",
    rf_refuted_head: "REFUTED & UNCONFIRMED HYPOTHESES",
    rf_limitations_head: "METHODOLOGICAL LIMITATIONS"
  }
};

let currentLang = 'ru';
let networkInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupLanguageToggle();
  loadOverview();
  loadTrafficBehavior();
  loadStructuralChanges();
  loadAnomalyExplorer();
  loadNetworkEvolution();
  loadResearchFindings();
  loadTargetCluster();
  initNetworkGraph();
  loadModels();
  loadTimeline();
  loadAuditLogs();
  loadMessagesTable();
});

function t(key) {
  return I18N[currentLang][key] || key;
}

function updateTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (I18N[currentLang][key]) {
      el.textContent = I18N[currentLang][key];
    }
  });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    const key = el.getAttribute("data-i18n-ph");
    if (I18N[currentLang][key]) {
      el.setAttribute("placeholder", I18N[currentLang][key]);
    }
  });
}

function setupLanguageToggle() {
  const btn = document.getElementById("lang-btn");
  btn.addEventListener("click", () => {
    currentLang = currentLang === 'ru' ? 'en' : 'ru';
    btn.textContent = I18N[currentLang].lang_toggle;
    updateTranslations();
  });
}

function setupTabs() {
  document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      const pane = document.getElementById(targetId);
      if (pane) pane.classList.add("active");
      
      if (targetId === "tab-graph" && networkInstance) {
        networkInstance.fit();
      }
      if (targetId === "tab-traffic") loadTrafficBehavior();
      if (targetId === "tab-structural") loadStructuralChanges();
      if (targetId === "tab-anomalies") loadAnomalyExplorer();
      if (targetId === "tab-net-evolution") {
        if (epochNetworkInstance) epochNetworkInstance.fit();
        else loadNetworkEvolution('epoch_2');
      }
      if (targetId === "tab-findings") loadResearchFindings();
    });
  });
}

// 1. Overview
async function loadOverview() {
  try {
    const res = await fetch("/api/overview");
    const data = await res.json();
    const m = data.metrics;
    
    document.getElementById("stat-primary-msgs").textContent = m.primary_messages.toLocaleString();
    document.getElementById("stat-raw-entries").textContent = m.total_raw_archive_entries.toLocaleString();
    document.getElementById("stat-duplicates").textContent = m.flagged_duplicates.toLocaleString();
    document.getElementById("stat-blocks").textContent = m.parsed_code_blocks.toLocaleString();
    document.getElementById("stat-codewords").textContent = m.unique_codewords.toLocaleString();
    document.getElementById("stat-numbers").textContent = m.unique_8digit_combinations.toLocaleString();
    document.getElementById("stat-audit").textContent = m.audit_log_items.toLocaleString();
    document.getElementById("stat-events").textContent = m.historical_events_registered.toLocaleString();
    
    // Render yearly bar chart using Plotly
    const years = Object.keys(data.years_distribution);
    const counts = Object.values(data.years_distribution);
    
    const plotData = [{
      x: years,
      y: counts,
      type: 'bar',
      marker: {
        color: '#38bdf8',
        line: { color: '#0284c7', width: 1.5 }
      }
    }];
    
    const layout = {
      title: { text: currentLang === 'ru' ? 'Распределение радиограмм по годам' : 'Radiograms by Year', font: { color: '#f8fafc', size: 14 } },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { color: '#94a3b8' },
      xaxis: { title: currentLang === 'ru' ? 'Год' : 'Year', gridcolor: '#1e293b' },
      yaxis: { title: currentLang === 'ru' ? 'Количество радиограмм' : 'Message Count', gridcolor: '#1e293b' },
      margin: { t: 40, b: 40, l: 50, r: 20 }
    };
    
    Plotly.newPlot('overview-chart', plotData, layout, { responsive: true, displayModeBar: false });
  } catch (err) {
    console.error("Overview load failed", err);
  }
}

// 2. Targets Cluster
async function loadTargetCluster() {
  try {
    const res = await fetch("/api/targets/ziziphus_cluster");
    const data = await res.json();
    
    const tbody = document.getElementById("target-records-body");
    tbody.innerHTML = "";
    data.target_records.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell">${r.date}</td>
        <td class="mono-cell">${r.time_as_logged || '—'}</td>
        <td class="mono-cell"><span class="badge badge-amber">${r.code_word}</span></td>
        <td class="mono-cell"><strong>${r.digit_group_1} ${r.digit_group_2}</strong></td>
        <td class="mono-cell">${r.header_number || '—'}</td>
        <td class="mono-cell"><small>${r.source_file}:${r.source_line}</small></td>
      `;
      tbody.appendChild(tr);
    });
    
    // 77248209 confirmation table
    const linkBody = document.getElementById("target-7724-body");
    linkBody.innerHTML = "";
    data.link_77248209.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell"><strong>${r.date}</strong></td>
        <td class="mono-cell">${r.time_as_logged}</td>
        <td class="mono-cell"><span class="badge ${r.code_word === 'ЗИЗИФУС' ? 'badge-cyan' : 'badge-amber'}">${r.code_word}</span></td>
        <td class="mono-cell"><span class="badge badge-rose">7724 8209</span></td>
        <td class="mono-cell">${r.full_word_sequence}</td>
        <td class="mono-cell"><small>${r.source_file}:${r.source_line}</small></td>
      `;
      linkBody.appendChild(tr);
    });
    
    // Triplet echo table
    const tripBody = document.getElementById("triplet-echo-body");
    tripBody.innerHTML = "";
    data.triplet_echo.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell">${r.date}</td>
        <td class="mono-cell">${r.time_as_logged || '—'}</td>
        <td class="mono-cell"><strong>${r.code_word}</strong></td>
        <td class="mono-cell"><span class="badge badge-cyan">${r.digit_combination}</span></td>
        <td class="mono-cell">${r.header_number || '—'}</td>
        <td class="mono-cell"><small>${r.source_file}:${r.source_line}</small></td>
      `;
      tripBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Target cluster load failed", err);
  }
}

// 3. Network Graph
function bindNetworkEvents(network, nodes, edges) {
  let isHighlighted = false;

  function restoreHighlight() {
    if (!isHighlighted) return;
    const nUpdates = [];
    nodes.forEach(n => {
      nUpdates.push({
        id: n.id,
        opacity: 1.0,
        font: { color: '#f8fafc', size: 11, strokeWidth: 2, strokeColor: '#070b12' }
      });
    });
    nodes.update(nUpdates);

    const eUpdates = [];
    edges.forEach(e => {
      eUpdates.push({
        id: e.id,
        opacity: 1.0,
        width: 1.5
      });
    });
    edges.update(eUpdates);
    isHighlighted = false;
  }

  network.on("selectNode", function (params) {
    const selectedNodeId = params.nodes[0];
    if (!selectedNodeId) return;

    const connectedNodes = network.getConnectedNodes(selectedNodeId);
    const connectedEdges = network.getConnectedEdges(selectedNodeId);
    const activeNodeIds = new Set([selectedNodeId, ...connectedNodes]);
    const activeEdgeIds = new Set(connectedEdges);

    const nUpdates = [];
    nodes.forEach(n => {
      if (activeNodeIds.has(n.id)) {
        nUpdates.push({
          id: n.id,
          opacity: 1.0,
          font: {
            color: '#ffffff',
            size: n.id === selectedNodeId ? 12 : 11,
            strokeWidth: 2,
            strokeColor: '#000000'
          }
        });
      } else {
        nUpdates.push({
          id: n.id,
          opacity: 0.15,
          font: { color: '#334155', size: 10, strokeWidth: 0 }
        });
      }
    });
    nodes.update(nUpdates);

    const eUpdates = [];
    edges.forEach(e => {
      if (activeEdgeIds.has(e.id)) {
        eUpdates.push({
          id: e.id,
          opacity: 1.0,
          width: 2.5
        });
      } else {
        eUpdates.push({
          id: e.id,
          opacity: 0.08,
          width: 1
        });
      }
    });
    edges.update(eUpdates);
    isHighlighted = true;

    const nodeObj = nodes.get(selectedNodeId);
    const neighborNames = connectedNodes.map(nid => {
      const obj = nodes.get(nid);
      return obj ? obj.label : nid;
    });

    const groupNames = {
      'CODE_WORD': 'Кодовое слово',
      'NUMBER_GROUP': 'Цифровая группа',
      'CALLSIGN': 'Позывной',
      'RADIOGRAM': 'Радиограмма'
    };
    const gName = groupNames[nodeObj.group] || nodeObj.group || 'Узел';

    const infoEl = document.getElementById("selected-node-info");
    if (infoEl) {
      infoEl.innerHTML = `
        <span style="color:var(--color-amber); font-weight:bold;">[${gName}]</span>
        <span style="color:#ffffff; font-weight:bold; margin-left:4px;">${nodeObj.label}</span>
        <span style="color:var(--text-muted); margin-left:8px;">| Связей: <strong>${connectedNodes.length}</strong></span>
        <span style="color:var(--text-secondary); margin-left:8px;">| Соседи: <span style="color:var(--color-cyan);">${neighborNames.slice(0, 5).join(', ')}${neighborNames.length > 5 ? ' ... (+' + (neighborNames.length - 5) + ')' : ''}</span></span>
      `;
    }
  });

  network.on("selectEdge", function (params) {
    if (params.nodes.length === 0 && params.edges.length > 0) {
      const selectedEdgeId = params.edges[0];
      const edgeObj = edges.get(selectedEdgeId);
      if (edgeObj) {
        const fromNode = nodes.get(edgeObj.from);
        const toNode = nodes.get(edgeObj.to);
        const fromLabel = fromNode ? fromNode.label : edgeObj.from;
        const toLabel = toNode ? toNode.label : edgeObj.to;
        const rel = edgeObj.title || edgeObj.relation || "Связь";

        const infoEl = document.getElementById("selected-node-info");
        if (infoEl) {
          infoEl.innerHTML = `
            <span style="color:var(--color-cyan); font-weight:bold;">[Связь]</span>
            <span style="color:#ffffff; font-weight:bold; margin-left:4px;">${fromLabel}</span>
            <span style="color:var(--text-muted);"> ⟷ </span>
            <span style="color:#ffffff; font-weight:bold;">${toLabel}</span>
            <span style="color:var(--color-emerald); margin-left:8px;">| ${rel}</span>
            <span style="color:var(--text-muted); margin-left:8px;">| Вес: ${edgeObj.weight || 1}</span>
          `;
        }
      }
    }
  });

  network.on("deselectNode", function () {
    restoreHighlight();
    const infoEl = document.getElementById("selected-node-info");
    if (infoEl) {
      infoEl.innerHTML = `Кликните на узел или связь для инспекции свойств`;
    }
  });

  network.on("deselectEdge", function () {
    if (network.getSelectedNodes().length === 0) {
      restoreHighlight();
      const infoEl = document.getElementById("selected-node-info");
      if (infoEl) {
        infoEl.innerHTML = `Кликните на узел или связь для инспекции свойств`;
      }
    }
  });
}

async function initNetworkGraph() {
  const container = document.getElementById("network-container");
  try {
    const res = await fetch("/api/graph/subgraph?targets=ЗИЗИФУС,ПАСКОИТ,ГАШЕНИЕ,НИЗКИЙ&depth=2");
    const graphData = await res.json();
    
    // Ensure nodes have compact 11px font
    (graphData.nodes || []).forEach(n => {
      n.font = {
        color: '#f8fafc',
        face: 'JetBrains Mono, monospace',
        size: 11,
        strokeWidth: 2,
        strokeColor: '#070b12'
      };
    });

    // Remove permanent edge labels and ensure hover tooltips
    (graphData.edges || []).forEach(e => {
      delete e.label;
      e.font = { size: 0 };
      if (!e.title) {
        const rel = e.relation || 'LINK';
        if (rel === 'WORD_TO_DIGITS') {
          e.title = 'Связь: Кодовое слово ↔ Числовая группа (WORD_TO_DIGITS)';
        } else if (rel === 'CO_OCCURRENCE') {
          e.title = 'Связь: Совместная передача в сообщении (CO_OCCURRENCE)';
        } else {
          e.title = `Связь: ${rel}`;
        }
      }
    });

    const nodes = new vis.DataSet(graphData.nodes);
    const edges = new vis.DataSet(graphData.edges);
    
    const data = { nodes, edges };
    const options = {
      nodes: {
        shape: 'dot',
        borderWidth: 1.5,
        font: {
          color: '#f8fafc',
          face: 'JetBrains Mono, monospace',
          size: 11,
          strokeWidth: 2,
          strokeColor: '#070b12'
        },
        scaling: { label: { enabled: false } }
      },
      edges: {
        width: 1.5,
        hoverWidth: 2.5,
        selectionWidth: 3,
        smooth: {
          type: 'continuous',
          roundness: 0.15
        },
        font: { size: 0 }
      },
      physics: {
        solver: 'barnesHut',
        barnesHut: {
          gravitationalConstant: -6500,
          centralGravity: 0.22,
          springLength: 175,
          springConstant: 0.035,
          damping: 0.09,
          avoidOverlap: 0.85
        },
        stabilization: {
          iterations: 180,
          updateInterval: 25
        }
      },
      interaction: {
        hover: true,
        hoverConnectedEdges: true,
        tooltipDelay: 80,
        zoomView: true,
        dragView: true,
        dragNodes: true,
        navigationButtons: true,
        keyboard: {
          enabled: true,
          bindToWindow: false
        }
      }
    };
    
    if (networkInstance) {
      networkInstance.destroy();
    }
    networkInstance = new vis.Network(container, data, options);
    bindNetworkEvents(networkInstance, nodes, edges);
    
  } catch (err) {
    console.error("Network init failed", err);
  }
}

async function searchGraphNode() {
  const q = document.getElementById("graph-search-input").value.trim();
  if (!q) return;
  try {
    const res = await fetch(`/api/graph/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    if (data.found && networkInstance) {
      (data.nodes || []).forEach(n => {
        n.font = {
          color: '#f8fafc',
          face: 'JetBrains Mono, monospace',
          size: 11,
          strokeWidth: 2,
          strokeColor: '#070b12'
        };
      });
      (data.edges || []).forEach(e => {
        delete e.label;
        e.font = { size: 0 };
        if (!e.title) {
          e.title = e.relation ? `Связь: ${e.relation}` : 'Связь';
        }
      });
      const nodes = new vis.DataSet(data.nodes);
      const edges = new vis.DataSet(data.edges);
      networkInstance.setData({ nodes, edges });
      bindNetworkEvents(networkInstance, nodes, edges);
      networkInstance.fit();
      document.getElementById("selected-node-info").textContent = `Найдено узлов: ${data.matched_count}`;
    } else {
      alert("Узел не найден в графе");
    }
  } catch (err) {
    console.error("Search failed", err);
  }
}

function resetGraph() {
  initNetworkGraph();
}

// 4. Mathematical Models
async function loadModels() {
  try {
    // K-Means Clustering & PCA
    const clRes = await fetch("/api/clustering/modes?k=4");
    const clData = await clRes.json();
    
    document.getElementById("silhouette-score").textContent = clData.silhouette_score;
    
    // PCA Scatter
    const pcaPoints = clData.clustered_years;
    const colors = ['#38bdf8', '#f59e0b', '#10b981', '#f43f5e'];
    
    const scatterData = [{
      x: pcaPoints.map(p => p.pca_x),
      y: pcaPoints.map(p => p.pca_y),
      text: pcaPoints.map(p => `${p.year} (Кластер ${p.cluster_id + 1})`),
      mode: 'markers+text',
      textposition: 'top center',
      marker: {
        size: 14,
        color: pcaPoints.map(p => colors[p.cluster_id % colors.length]),
        line: { color: '#ffffff', width: 1 }
      }
    }];
    
    const pcaLayout = {
      title: { text: currentLang === 'ru' ? '2D PCA проекция кластеров активности' : '2D PCA Clusters of Activity', font: { color: '#f8fafc', size: 14 } },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { color: '#94a3b8' },
      xaxis: { title: 'PCA Component 1', gridcolor: '#1e293b' },
      yaxis: { title: 'PCA Component 2', gridcolor: '#1e293b' },
      margin: { t: 40, b: 40, l: 40, r: 20 }
    };
    Plotly.newPlot('pca-chart', scatterData, pcaLayout, { responsive: true, displayModeBar: false });
    
    // Diurnal chart
    const diurnRes = await fetch("/api/temporal/diurnal");
    const diurnData = await diurnRes.json();
    
    const diurnPlot = [{
      x: diurnData.hourly_distribution.map(d => d.hour_label),
      y: diurnData.hourly_distribution.map(d => d.count),
      type: 'bar',
      marker: { color: '#a855f7' }
    }];
    const diurnLayout = {
      title: { text: currentLang === 'ru' ? 'Суточное распределение радиообмена (часы UTC)' : 'Diurnal Distribution (UTC Hours)', font: { color: '#f8fafc', size: 14 } },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: { color: '#94a3b8' },
      xaxis: { title: currentLang === 'ru' ? 'Час (UTC)' : 'Hour (UTC)', gridcolor: '#1e293b' },
      yaxis: { title: currentLang === 'ru' ? 'Передач' : 'Broadcasts', gridcolor: '#1e293b' },
      margin: { t: 40, b: 40, l: 50, r: 20 }
    };
    Plotly.newPlot('diurnal-chart', diurnPlot, diurnLayout, { responsive: true, displayModeBar: false });
    
    // Word Frequency Table
    const wfRes = await fetch("/api/frequency/words?top_n=15");
    const wfData = await wfRes.json();
    const wfBody = document.getElementById("word-freq-body");
    wfBody.innerHTML = "";
    wfData.top_words.forEach((w, idx) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell">${idx + 1}</td>
        <td class="mono-cell"><strong>${w.code_word}</strong></td>
        <td class="mono-cell">${w.frequency}</td>
        <td class="mono-cell">${w.distinct_dates}</td>
        <td class="mono-cell"><small>${w.first_seen} .. ${w.last_seen}</small></td>
      `;
      wfBody.appendChild(tr);
    });
    
    // Callsigns Table
    const csRes = await fetch("/api/frequency/callsigns");
    const csData = await csRes.json();
    const csBody = document.getElementById("callsign-freq-body");
    csBody.innerHTML = "";
    csData.callsigns.forEach(c => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell"><strong>${c.normalized_callsign}</strong></td>
        <td class="mono-cell">${c.count}</td>
        <td class="mono-cell">${c.percentage}%</td>
        <td class="mono-cell"><small>${c.min_year} - ${c.max_year}</small></td>
      `;
      csBody.appendChild(tr);
    });
    
    // Repeated numbers table
    const repRes = await fetch("/api/repetition/repeated_numbers?min_occ=2");
    const repData = await repRes.json();
    const repBody = document.getElementById("repeated-numbers-body");
    repBody.innerHTML = "";
    repData.cross_word_links.slice(0, 15).forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell"><strong>${r.digits}</strong></td>
        <td class="mono-cell"><span class="badge badge-amber">${r.distinct_words}</span></td>
        <td class="mono-cell">${r.occurrences}</td>
        <td class="mono-cell">${r.words}</td>
        <td class="mono-cell">${r.mean_interval_days} дн.</td>
        <td class="mono-cell"><small>${r.dates}</small></td>
      `;
      repBody.appendChild(tr);
    });
    
  } catch (err) {
    console.error("Models load failed", err);
  }
}

async function runPermutationTest() {
  const resultBox = document.getElementById("permutation-results");
  resultBox.innerHTML = "<p>Выполняется симуляция 2 000 перестановок Монте-Карло...</p>";
  try {
    const res = await fetch("/api/hypothesis/permutation?window=7&n_trials=2000");
    const d = await res.json();
    resultBox.innerHTML = `
      <div class="intel-box ${d.empirical_p_value < 0.05 ? 'amber' : 'cyan'}">
        <h4>${d.summary_text}</h4>
        <p>Наблюдаемое число радиограмм в окнах +/- 7 дней: <strong>${d.observed_transmissions_in_windows}</strong></p>
        <p>Математическое ожидание при случайном нулевом распределении: <strong>${d.expected_transmissions_under_H0}</strong> (станд. откл. ${d.perm_std})</p>
        <p>Эмпирический p-value: <strong>${d.empirical_p_value}</strong> (Z-score: <strong>${d.z_score}</strong>)</p>
        <p>Отвержение нулевой гипотезы на уровне α = 0.05: <strong>${d.reject_null_at_005 ? 'ДА (Статистически значимо)' : 'НЕТ'}</strong></p>
      </div>
    `;
  } catch (err) {
    resultBox.innerHTML = "<p style='color:red;'>Ошибка выполнения теста</p>";
  }
}

// 5. Timeline & Event Study
async function loadTimeline() {
  try {
    const res = await fetch("/api/events/study");
    const data = await res.json();
    const tbody = document.getElementById("timeline-table-body");
    tbody.innerHTML = "";
    data.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell"><strong>${r.date}</strong></td>
        <td><strong>${currentLang === 'ru' ? r.event_name : r.event_name_en}</strong><br><small class="text-muted">${r.category} (${r.region})</small></td>
        <td class="mono-cell">${r.window_days}</td>
        <td class="mono-cell"><strong>${r.pre_observed}</strong></td>
        <td class="mono-cell">${r.pre_baseline_mean}</td>
        <td class="mono-cell">${r.pre_percentile}%</td>
        <td class="mono-cell"><span class="badge ${r.pre_p_upper < 0.1 ? 'badge-amber' : 'badge-cyan'}">${r.pre_p_upper}</span></td>
        <td class="mono-cell">${r.post_observed}</td>
        <td class="mono-cell"><span class="badge ${r.post_p_upper < 0.1 ? 'badge-amber' : 'badge-cyan'}">${r.post_p_upper}</span></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Timeline load failed", err);
  }
}

async function evaluateCustomEvent() {
  const d = document.getElementById("custom-event-date").value;
  const name = document.getElementById("custom-event-name").value || "Пользовательское событие";
  if (!d) {
    alert("Выберите дату события");
    return;
  }
  try {
    const res = await fetch(`/api/events/custom?date=${encodeURIComponent(d)}&name=${encodeURIComponent(name)}`);
    const data = await res.json();
    const box = document.getElementById("custom-event-result");
    let html = `<h4>Результаты для: ${name} (${d})</h4><table><thead><tr><th>Окно (дней)</th><th>До события (факт)</th><th>Базовое среднее</th><th>Процентиль</th><th>p-value (верхн.)</th><th>После события (факт)</th><th>p-value (после)</th></tr></thead><tbody>`;
    data.forEach(r => {
      html += `<tr><td>${r.window_days}</td><td><strong>${r.pre_observed}</strong></td><td>${r.pre_baseline_mean}</td><td>${r.pre_percentile}%</td><td>${r.pre_p_upper}</td><td><strong>${r.post_observed}</strong></td><td>${r.post_p_upper}</td></tr>`;
    });
    html += "</tbody></table>";
    box.innerHTML = html;
  } catch (err) {
    console.error("Custom event eval failed", err);
  }
}

// 6. Audit & Deduplication
async function loadAuditLogs() {
  try {
    const res = await fetch("/api/audit/logs?limit=100");
    const data = await res.json();
    const tbody = document.getElementById("audit-table-body");
    tbody.innerHTML = "";
    data.forEach(a => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell">${a.date || '—'} ${a.time || ''}</td>
        <td class="mono-cell"><span class="badge badge-amber">${a.audit_type}</span></td>
        <td class="mono-cell"><span class="badge badge-rose">${a.action_taken}</span></td>
        <td>${a.rationale}</td>
        <td class="mono-cell"><small>${a.raw_snippet}</small></td>
        <td class="mono-cell"><small>${a.source_file}:${a.source_line}</small></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Audit load failed", err);
  }
}

// 7. Messages Explorer
let currentMsgPage = 1;
async function loadMessagesTable(page = 1) {
  currentMsgPage = page;
  const year = document.getElementById("msg-filter-year").value;
  const word = document.getElementById("msg-filter-word").value.trim();
  
  let url = `/api/messages/browse?page=${page}&page_size=20`;
  if (year) url += `&year=${year}`;
  if (word) url += `&word=${encodeURIComponent(word)}`;
  
  try {
    const res = await fetch(url);
    const data = await res.json();
    
    document.getElementById("msg-total-count").textContent = `Всего: ${data.total}`;
    document.getElementById("msg-page-indicator").textContent = `${data.page} / ${data.total_pages || 1}`;
    
    const tbody = document.getElementById("messages-table-body");
    tbody.innerHTML = "";
    data.items.forEach(m => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="mono-cell"><strong>${m.date}</strong></td>
        <td class="mono-cell">${m.time_as_logged || '—'}</td>
        <td class="mono-cell"><span class="badge badge-cyan">${m.callsign || '—'}</span></td>
        <td class="mono-cell">${m.header_number || '—'}</td>
        <td class="mono-cell"><strong>${m.full_word_sequence}</strong></td>
        <td class="mono-cell"><span class="badge badge-emerald">${m.quality_flag}</span></td>
        <td class="mono-cell"><small>${m.source_file}:${m.source_line}</small></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Messages load failed", err);
  }
}

function prevMsgPage() {
  if (currentMsgPage > 1) loadMessagesTable(currentMsgPage - 1);
}

function nextMsgPage() {
  loadMessagesTable(currentMsgPage + 1);
}


// ==========================================
// PHASE 2: COMPREHENSIVE ANALYTICAL MODULES
// ==========================================

let epochNetworkInstance = null;

// 1. TRAFFIC BEHAVIOR DYNAMICS
async function loadTrafficBehavior() {
  try {
    const [volRes, diuRes, intRes, cycRes] = await Promise.all([
      fetch("/api/traffic/volume"),
      fetch("/api/traffic/diurnal"),
      fetch("/api/traffic/inter_arrival"),
      fetch("/api/traffic/cycles")
    ]);
    
    const volData = await volRes.json();
    const diuData = await diuRes.json();
    const intData = await intRes.json();
    const cycData = await cycRes.json();

    // Cards
    document.getElementById("tb-total-msgs").textContent = (volData.total_clean_messages || 0).toLocaleString();
    document.getElementById("tb-mean-interval").textContent = `${intData.mean_interval_hours || 0} ч`;
    document.getElementById("tb-fano").textContent = `${intData.fano_factor || 0} (Fano)`;
    document.getElementById("tb-daytime-pct").textContent = `${diuData.daytime_pct_utc || 0}%`;

    // Volume timeline chart (Daily + MA7 + MA30)
    const dates = volData.daily_counts.map(d => d.date);
    const counts = volData.daily_counts.map(d => d.count);
    const ma7 = volData.daily_counts.map(d => d.ma7);
    const ma30 = volData.daily_counts.map(d => d.ma30);

    Plotly.newPlot("chart-traffic-volume", [
      {
        x: dates, y: counts, type: 'bar', name: 'Радиограмм / день',
        marker: { color: 'rgba(56, 189, 248, 0.45)' }
      },
      {
        x: dates, y: ma7, type: 'scatter', mode: 'lines', name: '7-дневная скользящая (MA-7)',
        line: { color: '#f59e0b', width: 2 }
      },
      {
        x: dates, y: ma30, type: 'scatter', mode: 'lines', name: '30-дневная скользящая (MA-30)',
        line: { color: '#10b981', width: 2.5 }
      }
    ], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { gridcolor: '#1e293b', title: 'Передач' },
      margin: { t: 20, r: 20, l: 45, b: 40 },
      legend: { orientation: 'h', y: 1.15 }
    }, { responsive: true, displayModeBar: false });

    // Diurnal chart (UTC vs MSK)
    const utcHours = diuData.utc_distribution.map(d => d.hour);
    const utcPct = diuData.utc_distribution.map(d => d.pct);
    const mskPct = diuData.msk_distribution.map(d => d.pct);

    Plotly.newPlot("chart-traffic-diurnal", [
      {
        x: utcHours, y: utcPct, type: 'scatter', mode: 'lines+markers', name: 'UTC',
        line: { color: '#38bdf8', width: 2.5 }
      },
      {
        x: utcHours, y: mskPct, type: 'scatter', mode: 'lines+markers', name: 'MSK (UTC+3)',
        line: { color: '#f59e0b', width: 2, dash: 'dot' }
      }
    ], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { title: 'Час суток (0–23)', gridcolor: '#1e293b', dtick: 2 },
      yaxis: { title: 'Доля (%)', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 40, b: 40 },
      legend: { orientation: 'h', y: 1.15 }
    }, { responsive: true, displayModeBar: false });

    // Day of week chart
    const dowNames = volData.day_of_week.map(d => d.dow);
    const dowCounts = volData.day_of_week.map(d => d.count);
    Plotly.newPlot("chart-traffic-dow", [{
      x: dowNames, y: dowCounts, type: 'bar',
      marker: { color: '#a855f7' }
    }], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { title: 'Передач', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 40, b: 40 }
    }, { responsive: true, displayModeBar: false });

    // Inter-arrival intervals histogram
    const intLabels = intData.interval_histogram.map(d => d.interval);
    const intPcts = intData.interval_histogram.map(d => d.pct);
    Plotly.newPlot("chart-traffic-intervals", [{
      x: intLabels, y: intPcts, type: 'bar',
      marker: { color: '#10b981' }
    }], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { title: 'Доля (%)', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 40, b: 60 }
    }, { responsive: true, displayModeBar: false });

    document.getElementById("tb-intervals-conclusion").textContent = intData.scientific_conclusion || '';

    // Autocorrelation Function (ACF)
    const acfLags = cycData.acf_series.map(d => d.lag);
    const acfVals = cycData.acf_series.map(d => d.acf);
    Plotly.newPlot("chart-traffic-acf", [{
      x: acfLags, y: acfVals, type: 'scatter', mode: 'lines+markers',
      line: { color: '#f59e0b', width: 2 },
      marker: { size: 5 }
    }], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { title: 'Лаг (дней)', gridcolor: '#1e293b', dtick: 7 },
      yaxis: { title: 'Корреляция', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 40, b: 40 }
    }, { responsive: true, displayModeBar: false });

    document.getElementById("tb-acf-conclusion").textContent = cycData.methodological_note || '';

  } catch (err) {
    console.error("Traffic behavior load error:", err);
  }
}


// 2. STRUCTURAL CHANGES & LEXICAL TURNOVER
async function loadStructuralChanges() {
  try {
    const [callRes, blockRes, vocRes, cooRes] = await Promise.all([
      fetch("/api/structural/callsigns"),
      fetch("/api/structural/blocks"),
      fetch("/api/structural/vocabulary"),
      fetch("/api/structural/cooccurrence")
    ]);

    const callData = await callRes.json();
    const blockData = await blockRes.json();
    const vocData = await vocRes.json();
    const cooData = await cooRes.json();

    // Metric cards
    document.getElementById("sc-total-vocab").textContent = (vocData.total_unique_vocabulary || 0).toLocaleString();
    document.getElementById("sc-singletons").textContent = `${vocData.singleton_pct || 0}% (${vocData.singleton_count || 0})`;
    document.getElementById("sc-single-block").textContent = `${blockData.overall_metrics.single_block_pct || 0}%`;
    document.getElementById("sc-heaps-beta").textContent = `β = ${vocData.heaps_law.beta || 0}`;

    // Heaps' Law curve
    const nMsgs = vocData.growth_curve.map(d => d.n_messages);
    const uVoc = vocData.growth_curve.map(d => d.unique_vocab);
    const k = vocData.heaps_law.k;
    const beta = vocData.heaps_law.beta;
    const heapsFit = nMsgs.map(n => Math.round(k * Math.pow(n, beta)));

    Plotly.newPlot("chart-heaps-law", [
      {
        x: nMsgs, y: uVoc, type: 'scatter', mode: 'lines+markers', name: 'Фактический словарь V(N)',
        line: { color: '#38bdf8', width: 2.5 }
      },
      {
        x: nMsgs, y: heapsFit, type: 'scatter', mode: 'lines', name: `Аппроксимация Хипса (β=${beta})`,
        line: { color: '#f59e0b', width: 2, dash: 'dash' }
      }
    ], {
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { title: 'Объем выборки (радиограмм N)', gridcolor: '#1e293b' },
      yaxis: { title: 'Уникальных слов V(N)', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 45, b: 40 },
      legend: { orientation: 'h', y: 1.15 }
    }, { responsive: true, displayModeBar: false });

    // Annual vocabulary turnover (New vs Reused words)
    const turnYears = vocData.yearly_turnover.map(d => d.year);
    const newWords = vocData.yearly_turnover.map(d => d.new_words_introduced);
    const reusedWords = vocData.yearly_turnover.map(d => d.reused_from_past);

    Plotly.newPlot("chart-vocab-turnover", [
      {
        x: turnYears, y: newWords, type: 'bar', name: 'Новые слова (Впервые в эфире)',
        marker: { color: '#10b981' }
      },
      {
        x: turnYears, y: reusedWords, type: 'bar', name: 'Повторные слова из прошлых лет',
        marker: { color: '#a855f7' }
      }
    ], {
      barmode: 'stack',
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { title: 'Слов', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 45, b: 40 },
      legend: { orientation: 'h', y: 1.15 }
    }, { responsive: true, displayModeBar: false });

    // Callsign transition chart
    const csTraces = callData.callsign_distribution.map(item => ({
      x: item.years, y: item.counts, type: 'bar', name: item.callsign
    }));

    Plotly.newPlot("chart-callsigns", csTraces, {
      barmode: 'stack',
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { title: 'Передач', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 45, b: 40 },
      legend: { orientation: 'h', y: 1.25 }
    }, { responsive: true, displayModeBar: false });

    // Block length distribution by year
    const blockTraces = blockData.series.map(item => ({
      x: blockData.years, y: item.counts, type: 'bar', name: item.label
    }));

    Plotly.newPlot("chart-block-lengths", blockTraces, {
      barmode: 'stack',
      paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
      font: { color: '#94a3b8', family: 'monospace' },
      xaxis: { gridcolor: '#1e293b' },
      yaxis: { title: 'Радиограмм', gridcolor: '#1e293b' },
      margin: { t: 20, r: 20, l: 45, b: 40 },
      legend: { orientation: 'h', y: 1.25 }
    }, { responsive: true, displayModeBar: false });

    // Word co-occurrence table
    const coocTbody = document.getElementById("table-cooccur-body");
    coocTbody.innerHTML = "";
    if (cooData.pairs && cooData.pairs.length > 0) {
      cooData.pairs.forEach(p => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="mono-cell" style="color:var(--color-cyan); font-weight:bold;">${p.word1}</td>
          <td class="mono-cell" style="color:var(--color-amber); font-weight:bold;">${p.word2}</td>
          <td class="mono-cell"><span class="badge badge-emerald">${p.cooccurrences} раз</span></td>
        `;
        coocTbody.appendChild(tr);
      });
    } else {
      coocTbody.innerHTML = `<tr><td colspan="3" style="text-align:center; color:var(--text-muted);">Парные сочетания не обнаружены</td></tr>`;
    }

  } catch (err) {
    console.error("Structural changes load error:", err);
  }
}


// 3. ANOMALY EXPLORER
async function loadAnomalyExplorer(threshold = 3.0) {
  try {
    const [anomRes, febRes, gapRes] = await Promise.all([
      fetch(`/api/anomalies/daily?threshold=${threshold}`),
      fetch("/api/anomalies/feb2022"),
      fetch("/api/anomalies/gaps")
    ]);

    const anomData = await anomRes.json();
    const febData = await febRes.json();
    const gapData = await gapRes.json();

    // Populate anomalies table
    const tbody = document.getElementById("table-anomalies-body");
    tbody.innerHTML = "";
    if (anomData.anomalies && anomData.anomalies.length > 0) {
      anomData.anomalies.forEach(a => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="mono-cell"><strong>${a.date}</strong></td>
          <td class="mono-cell" style="color:var(--color-cyan); font-weight:bold;">${a.count}</td>
          <td class="mono-cell"><span class="badge badge-rose">Z = +${a.mod_z_score} MAD</span></td>
          <td class="mono-cell" style="color:var(--color-amber);">${a.poisson_p_value}</td>
          <td class="mono-cell"><small>${a.words_sample.join(', ')} (${a.words_count} слов)</small></td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Аномалии выше порога не обнаружены</td></tr>`;
    }

    // Feb 2022 Forensic Card
    document.getElementById("anom-feb2022-evidence").textContent = febData.duplicate_evidence;
    let febTimelineHtml = `<strong>Подтверждённая хронология февраля 2022 года (после очистки):</strong><br>`;
    febData.february_timeline.forEach(t => {
      febTimelineHtml += `• <strong>${t.date}:</strong> ${t.genuine_transmissions} подлинных радиограмм<br>`;
    });
    febTimelineHtml += `<br><span style="color:#10b981;">${febData.scientific_verdict}</span>`;
    document.getElementById("anom-feb2022-timeline").innerHTML = febTimelineHtml;

    // Archive Gaps Card
    document.getElementById("anom-gaps-warning").textContent = gapData.methodological_warning;
    let gapListHtml = `<strong>Крупнейшие лакуны мониторинга (> 14 дней):</strong><br>`;
    gapData.gap_records.forEach(g => {
      gapListHtml += `• <strong>${g.start_gap} &rarr; ${g.end_gap}:</strong> ${g.duration_days} дней (${g.classification})<br>`;
    });
    document.getElementById("anom-gaps-list").innerHTML = gapListHtml;

    // Threshold selector
    const sel = document.getElementById("anom-threshold-select");
    if (!sel._hooked) {
      sel.addEventListener("change", (e) => {
        loadAnomalyExplorer(parseFloat(e.target.value));
      });
      sel._hooked = true;
    }

  } catch (err) {
    console.error("Anomaly explorer load error:", err);
  }
}


// 4. NETWORK EVOLUTION
async function loadNetworkEvolution(epochId = 'epoch_2') {
  try {
    const [epRes, visRes] = await Promise.all([
      fetch("/api/network/epochs"),
      fetch(`/api/network/epoch_vis/${epochId}`)
    ]);

    const epochs = await epRes.json();
    const visData = await visRes.json();

    // Find current epoch metrics
    const curEpoch = epochs.find(e => e.epoch_id === epochId) || epochs[1];
    document.getElementById("epoch-stat-nodes").textContent = (curEpoch.nodes || 0).toLocaleString();
    document.getElementById("epoch-stat-edges").textContent = (curEpoch.edges || 0).toLocaleString();
    document.getElementById("epoch-stat-density").textContent = curEpoch.density;
    document.getElementById("epoch-stat-transitivity").textContent = curEpoch.transitivity_clustering;
    document.getElementById("epoch-stat-giant").textContent = `${curEpoch.giant_component_pct}% (${curEpoch.giant_component_size})`;

    // Populate Hubs Table
    const hubsTbody = document.getElementById("table-epoch-hubs-body");
    hubsTbody.innerHTML = "";
    if (curEpoch.top_hubs && curEpoch.top_hubs.length > 0) {
      curEpoch.top_hubs.forEach(h => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="mono-cell" style="font-weight:bold; color:${h.type === 'codeword' ? 'var(--color-amber)' : 'var(--color-purple)'};">${h.node}</td>
          <td class="mono-cell"><span class="badge ${h.type === 'codeword' ? 'badge-amber' : 'badge-cyan'}">${h.type}</span></td>
          <td class="mono-cell"><span class="badge badge-emerald">Степень: ${h.degree}</span></td>
        `;
        hubsTbody.appendChild(tr);
      });
    }

    // Vis.js Graph Rendering
    const container = document.getElementById("epoch-network-vis");
    (visData.nodes || []).forEach(n => {
      n.font = {
        color: '#f8fafc',
        face: 'JetBrains Mono, monospace',
        size: 11,
        strokeWidth: 2,
        strokeColor: '#070b12'
      };
    });
    (visData.edges || []).forEach(e => {
      delete e.label;
      e.font = { size: 0 };
      if (!e.title) {
        e.title = `Связь: ${e.from} ⟷ ${e.to} (Вес: ${e.value || 1})`;
      }
    });

    const data = {
      nodes: new vis.DataSet(visData.nodes),
      edges: new vis.DataSet(visData.edges)
    };
    const options = {
      nodes: {
        shape: 'dot',
        font: {
          color: '#f8fafc',
          face: 'JetBrains Mono, monospace',
          size: 11,
          strokeWidth: 2,
          strokeColor: '#070b12'
        }
      },
      edges: {
        smooth: { type: 'continuous', roundness: 0.15 },
        font: { size: 0 }
      },
      physics: {
        stabilization: { iterations: 160 },
        barnesHut: {
          gravitationalConstant: -5500,
          centralGravity: 0.22,
          springLength: 160,
          springConstant: 0.035,
          damping: 0.09,
          avoidOverlap: 0.8
        }
      },
      interaction: {
        hover: true,
        zoomView: true,
        dragView: true,
        navigationButtons: true
      }
    };
    if (epochNetworkInstance) epochNetworkInstance.destroy();
    epochNetworkInstance = new vis.Network(container, data, options);

    // Setup pill buttons
    document.querySelectorAll("#epoch-pill-buttons .callsign-pill").forEach(pill => {
      if (!pill._hooked) {
        pill.addEventListener("click", () => {
          document.querySelectorAll("#epoch-pill-buttons .callsign-pill").forEach(p => p.classList.remove("active"));
          pill.classList.add("active");
          const ep = pill.getAttribute("data-epoch");
          loadNetworkEvolution(ep);
        });
        pill._hooked = true;
      }
    });

  } catch (err) {
    console.error("Network evolution load error:", err);
  }
}


// 5. RESEARCH FINDINGS REGISTRY
async function loadResearchFindings() {
  try {
    const res = await fetch("/api/findings/registry");
    const data = await res.json();

    // Confirmed Facts
    const confContainer = document.getElementById("rf-confirmed-list");
    confContainer.innerHTML = "";
    data.confirmed_facts.forEach(f => {
      const card = document.createElement("div");
      card.className = "card";
      card.style.borderLeft = "4px solid var(--color-emerald)";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <h4 style="font-family:var(--font-mono); font-size:0.95rem; color:var(--text-primary);">${f.id}: ${f.title}</h4>
          <span class="badge badge-emerald">${f.status}</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem;">${f.evidence}</p>
        <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-cyan);">
          Первоисточники: ${f.sources.join(', ')}
        </div>
      `;
      confContainer.appendChild(card);
    });

    // Refuted Hypotheses
    const refContainer = document.getElementById("rf-refuted-list");
    refContainer.innerHTML = "";
    data.refuted_or_unconfirmed_hypotheses.forEach(h => {
      const card = document.createElement("div");
      card.className = "card";
      card.style.borderLeft = "4px solid var(--color-rose)";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <h4 style="font-family:var(--font-mono); font-size:0.95rem; color:var(--text-primary);">${h.id}: ${h.title}</h4>
          <span class="badge badge-rose">${h.status}</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-secondary);">${h.analysis}</p>
      `;
      refContainer.appendChild(card);
    });

    // Methodological Limitations
    const limContainer = document.getElementById("rf-limitations-list");
    limContainer.innerHTML = "";
    data.methodological_limitations.forEach(l => {
      const card = document.createElement("div");
      card.className = "card";
      card.style.borderLeft = "4px solid var(--color-amber)";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <h4 style="font-family:var(--font-mono); font-size:0.95rem; color:var(--text-primary);">${l.id}: ${l.title}</h4>
          <span class="badge badge-amber">LIMITATION</span>
        </div>
        <p style="font-size:0.85rem; color:var(--text-secondary);">${l.description}</p>
      `;
      limContainer.appendChild(card);
    });

  } catch (err) {
    console.error("Research findings load error:", err);
  }
}
