# СРОЧНЫЙ АУДИТ ПЕРВОИСТОЧНИКОВ: СЛОВО «ЗИЗИФУС» В ЖУРНАЛАХ УВБ-76
## Отчет независимой проверки достоверности данных (Signal Intelligence Audit)
**Проект:** ZIZIPHUS JUJUBA  
**Дата проведения проверки:** 16 октября 2026 г.  
**Вердикт аудита:** **ПОДТВЕРЖДЕНО (CONFIRMED)** — факт присутствия кодового слова «ЗИЗИФУС» в первичных журналах радиопередач УВБ-76 полностью подтвержден независимыми первоисточниками Priyom.org.

---

## 1. Введение и предмет расследования

В рамках проверки возникшего предположения о том, что слово «ЗИЗИФУС» якобы отсутствует в подлинных архивах УВБ-76, а публикации о нем могут являться фальсификацией или артефактом пост-обработки, лабораторией проведено независимое расследование.

Были исследованы:
1. Исходные архивы GitHub (`UVB-76-Structured-Signal-Analysis-main.zip` и внутренний `tar.xz`).
2. Первичные текстовые журналы радиопередач за 2010–2022 гг. (`*_logs.txt`).
3. Подготовленные вторичные таблицы (`*.csv`, `*.json`).
4. **Независимый первоисточник: открытые веб-архивы Priyom.org** (прямые HTTP-запросы к официальным страницам мониторинга).
5. Анализ кодировок Unicode (проверка на латинские омоглифы, такие как латинская `C`).
6. Этимология и транслитерация (`ZIZIPHUS` vs `ZIZIFUS`).

---

## 2. Результаты поиска по всем файлам проекта и архивам

Поиск по шаблонам `ЗИЗИФУС`, `ЗИЗИФУC` (латинская C), `ZIZIFUS`, `ZIZIPHUS`, `ЗИЗИФ` показал:

| Источник | Файл | Количество вхождений | Статус |
|---|---|---|---|
| **Первичный TXT (GitHub ZIP & tar.xz)** | `2011_logs.txt` | 2 (1 Cyrillic + 1 Latin) | **Подтверждено** |
| **Первичный TXT (GitHub ZIP & tar.xz)** | `2014_logs.txt` | 4 (2 Cyrillic + 2 Latin) | **Подтверждено** |
| **Первичный TXT (GitHub ZIP & tar.xz)** | `2015_logs.txt` | 4 (2 Cyrillic + 2 Latin) | **Подтверждено** |
| **Первичный TXT (GitHub ZIP & tar.xz)** | `2019_logs.txt` | 2 (1 Cyrillic + 1 Latin) | **Подтверждено** |
| **Вторичные CSV** | `UVB76_crossword_number_links.csv` | 6 записей | **Подтверждено** |
| **Вторичные CSV** | `UVB76_full_messages.csv` | 6 записей | **Подтверждено** |
| **Вторичные CSV** | `UVB76_full_messages_deduplicated.csv` | 6 записей | **Подтверждено** |
| **Первоисточник Priyom.org (Live Web)** | `priyom.org/...` (соотв. месяцы) | 6 записей | **ПОДТВЕРЖДЕНО НА 100%** |

Вариант с написанием **`ZIZIPHUS`** (через латинское `PH`) в первичных журналах радиоперехватов **отсутствует**, так как радиомониторы Priyom.org транслитерируют русскую букву «Ф» исключительно как **`F`** (`ZIZIFUS`), а не по правилам латинской ботанической номенклатуры (*Ziziphus jujuba*). Это объясняет, почему поверхностный поиск по английскому слову `ZIZIPHUS` не давал результатов.

Все символы в слове «ЗИЗИФУС» являются подлинными символами кириллицы:
`U+0417 (З) U+0418 (И) U+0417 (З) U+0418 (И) U+0424 (Ф) U+0423 (У) U+0421 (С)` — никаких скрытых латинских подмен или омоглифов не обнаружено.

---

## 3. Детальный реестр всех найденных совпадений

### Совпадение № 1: 05 сентября 2011 года
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2011_logs.txt`
- **Строки:** 302–304
- **Дата и время:** `September 05, 2011 12:50 UTC`
- **Позывной и заголовок:** `MDZhB / МДЖБ` | `09402`
- **Полный фрагмент из файла:**
  ```text
  September 05, 2011	12:50	
  4.625 MHz
  J3E (USB)
  MDZhB /МДЖБ	
  09402

  ZIZIFUS 91363241

  ЗИЗИФУС 91363241

  Male voice
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2011`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <tr>
  <td>September 05, 2011</td>
  <td>12:50</td>
  <td><ul><li>4.625 MHz</li><li style="list-style: none;">J3E (USB)</li></ul></td>
  <td>MDZhB /МДЖБ</td>
  <td valign="top"><p>09402</p></td>
  <td valign="top"><p class="messageCol">ZIZIFUS 91363241</p></td>
  <td width="200" valign="top"><p class="messageCol">ЗИЗИФУС 91363241</p></td>
  <td class="comments">Male voice</td>
  </tr>
  ```

