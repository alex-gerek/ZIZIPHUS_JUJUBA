# ZIZIPHUS JUJUBA: Структура реляционной базы данных (Database Schema)

СУБД: **SQLite 3**
Файл базы данных: `data/database/ziziphus_jujuba.db`
Режим журналирования: `WAL` (Write-Ahead Logging) для максимальной производительности чтения.

---

## 1. Таблица `Messages` (Радиограммы)
Хранит базовые записи о каждой зафиксированной передаче станции УВБ-76.

| Поле | Тип | Описание |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Уникальный номер радиограммы |
| `source_id` | INTEGER | Внешний ключ на таблицу `Sources` |
| `source_file` | TEXT | Исходный текстовый файл журнала (например, `2014_logs.txt`) |
| `source_line` | INTEGER | Номер строки в исходном файле первоисточника |
| `date` | TEXT | Дата передачи в формате `YYYY-MM-DD` |
| `year` | INTEGER | Календарный год |
| `month` | INTEGER | Месяц (1–12) |
| `day` | INTEGER | День месяца (1–31) |
| `time_as_logged` | TEXT | Время фиксации в журнале (`HH:MM` или `HH:MM:SS`) |
| `timezone` | TEXT | Часовой пояс (по умолчанию `UTC`) |
| `callsign` | TEXT | Позывной станции (например, `МДЖБ`, `ЖУОЗ`, `АНВФ`, `НЖТИ`) |
| `header_number` | TEXT | Пятизначная группа или вводный номер (например, `14 882`) |
| `full_text` | TEXT | Полный текст радиограммы |
| `full_word_sequence` | TEXT | Последовательность кодовых слов |
| `block_count` | INTEGER | Количество кодоблоков в сообщении |
| `quality_flag` | TEXT | Флаг разборчивости и качества записи |
| `is_duplicate` | INTEGER | Признак дубликата (0 = чистое сообщение, 1 = дубликат) |
| `duplicate_type` | TEXT | Тип дубликата (`EXACT_TIMESTAMP`, `CROSS_FILE_DUPLICATE`) |
| `duplicate_reason` | TEXT | Обоснование исключения |
| `dedup_group_id` | TEXT | Идентификатор группы схожести |

---

## 2. Таблица `CodeBlocks` (Кодовые блоки)
Нормализованные структуры вида: **Кодовое слово + 4-значная группа 1 + 4-значная группа 2**.

| Поле | Тип | Описание |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Идентификатор кодоблока |
| `message_id` | INTEGER | Внешний ключ на `Messages.id` (ON DELETE CASCADE) |
| `block_index` | INTEGER | Порядковый номер блока внутри сообщения (1, 2, 3...) |
| `code_word` | TEXT | Кодовое слово на кириллице (например, `ЗИЗИФУС`, `ПАСКОИТ`) |
| `code_word_latin` | TEXT | Международная транскрипция Priyom (`ZIZIFUS`) |
| `digit_group_1` | TEXT | Первая четырехзначная группа цифр (например, `7724`) |
| `digit_group_2` | TEXT | Вторая четырехзначная группа цифр (например, `8209`) |
| `digit_combination` | TEXT | Полная восьмизначная комбинация (`7724 8209`) |
| `uncertainty_flag` | INTEGER | Флаг сомнения оператора при приеме на слух (0/1) |
| `notes` | TEXT | Примечания |

---

## 3. Таблица `Sources` (Первоисточники)
Аудиторский след происхождения каждого исходного файла и контрольные суммы.

| Поле | Тип | Описание |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Идентификатор источника |
| `file_name` | TEXT | Название файла (например, `2014_logs.txt`) |
| `file_path` | TEXT | Локальный путь к оригинальному файлу |
| `sha256_checksum` | TEXT | Контрольная сумма SHA-256 оригинального файла |
| `raw_line_count` | INTEGER | Общее количество строк в файле |
| `messages_parsed` | INTEGER | Число успешно извлеченных радиограмм |
| `source_url` | TEXT | Официальный URL репозитория / Priyom.org |

---

## 4. Таблица `HistoricalEvents` (Исторические события)
Реестр верифицированных геополитических, военных и переговорных событий для модуля Event-Study.

| Поле | Тип | Описание |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Идентификатор события |
| `event_name` | TEXT | Название события на русском языке |
| `event_name_en` | TEXT | Название события на английском языке |
| `start_date` | TEXT | Дата начала события (`YYYY-MM-DD`) |
| `end_date` | TEXT | Дата завершения события |
| `category` | TEXT | Категория (`MILITARY_ESCALATION`, `DIPLOMACY`, `EXERCISE`, `CRISIS`) |
| `region` | TEXT | Географический регион |
| `description` | TEXT | Историческая справка |
| `source_url` | TEXT | Источник датировки (ООН, ОБСЕ, международные архивы) |
| `dating_accuracy` | TEXT | Точность датировки (`EXACT_DAY`, `MONTH`) |

---

## 5. Таблица `AuditLog` (Журнал аудита данных)
Протокол всех действий по фильтрации, дедупликации и верификации данных.

| Поле | Тип | Описание |
|:---|:---|:---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Номер записи аудита |
| `source_file` | TEXT | Файл, в котором обнаружена аномалия |
| `source_line` | INTEGER | Строка аномалии |
| `date` | TEXT | Дата аномальной записи |
| `time` | TEXT | Время записи |
| `audit_type` | TEXT | Тип аудита (`CROSS_FILE_DUPLICATE`, `CORRUPTED_ENTRY`, `LIVE_INTERCEPTION`) |
| `action_taken` | TEXT | Предпринятое действие (`FLAGGED_DUPLICATE`, `INSERTED_PRIMARY`) |
| `rationale` | TEXT | Научное и техническое обоснование действия |
| `raw_snippet` | TEXT | Точный исходный фрагмент текста |
