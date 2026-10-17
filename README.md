<p align="center">
  <img src="app/static/img/ziziphus_icon.png" width="128" height="128" alt="Ziziphus Jujuba Logo">
</p>

# ZIZIPHUS JUJUBA
## Signal Intelligence & Pattern Analysis Lab

<p align="center">
  <b><a href="#-русская-версия">🇷🇺 Читать на русском</a></b> &nbsp;|&nbsp; 
  <b><a href="#-english-version">🇬🇧 Read in English</a></b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20--%203.14-blue?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0078d7?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/Database-SQLite%203-003b57?style=flat-square" alt="Database">
  <img src="https://img.shields.io/badge/Status-Operational%20%7C%20Phase%202%20Validated-10b981?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Reproducibility-100%25%20Verified-brightgreen?style=flat-square" alt="Reproducibility">
  <img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square" alt="License">
</p>

---

# 🇷🇺 Русская версия

## 1. О проекте простыми словами

> **Главный вопрос исследования:**  
> *«Можно ли раскрыть внутреннюю структуру и поведение сложной системы радиообмена, вообще не зная содержания шифрованных сообщений?»*

**ZIZIPHUS JUJUBA** — это автономная научно-исследовательская лаборатория цифровой радиоэлектронной разведки и анализа паттернов (*Signal Intelligence & Traffic Analysis*). Проект посвящен исследованию легендарной коротковолновой станции **УВБ-76 («Жужжалка» / The Buzzer, частота 4625 кГц USB)** на основе открытых журналов любительского радиомониторинга за 2010–2022 годы.

Военные шифры станции математически невскрываемы без одноразовых ключей. Однако передают радиограммы **живые люди**, а принимают и координируют их **реальные узлы связи**. Люди дежурят по сменам, у них есть любимые привычки, регламентные дни проверок, а во время реальных геополитических кризисов их поведение меняется.

**ZIZIPHUS JUJUBA** не взламывает тексты — лаборатория применяет высшую математику и машинное обучение к **поведению эфира**: времени выходов, частотам повторений, паузам между передачами, графам связей между позывными и сопоставлению активности с событиями в реальном мире.

Программа работает **полностью автономно и локально**, не отправляет никаких данных в сеть и гарантирует 100% математическую воспроизводимость каждого расчета.

---

## 2. Что внутри и какие расчеты мы обновили (13 аналитических вкладок)

В обновленной версии лаборатории мы перепроверили первичные логи, провели форензик-аудит (устранили ошибки и дублирования в архивах) и объединили анализ в 13 интерактивных разделов:

| № | Раздел лаборатории | Что делает математическая модель (простыми словами) |
|---|---|---|
| **1** | **Overview (Обзор)** | Сводные метрики: дедуплицированная база сообщений, хронология с 1997 по 2022 гг., ключевые показатели системы. |
| **2** | **Frequency Analysis (Частотный анализ)** | Закон Ципфа: какие позывные, кодовые слова и группы цифр звучат чаще всего, а какие уникальны. |
| **3** | **Repetitions & Intervals (Повторы и паузы)** | Сколько живут кодовые слова, через какие промежутки времени повторяются блоки и когда меняются таблицы шифроблокнотов. |
| **4** | **Time Series (Временные ряды)** | Суточные ритмы: доказано, что **78.4%** радиограмм передаются с 10:00 до 21:00 MSK (график штабных смен), а ночью наступает спад. |
| **5** | **Clustering (Кластеризация режимов)** | Модели *K-Means* и *DBSCAN* без подсказок группируют передачи на три типа: рутинная проверка связи, экстренные циркулярные приказы и сбои. |
| **6** | **Graph Intelligence (Граф связей)** | «Социальная сеть» радиоэфира: алгоритмы центральности (*Degree*, *Betweenness*) выявляют ключевые узлы-мосты и командные центры. |
| **7** | **Historical Event Study (Корреляция с событиями)** | Анализ реакции радиостанции на реальные кризисы (Крым 2014 г., масштабные учения, геополитические обострения). |
| **8** | **Hypothesis Testing (Проверка гипотез)** | Математическая строгость: тесты хи-квадрат, Манна-Уитни и критерии согласия Пуассона доказывают, где есть реальная закономерность, а где случайность ($p < 0.001$). |
| **9** | **Traffic Behavior (Поведение радиообмена)** | Фактор Фано ($D = 14.8 \gg 1.0$) опровергает стационарный шум и доказывает лавинообразный, «пакетный» характер военных приказов. |
| **10** | **Structural Dynamics (Структурные изменения)** | Закон Хипса ($V(N) \propto N^{0.742}$): скорость исчерпания словаря доказывает закрытый армейский фонд позывных (УЗБ-76 $\to$ МДЖБ $\to$ ЖУОЗ $\to$ АНВФ $\to$ НЖТИ). |
| **11** | **Anomaly Explorer (Анализ аномалий)** | Робастный *Modified Z-Score (MAD)* и *Isolation Forest*: обнаружение настоящих всплесков активности и отсеивание технических сбоев WebSDR-приемников. |
| **12** | **Network Evolution (Эволюция сети)** | Как менялась топология радиосети на протяжении 4 исторических эпох: 2011–2013, 2014–2015, 2016–2019 и 2020–2022 гг. |
| **13** | **Research Findings (Доказательный реестр)** | Итоговый научный реестр: доказанные факты (включая аутентичность слова *«ЗИЗИФУС»*, зафиксированного 6 раз за 8 лет) и развенчанные мифы. |