---

### Совпадение № 2: 09 апреля 2014 года (в паре со словом «ГАШЕНИЕ»)
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2014_logs.txt`
- **Строки:** 671–685
- **Дата и время:** `April 09, 2014 11:48 UTC`
- **Позывной и заголовок:** `MDZhB/МДЖБ:ru` | `34568`
- **Полный фрагмент из файла:**
  ```text
  April 09, 2014	11:48	
  4.625 MHz
  J3E (USB)
  MDZhB/МДЖБ:ru	
  34568

  GASHENIE 48954813

  ZIZIFUS 98361935

  ГАШЕНИЕ 48954813

  ЗИЗИФУС 98361935

  Logged by Webweasel/Argonn/Gwraspe
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2014/april`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <p class="messageCol">GASHENIE 48954813</p>
  <p class="messageCol">ZIZIFUS 98361935</p>
  <p class="messageCol">ГАШЕНИЕ 48954813</p>
  <p class="messageCol">ЗИЗИФУС 98361935</p>
  <td class="comments">Logged by Webweasel/Argonn/Gwraspe</td>
  ```

---

### Совпадение № 3: 02 октября 2014 года (совпадение 7724 8209 со словом «ПАСКОИТ»)
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2014_logs.txt`
- **Строки:** 1665–1675
- **Дата и время:** `October 02, 2014 12:14 UTC`
- **Позывной и заголовок:** `MDZhB` | `01842`
- **Полный фрагмент из файла:**
  ```text
  October 02, 2014	12:14	
  4625 kHz
  J3E (USB)
  MDZhB	
  01842

  ZIZIFUS 77248209

  ЗИЗИФУС 77248209

  Logged by PeterSpb
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2014/october`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <tr>
  <td>October 02, 2014</td>
  <td>12:14</td>
  <td><ul><li>4625 kHz</li><li style="list-style: none;">J3E (USB)</li></ul></td>
  <td>MDZhB</td>
  <td valign="top"><p>01842</p></td>
  <td><p class="messageCol">ZIZIFUS 77248209</p></td>
  <td width="200" valign="top"><p class="messageCol">ЗИЗИФУС 77248209</p></td>
  <td class="comments">Logged by PeterSpb</td>
  </tr>
  ```

#### Сверка парной записи со словом «ПАСКОИТ» (04 сентября 2014 года):
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2014_logs.txt`
- **Строки:** 1333–1343
- **Дата и время:** `September 04, 2014 13:24 UTC`
- **Позывной и заголовок:** `MDZhB` | `38120`
- **Полный фрагмент из файла:**
  ```text
  September 04, 2014	13:24	
  4625 kHz
  J3E (USB)
  MDZhB	
  38120

  PASKOIT 77248209

  ПАСКОИТ 77248209

  Logged by PeterSpb
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2014/september`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <tr>
  <td>September 04, 2014</td>
  <td>13:24</td>
  <td><ul><li>4625 kHz</li><li style="list-style: none;">J3E (USB)</li></ul></td>
  <td>MDZhB</td>
  <td valign="top"><p>38120</p></td>
  <td><p class="messageCol">PASKOIT 77248209</p></td>
  <td width="200" valign="top"><p class="messageCol">ПАСКОИТ 77248209</p></td>
  <td class="comments">Logged by PeterSpb</td>
  </tr>
  ```
Обе радиограммы зафиксированы одним и тем же наблюдателем (`PeterSpb`) с интервалом ровно 28 дней и подтверждены в независимом открытом источнике.

---

### Совпадение № 4: 07 мая 2015 года
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2015_logs.txt`
- **Строки:** 1314–1324
- **Дата и время:** `May 07, 2015 13:58 UTC`
- **Позывной и заголовок:** `MDZhB /МДЖБ` | `24855`
- **Полный фрагмент из файла:**
  ```text
  May 07, 2015	13:58	
  4625 kHz
  J3E (USB)
  MDZhB /МДЖБ	
  24855

  ZIZIFUS 36116021

  ЗИЗИФУС 36116021

  Recorded by PeterSpb, transcripted by PeterSpb/Argonn
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2015/may`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <p class="messageCol">ZIZIFUS 36116021</p>
  <p class="messageCol">ЗИЗИФУС 36116021</p>
  <td class="comments">Recorded by PeterSpb, transcripted by PeterSpb/Argonn</td>
  ```

---

### Совпадение № 5: 11 октября 2015 года
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2015_logs.txt`
- **Строки:** 2825–2835
- **Дата и время:** `October 11, 2015 12:29 UTC`
- **Позывной и заголовок:** `MDZhB /МДЖБ` | `67253`
- **Полный фрагмент из файла:**
  ```text
  October 11, 2015	12:29	
  4625 kHz
  J3E (USB)
  MDZhB /МДЖБ	
  67253

  ZIZIFUS 76116021

  ЗИЗИФУС 76116021

  Recorded by PeterSpb, Argonn
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2015/october`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <p class="messageCol">ZIZIFUS 76116021</p>
  <p class="messageCol">ЗИЗИФУС 76116021</p>
  <td class="comments">Recorded by PeterSpb, Argonn</td>
  ```

---

### Совпадение № 6: 19 июня 2019 года (в паре со словом «НИЗКИЙ»)
- **Файл:** `UVB-76-Structured-Signal-Analysis-main/data/raw/2019_logs.txt`
- **Строки:** 1813–1820
- **Дата и время:** `June 19, 2019 09:40 UTC`
- **Позывной и заголовок:** `ZhUOZ /ЖУОЗ` | `27480`
- **Полный фрагмент из файла:**
  ```text
  June 19, 2019	09:40	
  4625 kHz
  J3E (USB)
  ZhUOZ /ЖУОЗ	27480	
  NIZKIJ 0171 6479 ZIZIFUS 3611 6021

  НИЗКИЙ 0171 6479 ЗИЗИФУС 3611 6021
  ```
- **Сверка с Priyom.org:** URL: `https://priyom.org/military-stations/russia/the-buzzer/2019/june`
  Фрагмент HTML со страницы Priyom.org:
  ```html
  <p class="messageCol">NIZKIJ 0171 6479 ZIZIFUS 3611 6021</p>
  <p class="messageCol">НИЗКИЙ 0171 6479 ЗИЗИФУС 3611 6021</p>
  ```

---

## 4. Происхождение записей и проверка на фальсификацию

В ходе форензик-аудита проверены три гипотезы:

1. **Гипотеза А: Слово «ЗИЗИФУС» было добавлено автором репозитория GitHub (Austin Smith / Leerrooy95) в 2025 году.**
   - **Опровергнуто:** Все 6 записей присутствуют на официальном сайте Priyom.org в архивах за соответствующие годы и месяцы (2011, 2014, 2015, 2019), которые ведутся независимым международным сообществом радиомониторинга более 15 лет и были созданы задолго до появления репозитория GitHub.

2. **Гипотеза Б: Слово «ЗИЗИФУС» возникло в результате генерации ИИ или ошибки скрипта.**
   - **Опровергнуто:** Записи сопровождаются подлинными метаданными наблюдателей (`PeterSpb`, `Argonn`, `Gwraspe`, `Webweasel`), частотами (`4.625 MHz`, `4625 kHz`), модуляцией `J3E (USB)` и пятизначными заголовками. Текстовые файлы репозитория GitHub являются прямым дампом HTML-страниц Priyom.org.

3. **Гипотеза В: Источник сомнений — поиск по неправильному написанию.**
   - **Подтверждено:** Попытка найти слово по запросу `ZIZIPHUS` (английское ботаническое написание через `ph`) дает 0 результатов, поскольку радиолюбители Priyom.org транслитерируют звук [ф] исключительно как букву `F` (`ZIZIFUS`).

---

## 5. Итоговый вердикт

> ### ИТОГОВЫЙ ВЕРДИКТ: ПОДТВЕРЖДЕНО (CONFIRMED)
>
> 1. Кодовое слово **«ЗИЗИФУС» (ZIZIFUS)** является **подлинным историческим кодовым словом радиостанции УВБ-76**, зафиксированным в эфире как минимум 6 раз в период с 2011 по 2019 год.
> 2. Совпадение 8-значной цифровой комбинации **`7724 8209`** у радиограмм **ПАСКОИТ (04.09.2014)** и **ЗИЗИФУС (02.10.2014)** является **документальным фактом первичных журналов Priyom.org**, а не расчетной моделью или артефактом пост-обработки.
> 3. Данные являются достоверными и **не подлежат исключению из исследовательской базы данных**.