---

## 3. Как скачать и запустить на своем компьютере

Для работы с готовыми сборками **вам не нужно устанавливать Python или настраивать библиотеки**. Всё необходимое уже упаковано внутри.

### 🪟 Windows (Portable ZIP)
1. Скачайте архив **`ZiziphusJujuba-v2.0.0-windows-x64.zip`** из раздела [Releases](https://github.com/alex-gerek/ZIZIPHUS_JUJUBA/releases).
2. Распакуйте архив в любую папку (например, на Рабочий стол или диск `C:` / `D:`).
3. Дважды кликните по файлу **`ZiziphusJujuba.exe`** (или `start.bat`).
4. Приложение автоматически запустится и откроет лабораторию в вашем обычном веб-браузере по адресу:  
   👉 **`http://127.0.0.1:8765`**

> [!TIP]
> **Защита от случайного повторного запуска:** если программа уже работает в фоновом режиме, повторный клик по `.exe` не вызовет ошибку, а мгновенно откроет браузер со всеми вашими графиками.

---

### 🍏 macOS (Apple Silicon M1/M2/M3/M4 и Intel Mac)
1. Скачайте подходящий архив из раздела [Releases](https://github.com/alex-gerek/ZIZIPHUS_JUJUBA/releases):
   * Для современных Mac (процессоры **M1, M2, M3, M4**): **`ZiziphusJujuba-v2.0.0-macos-arm64.zip`**
   * Для Mac предыдущих поколений (процессоры **Intel**): **`ZiziphusJujuba-v2.0.0-macos-intel.zip`**
2. Распакуйте скачанный ZIP-архив в папку `Загрузки` или `Программы` (`Applications`).
3. Запустите приложение **`ZiziphusJujuba.app`** двойным кликом.

#### ⚠️ Важное замечание для macOS (Gatekeeper):
Так как сборка выпущена независимым исследователем без платного ежегодного сертификата Apple Developer ID, операционная система macOS при первом открытии может показать предупреждение: *«Приложение загружено из Интернета»* или *«Не удается открыть, так как разработчик не может быть проверен»*.

**Как запустить за 5 секунд (два простых способа):**
* **Способ 1 (через Finder):** Нажмите по `ZiziphusJujuba.app` **правой кнопкой мыши** (или зажмите клавишу `Control` и кликните) $\to$ выберите пункт **«Открыть»** (Open) $\to$ в появившемся окне подтвердите нажатием кнопки **«Открыть»**. macOS навсегда запомнит это разрешение.
* **Способ 2 (через Терминал):** Если система заблокировала файл, откройте Терминал и выполните команду снятия метки карантина:
  ```bash
  xattr -cr /Applications/ZiziphusJujuba.app
  ```

---

### 💻 Запуск из исходного кода (для разработчиков и исследователей)

Если вы хотите запустить проект напрямую из исходников:
```bash
# 1. Клонировать репозиторий
git clone https://github.com/alex-gerek/ZIZIPHUS_JUJUBA.git
cd ZIZIPHUS_JUJUBA

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить лабораторию
python run_app.py

# 4. Запустить полный набор автоматических тестов (23 теста)
python -m unittest discover tests
```

---

<br>

---

# 🇬🇧 English Version

## 1. About the Project in Plain English

> **Core Research Question:**  
> *“Can we uncover the operational structure, hierarchy, and dynamics of an encrypted radio network without decrypting a single word of the underlying messages?”*

**ZIZIPHUS JUJUBA** is an autonomous, open-source Signal Intelligence (SIGINT) and Pattern Analysis laboratory. It is dedicated to the empirical study of the legendary Russian military shortwave station **UVB-76 ("The Buzzer", broadcasting at 4625.0 kHz USB)** using open community archives spanning from 2010 to 2022.

The tactical military ciphers transmitted by UVB-76 are mathematically unbreakable without one-time pads. However, the radio station is operated by **human beings** and connects **physical military command nodes**. Human operators follow shift rosters, exhibit routine habits, conduct scheduled system checks, and alter their behavior during real-world crises.

**ZIZIPHUS JUJUBA** does not attempt to break the ciphers. Instead, it applies data science, graph theory, and mathematical modeling to **channel traffic behavior**: transmission timing, repetition intervals, vocabulary growth, co-occurrence networks, and geopolitical event correlations.

The entire platform runs **100% locally and offline**, requires zero cloud services, and guarantees strict mathematical reproducibility of all findings.

---

## 2. Architecture & Enhanced Research Modules (13 Analytical Tabs)

In this release, we conducted a forensic data audit (cleaning archive duplicates and anomalies) and structured the lab into 13 comprehensive interactive tabs:

| # | Analytical Module | What the Mathematical Model Does |
|---|---|---|
| **1** | **Overview** | System-wide metrics, deduplicated SQLite message database, and historical timeline from 1997 through 2022. |
| **2** | **Frequency Analysis** | Zipfian distribution of phonetic codewords, callsigns, and number combinations. |
| **3** | **Repetitions & Intervals** | Codeword life cycles, retransmission lags, and detection of 28-day cipher pad rotation cycles. |
| **4** | **Time Series** | Diurnal profiling: demonstrates that **78.4%** of all broadcasts occur between 07:00–18:00 UTC (staff shift schedule) followed by night silence. |
| **5** | **Clustering Modes** | Unsupervised *K-Means* and *DBSCAN* clustering classifying signals into routine checks, emergency alerts, and transmission anomalies. |
| **6** | **Graph Intelligence** | Network graph analysis: Degree and Betweenness centrality identify command hub nodes and bridge messages in the communication network. |
| **7** | **Historical Event Study** | Statistical correlation testing radio bursts against geopolitical and military events (e.g. 2014 Crimean crisis and large-scale military drills). |
| **8** | **Hypothesis Testing** | Strict statistical testing: Chi-Square, Mann-Whitney, and Poisson dispersion tests proving significance vs random chance ($p < 0.001$). |
| **9** | **Traffic Behavior** | High Fano factor ($D = 14.8 \gg 1.0$) refutes stationary Poisson noise, proving bursty, clustered packet transmission dynamics. |
| **10** | **Structural Dynamics** | Heaps' Law ($V(N) \propto N^{0.742}$): vocabulary saturation proving a strictly closed military phonetic codebook across callsign eras (UZB-76 $\to$ MDZhB $\to$ ZhUOZ $\to$ ANVF $\to$ NZhTI). |
| **11** | **Anomaly Explorer** | Robust *Modified Z-Score (MAD)* and *Isolation Forest* algorithms detecting authentic activity surges and filtering out WebSDR receiver downtimes. |
| **12** | **Network Evolution** | Longitudinal topological analysis across 4 distinct historical epochs (2011–2013, 2014–2015, 2016–2019, 2020–2022). |
| **13** | **Research Findings** | Comprehensive evidence registry: empirically proven findings (including the authentic 6 logged occurrences of codeword *“ZIZIPHUS”* over 8 years) vs debunked myths. |

---

## 3. How to Download and Run on Your Computer

Pre-compiled standalone releases **do not require Python or any manual package installation**. Everything is included out-of-the-box.

### 🪟 Windows (Portable ZIP)
1. Download **`ZiziphusJujuba-v2.0.0-windows-x64.zip`** from [Releases](https://github.com/alex-gerek/ZIZIPHUS_JUJUBA/releases).
2. Extract the archive into any folder of your choice.
3. Double-click **`ZiziphusJujuba.exe`** (or `start.bat`).
4. The application starts instantly and opens the dashboard in your default browser at:  
   👉 **`http://127.0.0.1:8765`**

> [!TIP]
> **Crash-proof startup:** If the server is already active in the background, clicking the launcher again will gracefully open your browser directly instead of failing.

---

### 🍏 macOS (Apple Silicon M1/M2/M3/M4 & Intel Mac)
1. Download the release archive matching your Mac architecture from [Releases](https://github.com/alex-gerek/ZIZIPHUS_JUJUBA/releases):
   * For modern Apple Silicon Macs (**M1, M2, M3, M4**): **`ZiziphusJujuba-v2.0.0-macos-arm64.zip`**
   * For Intel-based Macs (**Intel Core i5/i7/i9/Xeon**): **`ZiziphusJujuba-v2.0.0-macos-intel.zip`**
2. Unzip the downloaded file in your `Downloads` or `Applications` folder.
3. Double-click **`ZiziphusJujuba.app`** to launch.

#### ⚠️ Note on macOS Gatekeeper:
Because this application is built independently without an annual Apple Developer ID commercial subscription, macOS Gatekeeper may present a dialog stating: *"App downloaded from the Internet"* or *"Developer cannot be verified"*.

**Quick 5-second solution:**
* **Option 1 (via Finder):** Right-click (or hold `Control` and click) on `ZiziphusJujuba.app` $\to$ select **Open** $\to$ click **Open** in the confirmation dialog. macOS will permanently save this permission.
* **Option 2 (via Terminal):** If macOS blocks execution, remove the quarantine attribute with:
  ```bash
  xattr -cr /Applications/ZiziphusJujuba.app
  ```

---

### 💻 Running from Source Code (Developers & Researchers)

To run the project directly from source:
```bash
# 1. Clone the repository
git clone https://github.com/alex-gerek/ZIZIPHUS_JUJUBA.git
cd ZIZIPHUS_JUJUBA

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the laboratory
python run_app.py

# 4. Run automated test suite (23 unit tests)
python -m unittest discover tests
```

---

## 4. Repository Structure

```text
ZIZIPHUS_JUJUBA/
│
├── app/                      # FastAPI backend & web dashboard
│   ├── static/               # CSS styles (lab_dark.css), JS (lab_app.js), icons
│   ├── templates/            # HTML5 dashboard templates (index.html)
│   └── main.py               # REST API endpoints (32 routes across 13 tabs)
├── data/
│   ├── database/             # Relational SQLite database (ziziphus_jujuba.db)
│   ├── cleaned/              # Cleaned, deduplicated dataset CSVs
│   ├── raw/                  # Primary monitoring logs with SHA-256 verification
│   └── historical_events/    # Historical geopolitical events registry
├── docs/                     # Documentation & academic reports
│   ├── INSTALLATION.md       # Detailed multi-platform setup guide
│   ├── DATABASE_SCHEMA.md    # Normalized SQLite schema documentation
│   ├── MATHEMATICAL_METHODS.md # Mathematical definitions and formulas
│   ├── DATA_SOURCES_AND_LICENSES.md # Primary sources & licensing terms
│   └── LIMITATIONS.md        # Methodological constraints & caveats
├── exports/                  # Exported analytical datasets
├── reports/                  # Academic research reports
├── src/                      # Core mathematical and analytical engines
│   ├── analysis/             # Traffic, structure, anomaly & frequency models
│   ├── database/             # SQLite connection and migration manager
│   ├── ingestion/            # Pipeline building database from primary logs
│   ├── models/               # Graph evolution, Event-Study, clustering
│   └── parsing/              # Message normalization and phonetic parser
├── tests/                    # Automated regression & integration test suite
├── requirements.txt          # Python dependencies
├── COMPREHENSIVE_RESEARCH_REPORT.md # Full peer-style academic research report
├── README.md                 # Project README (Bilingual: RU / EN)
└── start.bat                 # One-click Windows starter script
```

---

## 5. License & Ethics

* **License:** [MIT License](LICENSE).
* **Open Science & Ethics:** This research is conducted strictly for educational and open-science purposes using public, non-classified amateur radio monitoring archives collected by enthusiasts worldwide over several decades. No classified or unauthorized interception systems were utilized.
