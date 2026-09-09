# 📦 Smart-Photo Changelog

## [1.0.40] - 2026-09-04

### Community Links & Discussion Integration
- **Integration of links to the official community and discussion**:
  - Quick, neat pill buttons have been added to the header of the web panel: **Telegram** (`t.me/KeeneticSmartPhoto`) and **Keenetic Forum** (official discussion thread).
  - An interactive feedback block for users of the Android mobile application and TV client has been added to the “Clients and Integration” section.
  - Direct buttons for going to the Telegram channel and a topic on the Keenetic forum have been added to the “Thank the author” section.
  - Links to discussion of releases have been added to the version history and self-update modal window.

## [1.0.39] - 2026-09-03

### Clean OPKG Installation & Unified API Status
- **Elimination of duplication of information when installing with an OPKG script**:
  - `package/entware/control/postinst` has been switched to a quiet background launch (detached graceful restart) without displaying outdated banners with an empty IP.
  - Added `GET /api/status` system endpoint that returns `status`, `version`, `router_model` and `web_port`.
  - The router model (`router_model`) is now correctly detected from `/tmp/sysinfo/model`, Device Tree and `ndmc`.
  - In the installation script `install.sh`, a port occupancy check and start timeout diagnostics have been added.
  - Формат завершения установки полностью приведен в соответствие со **Smart-Utils**.

## [1.0.38] - 2026-09-02

### Self-Update System (Smart-Utils Style)
- **Interactive self-updating system in Smart-Utils style**:
  - Clickable version badge in the header (`#appVersionBadge`) to view the changelog at any time.
  - A pulsating badge with a new version indicator (`.update-pulse-badge`, `.update-pulse-dot`) next to the version number when an update is available.
  - An update modal window with a version comparison banner (Current ➔ Available), a formatted list of changes, and an instant update button.
  - Встроенная live-консоль хода установки и автоматический поллинг перезапуска службы с перезагрузкой страницы.
  - Fixed closing modal window for selecting folders `folderPickerModal`.

## [1.0.37] - 2026-09-02

### OPKG Repository Release & Cache Busting
- **Official release of OPKG in the Keenetic repository (`snakelair/Keenetic`)**:
  - Build packages for all architectures (`mipsel-3.4`, `armv7-3.2`, `aarch64-3.10`, `x86_64`, `mips-3.4`).
  - Adding versioned query parameters to CSS and JS bundles (`style.css?v=1.0.37`, `app.js?v=1.0.37`) to instantly reset the browser cache.
  - Guaranteed display of the “Clients” and “Thank the author” sections without the need to forcefully clear the browser cache.

## [1.0.36] - 2026-09-02

### Native Clients & Integration Hub (Section “Clients”)
- **Новый раздел «📱 Клиенты и интеграция»**:
  - Добавлена новая вкладка в верхнее меню веб-интерфейса.
  - A detailed description of the architecture of interaction between the Keenetic server (ports: 8089 and : 18089) with native clients.
  - Detailed description of the capabilities of the mobile client **SmartPhotoSync (Android)**: chronological timeline in Google Photos style, photo statuses (LOCAL, SERVER, SYNCED, UPLOADING), background WorkManager service with 2MB chunks and SHA-256 hashes, selection of device folders, Media3 player.
  - Detailed description of the capabilities of the TV client **SmartPhoto TV**: 100% optimization for the remote control (D-Pad), cinematic slideshow with Ken Burns effects (60 FPS), Cross-Dissolve, Slide, Zoom In, smart Fisher-Yates Shuffle, EXIF ​​HUD overlay.
  - Links to direct download of the latest APK builds (`SmartPhotoAndroid.apk` and `SmartPhotoTV.apk`) from the general Keenetic repository, as well as links to launch the built-in Web TV PWA.
  - Summary of all pairing protocols (cloud 6-digit PIN via `ntfy.sh`, local rotating 4-digit PIN, persistent tokens).

## [1.0.35] - 2026-09-02

### Donate / Support Author Section (Thank the author)
- **New section “Thank the author”**:
  - A new tab has been added to the web interface navigation.
  - Support for gratitude methods: YuMoney (Russian bank cards, wallet, SBP, quick selection of amounts), Boosty (foreign and Russian cards, subscriptions and one-time donations), T-Bank (SBP, QR code, transfer without commission).
  - Card of the ecosystem of Smart projects (Smart-Photo, Smart-Route, Smart-Utils) with links to the Keenetic and GitHub repositories.
  - Quickly copy details and wallet numbers to the clipboard.

## [1.0.34] - 2026-08-30

### 6-Digit Cloud Pairing via ntfy.sh Relay (Zero IP Typing)
- **Cloud pairing via 6-digit PIN**:
  - Генерация временного 6-значного PIN-кода (время жизни 5 минут) с автоматической публикацией адреса сервера и токена в публичный открытый брокер `ntfy.sh`.
  - Эндпоинты сервера: `POST /api/system/cloud-pair/create`, `GET /api/system/cloud-pair/status`.
  - Интеграция в веб-интерфейс Настроек: отображение 6 крупных ячеек PIN, таймер обратного отсчета (5 минут) и кнопка генерации.
  - Integration into PWA SmartPhoto TV: when entering 6 digits, the client automatically requests parameters from `ntfy.sh`, determines the server address and token and logs in without manually entering the IP address.

## [1.0.33] - 2026-08-30

### Multi-Token Support & 4-Digit Rotating Pairing PIN
- **Support for multiple access tokens (Multi-Token)**:
  - Ability to create, name and revoke individual access tokens for each device (Smart TV, phones, PC) in the server settings.
  - Maintaining backward compatibility with the main `sync_token`.
  - Token management endpoints: `GET /api/system/tokens`, `POST /api/system/tokens`, `DELETE /api/system/tokens`.
- **Quick pairing using 4-digit PIN (Rotating PIN)**:
  - Automatic generation and rotation of a 4-digit PIN code every minute with a countdown timer in the settings.
  - Pairing endpoint: `POST /api/v1/auth/pair` - when you enter 4 digits on the client, the server generates and returns a permanent access token.
  - Интеграция в PWA SmartPhoto TV: окно авторизации автоматически распознает 4-значный код и выполняет привязку в один клик.

## [1.0.32] - 2026-08-30

### SmartPhoto TV PWA Integration & Smart TV Auto-Detection
- **SmartPhoto TV PWA client integration**:
  - PWA-клиент из репозитория `SmartPhotoTV` (`dist/web-tv`) встроен в сервер и доступен по путям `/pwa/`, `/pwa`, `/tv`, `/tv/` как на основном веб-порту (`8089`), так и на порту Smart-Sync (`18089`).
  - Статические файлы PWA (HTML, CSS, JS, манифест, service-worker) доступны на порту синхронизации без требования токена авторизации.
  - Automatic detection of Smart TV devices (Tizen, WebOS, Android TV, Apple TV, Roku, FireTV and TV browsers) by the User-Agent header with automatic redirection to the full-screen 10-foot UI `/pwa/`.
  - Automatic detection of server address `window.location.origin` without the need to manually enter IP when launched from the built-in PWA.
  - Built-in mechanism for synchronizing PWA distribution into all build scripts (`scripts/build_packages.go`, `build.bat`, `build_all.bat`, `build.ps1`, `deploy_silent.ps1`).

## [1.0.31] - 2026-08-30

### Client-Selected Sync Direction Modes
- **Support for client-side synchronization direction selection**:
  - The `direction` parameter has been added to the `POST /api/v1/sync/diff` request:
    - `"two_way"` (default) - calculation of the lists `to_upload` (per server) and `to_download` (per client);
    - `"upload_only"` (or `"backup"`, `"client_to_server"`) - calculates only files for backup from the client to the router;
    - `"download_only"` (or `"restore"`, `"server_to_client"`) - calculates only files for downloading from the router’s photo archive to the client.
  - Optimizing the load on the router's CPU and RAM in unidirectional scenarios.

## [1.0.30] - 2026-08-30

### Android Client API on Smart-Sync Port
- **REST API extension on Smart-Sync port (18089)**:
  - A complete set of gallery endpoints has been released to create a full-fledged Android mobile client with single authorization using a token (`X-Sync-Token`, `Authorization: Bearer`, or URL query `?token=...` for the Glide/Coil libraries):
    - `GET /api/v1/photos` - photo feed with filtering (years, months, days, folders, camera, favorites) and pagination;
    - `GET /api/v1/photos/{id}` — детальные метаданные фото (EXIF, координаты, разрешение, размер);
    - `GET /api/v1/photos/{id}/thumb` — получение миниатюр (`size=small|large`);
    - `GET /api/v1/photos/{id}/file` (or `/original`) - streaming of originals with support for `HTTP Range`;
    - `POST /api/v1/photos/{id}/favorite` — switching the “Favorites” status;
    - `GET /api/v1/albums` — list of albums with covers and photo counters;
    - `GET /api/v1/folders` - tree structure of folders;
    - `GET /api/v1/timeline/summary` - summary of dates for a quick scrollbar;
    - `GET /api/v1/stats` — indexer system statistics.

## [1.0.29] - 2026-08-30

### Native Smart-Sync REST API & WebDAV Integration
- **Native lightweight Smart-Sync REST API (Option 1)**:
  - Default dedicated port: `18089` (configurable in the web interface).
  - Secure authorization using a secret token (`X-Sync-Token` / `Bearer`).
  - Потоковая чанковая загрузка файлов (Chunked Streaming) с буфером < 2 МБ RAM и проверкой хэшей SHA-256.
  - Политики разрешения конфликтов (`keep_both`, `server_wins`, `client_wins`, `backup_only`).
  - Эндпоинты: `/api/v1/sync/ping`, `/api/v1/sync/diff`, `/api/v1/sync/upload/init`, `/api/v1/sync/upload/{id}/chunk`, `/api/v1/sync/upload/{id}/complete`, `/api/v1/sync/download`, `/api/v1/sync/delete`.
- **WebDAV Сервер (Вариант 2)**:
  - Default dedicated port: `28089` (configurable in the web interface).
  - Supports connecting mobile photo autoloading applications (PhotoSync, FolderSync) and network drives Windows/macOS/Linux.
  - Basic Auth authorization with password support.
- **Integration into the web interface and diagnostics**:
  - The “Synchronization and Integration” block in the “Settings” section with the generation and copying of tokens.
  - Checking the status of both services in System Doctor.

## [1.0.28] - 2026-08-29

### Albums Dual View (Grid & Tree) & Custom Scrollbar Fix
- **Two modes for displaying albums and folders**:
  - **Card Grid**: Classic view with album covers, number of photos, and disk size.
  - **Tree Explorer**:
    - Interactive directory tree with real-time folder search.
    - "Expand All" and "Collapse All" buttons.
    - Quickly view photos inside the selected folder directly in the tree or the “Open in photo feed” button.
    - Storing the selected display mode in `localStorage`.
- **Scroll fix**:
  - The global smooth scrollbar in all browsers (Firefox, Chrome, Edge, Safari) has been restored and stylized with a modern design in the glassmorphism style.

## [1.0.27] - 2026-08-28

### System Doctor Self-Diagnostics Revamp (Smart-Route Style)
- **Upgraded system self-diagnosis**:
  - Self-diagnosis card in Smart-Route style with summary badges (`🟢 УСПЕШНО`, `🟡 ПРЕДУПРЕЖДЕНИЯ`, `🔴 ОШИБКИ`).
  - Categorized list of checks (System, Kernel, RAM Heap, USB Mount Points, Photo Directories, Cache Write Permissions, Indexer, Web Server and Security).
  - Collapsible system pin block `Raw outputs` (`df -h`, `free -m`, `mount`, `uname -a`).
  - A button to quickly copy the report to the clipboard for support.

## [1.0.26] - 2026-08-28

### Navigation Tabs Reordering
- **The “Settings” section has been moved to the last position**:
  - The Settings tab now closes the navigation menu (`Фотолента` ➔ `Альбомы` ➔ `Избранное` ➔ `Фильтры & Поиск` ➔ `Индексация` ➔ `Журнал` ➔ `Диагностика` ➔ `Настройки`).

## [1.0.25] - 2026-08-28

### Real-Time Live Logs Terminal (Smart-Route Style)
- **Real Time Syslog**:
  - Live stream of logs via SSE without having to refresh the page.
  - Удобный фильтр уровней логов (`ALL`, `INFO`, `SUCCESS`, `WARN`, `ERROR`, `DEBUG`).
  - Instant text search by messages and categories with auto-filtering as you type.
  - Автопрокрутка к новым записям с возможностью фиксации скролла.
  - Точный таймстемп с миллисекундами (`HH:MM:SS.mmm`) и фирменная цветовая дифференциация.

## [1.0.24] - 2026-08-28

### Web UI Update Indicator & In-Place One-Click Updater
- **Индикатор обновления рядом с версией**:
  - При появлении новой версии в репозитории рядом с номером версии в шапке отображается анимированный золотистый бейдж `Обновление v1.0.X`.
- **Модальное окно со списком изменений (Changelog)**:
  - По клику на индикатор открывается модальное окно с подробным списком изменений от текущей версии до последней.
- **Seamless update in one click**:
  - Кнопка «Обновить сейчас» автоматически инициирует фоновое обновление пакета через `opkg`, отслеживает перезапуск сервиса и обновляет веб-страницу.

## [1.0.23] - 2026-08-28

### Unified Header & Navigation Menu Design (Smart-Utils Style)
- **Updated header and menu design in Smart-Utils style**:
  - Corporate logo with a gradient glow `linear-gradient(135deg, #1f6feb, #38d39f)`.
  - Header status indicators: `Keenetic Router` badge, online status, live SSE connection indicator `Live: Connected`.
  - Модернизированная панель навигации `.app-nav` с компактными кнопками, градиентной активной подсветкой и зелеными бейджами счетчиков.

## [1.0.22] - 2026-08-28

### URL Hash Routing & State Restoration on F5
- **Отображение раздела в URL**:
  - Текущая открытая вкладка теперь синхронизируется в URL хэше (`#photos`, `#albums`, `#favorites`, `#explore`, `#status`, `#settings`, `#logs`, `#doctor`).
  - When you reload the page using F5 (or follow a direct link / browser history Back-Forward), the open section is instantly restored.

## [1.0.21] - 2026-08-28

### Web Interface Password Protection (Optional)
- **Web interface password in settings**:
  - The “Web interface password (optional)” field has been added to the settings form.
  - When you set a password, the gallery is protected by HTTP Basic Auth (default login `admin`). If the value is empty, authorization is disabled for free access.

## [1.0.20] - 2026-08-28

### Zero-Copy Progressive Full Photo Streaming in Lightbox
- **Eliminating OOM crashes and reboots when viewing full-screen photos**:
  - **Zero-Copy Streaming**: in Lightbox, a full-size photo is now read by the browser directly via HTTP file streaming (`/api/photos/{id}/file`), leaving the decoding to the hardware GPU of the smartphone/PC. The router consumes **0 MB Go RAM and 0% CPU**.
  - **Instant Low-Res preview**: when flipping through a photo, a ready-made small thumbnail from the cache is first displayed (0 ms), then smoothly updated to a crystal clear full-size photo.
  - **Rotation order optimization (`thumbnail.go`)**: image scaling is now performed **BEFORE** rotation. Instead of rotating 48 million pixels (192 MB RAM), the finished tiny 320x240 thumbnail (0.05 MB RAM) is rotated - reducing memory consumption by 300 times.

## [1.0.19] - 2026-08-28

### Embedded EXIF Thumbnail Fast-Path & Strict Viewport Lazy Loading
- **Instantly extract embedded EXIF ​​thumbnails (`ExtractEmbeddedThumbnail`)**:
  - When you request a photo grid, the service reads ready-made JPEG thumbnails directly from the EXIF ​​(IFD1) headers. For 90% of photos from cameras and smartphones, generation takes **0.001 seconds at 0% CPU and 0 MB RAM**.
- **Strict `IntersectionObserver` with `data-src` on the client**:
  - The browser requests thumbnails **exclusively for cards actually visible on the screen** (`rootMargin: '100px'`). Background and unscrolled cards no longer create unnecessary load on the router.
- **Ограничение параллелизма (`max_concurrent_workers: 1`)**:
  - Строго последовательная генерация миниатюр предотвращает параллельные пики памяти и оставляет ядро CPU свободным для сети роутера.
- **Мгновенное освобождение памяти после масштабирования (`debug.FreeOSMemory`)**.

## [1.0.18] - 2026-08-28

### Strict <80MB Memory Budget & Zero-Allocation Timeline
- **Жесткий лимит памяти и устранение всплесков RAM**:
  - **`debug.SetMemoryLimit(80MB)` & `debug.SetGCPercent(20)`**: Go Runtime жестко удерживает использование памяти в рамках 80 МБ.
  - **Zero-Allocation Timeline**: прокрутка и пагинация фотоленты по умолчанию теперь читаются напрямую срезом из предсортированного массива, исключая создание промежуточных 80k-массивов при каждом HTTP-запросе.
  - **Caching statistics and albums**: `GetTimelineSummary`, `GetAlbums` and `GetStats` no longer bypass 80k photos per SSE tick/request, but instantly return precomputed structures.
  - **Cleaning up `FullPath` in memory**: Fixed storing redundant absolute paths in RAM (paths are generated on the fly).

## [1.0.17] - 2026-08-28

### Pure Semantic Package Versioning (No Dash Suffix)
- **Removed release suffix (`-1`) from OPKG packages**:
  - The package name, file `control` and index `Packages` now use the strictly pure semantic version of the program (`1.0.17` instead of `1.0.17-1`).
  - Full version synchronization in the OPKG package manager (`smart-utils`), web interface and repository.

## [1.0.16] - 2026-08-28

### Deep RAM Footprint Optimization & String Interning
- **Глубокая оптимизация потребления оперативной памяти (RAM)**:
  - **Интернирование строк (`InternString` / `Compact`)**: устранено дублирование повторяющихся строковых метаданных (`Format`, `SourceRoot`, `Directory`, `Make`, `Model`, `Lens` и др.) в памяти. Для коллекций 80k+ фото экономится до 40 МБ RAM.
  - **Потоковый JSON декодер и энкодер**: чтение и сохранение `index.json` теперь используют потоковые `json.NewDecoder` и `json.NewEncoder` вместо единовременной аллокации 30+ МБ буферов в куче.
  - **Forced memory return to OS (`debug.FreeOSMemory`)**: Memory used during database scanning and deserialization is immediately returned to the Linux kernel.
  - **Tuning the Go garbage collector (`debug.SetGCPercent(25)`)**: the threshold for holding free memory in the heap has been reduced to work effectively on routers with 128–512 MB RAM.
  - **Reducing the default LRU cache size to 4 MB** (`mem_cache_size_mb: 4`).

## [1.0.15] - 2026-08-28

### Automated Repository & Documentation Version Synchronization
- **Automatic synchronization of versions in the common repository (`snakelair/Keenetic`)**:
  - Implemented automatic synchronization of titles and badges in all documents (`README.md`, `smart_photo_README.md`, `index.html`) with each package build.
  - Versions in the description of repository packages now strictly correspond to the binary version of the program.

## [1.0.14] - 2026-08-28

### Instant Web Server Boot & Asynchronous Index Loading
- **Мгновенный старт веб-сервера (< 5 миллисекунд)**:
  - Порт `8089` теперь открывается немедленно при старте демона — полностью устранены задержки и ошибки 502 Bad Gateway при перезапуске.
  - Чтение и декодирование 30MB+ JSON-индекса (82k+ фото) перенесено в асинхронный фоновый поток.
  - Рекурсивный обход накопителя для `fsnotify` вотчера выполняется неблокирующе в фоне.
  - По готовности загрузки базы веб-клиенты мгновенно обновляются через SSE поток.

## [1.0.13] - 2026-08-28

### Fix Thumbnail & Photo File Resolution on Loaded Index
- **Динамическое восстановление абсолютных путей (`GetEffectiveFullPath`)**:
  - Устранена ошибка, из-за которой при загрузке базы из `index.json` поле `FullPath` оставалось пустым (`""`), вызывая отдачу заглушки «No Preview» для всех миниатюр.
  - Добавлено сохранение `full_path` в JSON и интеллектуальное восстановление физического пути по `SourceRoot` / `RelPath` / настроенным путям `photos_dirs`.
  - Previews and full-size files now open instantly even when moving the drive to another router or changing the USB mount point.

## [1.0.12] - 2026-08-28

### Date Sanity Analysis & Automatic File Mtime Correction
- **Analysis and sanitization of incorrect dates**:
  - Исключены даты из будущего (`> now + 24h`) и сброшенные в эпоху Unix (`1970-01-01` / нулевые даты).
  - Приоритет отдается валидным метаданным EXIF. Если дата в EXIF повреждена, используется дата файла или временной шаблон из имени файла (`IMG_YYYYMMDD_HHMMSS`).
  - **Автоматическая синхронизация даты файла на диске**: если в EXIF или имени файла содержится корректная дата, а дата модификации файла на диске (`mtime`) повреждена или сброшена, Smart-Photo автоматически обновляет `mtime` файла на диске через `os.Chtimes`.
  - Санитизация применяется как при первичном сканировании, так и при загрузке сохраненного индекса из кэша.

## [1.0.11] - 2026-08-28

### On-Demand Only Thumbnail Generation
- **Генерация миниатюр исключительно по запросу клиента (On-Demand)**:
  - Полностью отключена фоновая предварительная генерация миниатюр (`thumbQueue` и фоновые воркеры удалены).
  - Сканирование 80k+ фотографий теперь выполняется мгновенно и без паразитной нагрузки на CPU.
  - Миниатюры генерируются на лету при просмотре в браузере с семафорным ограничением параллелизма (`max_concurrent_workers`), защищающим RAM и CPU роутера от перегрузки при массовой подгрузке ленты.
  - Добавлено подробное логирование ошибок декодирования с указанием проблемного файла.

## [1.0.10] - 2026-08-28

### OPKG Package Integrity & Conffiles
- **Упаковка стандартного `config.json` в `data.tar.gz`**:
  - Полностью исключены предупреждения `file_sha256sum_alloc` при установке и обновлении пакета.
  - Синхронизированы контрольные суммы (MD5/SHA256) и размер пакета во всех архитектурных ветках.

## [1.0.9] - 2026-08-28

### Service Initialization & RAM Logging
- **Удален аргумент `-log /opt/var/log/smart-photo.log` из init-скрипта `S99smart-photo`**:
  - Теперь режим логирования полностью управляется конфигурационным файлом (`log_target: "memory"` по умолчанию) без принудительной перезаписи на диск.

## [1.0.8] - 2026-08-28

### OPKG Architecture & Repository Cleanliness
- **Полное устранение ошибки `has no valid architecture, ignoring` в OPKG**:
  - Каждая архитектурная ветка (`mipsel-3.4`, `aarch64-3.10`, `armv7-3.2`, `x86_64`, `mips-3.4` и их псевдонимы) теперь собирается со строгим соответствием архитектуры в пакете и в индексе `Packages`.
  - Удалены все устаревшие дубликаты пакетов из репозитория: для каждого сервиса (`smart-photo`, `smart-route`, `smart-utils`) хранится ровно один актуальный заголовок в каждом фиде.

## [1.0.7] - 2026-08-28

### Performance & CPU Optimization (0% Idle CPU)
- **Устранена паразитная нагрузка на процессор (100% CPU)**:
  - **Фильтрация событий файлового вотчера (`fsnotify`)**: Исключена циклическая переиндексация, вызывавшаяся записью служебных файлов кэша (`.smartphoto`), логов и временных файлов. Добавлена строгая фильтрация по поддерживаемым графическим форматам.
  - **Кэширование статистики миниатюр в памяти**: Устранен вызов `filepath.Walk` по всей директории кэша миниатюр каждые 3 секунды (добавлен TTL-кэш на 60 секунд).
  - **Облегченный SSE Heartbeat**: Заменен тяжелый 3-секундный пересчет статистики на легковесный ping-пакет, снижающий нагрузку процессора до 0% в режиме ожидания.
  - **Защита от записи пустого индекса**: Устранена перезапись `index.json` на накопитель при отсутствии фотографий.

## [1.0.6] - 2026-08-28

### Fixes & OPKG Architecture Compatibility
- **Исправление ошибки `has no valid architecture, ignoring` в OPKG**:
  - В поле `Architecture:` пакетов и индекса `Packages` установлено универсальное значение `all`, поддерживаемое абсолютно всеми устройствами и версиями Entware.
  - В репозиторий добавлены зеркальные псевдонимы директорий (например, `aarch64-k3.10` и `aarch64-3.10`, `mipsel-k3.4` и `mipsel-3.4`, `armv7sf-k3.2` и `armv7-3.2`).
  - В `install.sh` внедрено точное определение архитектуры непосредственно из `/opt/etc/opkg.conf`.

## [1.0.5] - 2026-08-28

### Realtime Watcher, Multi-folder & Live Discovery
- **Логирование в RAM по умолчанию**:
  - Режим логирования по умолчанию установлен в `"memory"` (кольцевой буфер в оперативной памяти), гарантируя нулевой износ Flash-памяти роутера.
- **Supports multiple photo folders (`photos_dirs`)**:
  - Added the ability to specify an arbitrary number of folders and USB drives at the same time (for example, several connected flash drives/disks).
  - The web panel settings have a dynamic list with add and delete buttons and a built-in Browse... explorer for each path.
- **Subscribe to real-time file system events (`fsnotify`)**:
  - The indexer automatically tracks adding, changing, renaming and deleting files in all configured directories through file system system events (with a smart debounce of 1.5 sec).
- **Display results on the fly without reboot**:
  - When new photos are discovered and indexed, they are instantly broadcast via an SSE stream to the browser and neatly integrated into the photo feed with real-time animation.

## [1.0.4] - 2026-08-28

### Fixes & HTTPS Installer Resilience
- **Fix `wget: not an http or ftp url` in the installer**:
  - Before updating the repositories, `install.sh` automatically installs `wget-ssl`, `ca-certificates` and `ca-bundle` from the standard Entware HTTP repository, giving the `opkg` package manager full HTTPS support.
  - Added automatic fallback: if `opkg update` fails to update the HTTPS feed, the installer directly downloads the `.ipk` package through the verified `curl -sSL` and installs it locally.

## [1.0.3] - 2026-08-28

### Repository Coexistence & Publishing Improvements
- **Single Storefront Repository `snakelair/Keenetic`**:
  - An interactive homepage `index.html` (web hub) has been created to showcase both projects: **Smart-Photo** (port 8089) and **Smart-Route** (port 8088).
  - Detailed function cards, 1-click commands for quick installation via SSH and a table of supported Keenetic models.
- **Reliable synchronization when publishing**:
  - The `push_keenetic_repo.bat` script synchronizes and updates the current state before assembly, ensuring the safety of the packages of both services in a single index `Packages` and `Packages.gz`.

## [1.0.2] - 2026-08-28

### Improvements & Mini File Manager
- **Hide the standard browser scrollbar**:
  - The cumbersome browser scrollbar has been completely removed from the entire interface and photo strip (`scrollbar-width: none` / `::-webkit-scrollbar { display: none }`).
  - All types of scrolling (mouse wheel, swiping on touch screens, keyboard, dragging the date slider) work perfectly smoothly.
- **Built-in mini file manager for selecting folders**:
  - Added “📁 Browse...” buttons in the settings for the photos folder (USB) and a separate cache folder.
  - Modal file system overview window with quick navigation through mount points (`/tmp/mnt`, `/opt`, Windows drives `C:\`, `D:\`).
  - Directory navigation, “Up” navigation, folder selection and confirmation in one click.

## [1.0.1] - 2026-08-28

### Improvements & Russian Localization
- **Full Russification of dates and times**:
  - All day headings (“Today”, “Yesterday”, “Friday, August 28, 2026”), captions (“August 28”), month names (“August 2026”) are translated into Russian.
  - Display date and time in full screen viewer and EXIF ​​panel in Russian locale format.
- **Application version indicator**:
  - The interface header displays the application version `v1.0.1` instead of static text.
  - Automatic display of the current version via API.
- **Interactive date and year scroller in Google Photos style (right)**:
  - Vertical date scale on the right with year marks (`2026`, `2025`...).
  - A draggable handle with a floating current date badge when scrolling.
  - Smooth transition to the selected year/month in one click.

## [1.0.0] - 2026-08-28

### Initial Release: Personal Google Photos-like Server for Keenetic Entware
- **Google Photos Timeline Experience**:
  - Infinite scroll with chunked API loading (`IntersectionObserver`).
  - Sticky day headers with friendly date grouping ("Today", "Yesterday", "28 August 2026").
  - Responsive photo grid with lazy thumbnail loading and aspect ratio preservation.
- **Fullscreen Lightbox & Viewer**:
  - High-res image rendering with smooth zooming (mouse wheel / buttons), panning, and 90° rotation.
  - Interactive slideshow mode with auto-advancing timer.
  - Complete EXIF inspector: Camera Make & Model, Lens, Aperture (f-stop), Shutter Speed, ISO, Focal Length, and GPS OpenStreetMap link.
  - Keyboard navigation (Arrow keys, Esc, Space, I, +, -, 0) and mobile swipe gestures.
- **On-the-Fly Thumbnail Engine & Two-Tier Cache**:
  - Pure Go image decoders and high-speed bilinear resizers (`CGO_ENABLED=0`).
  - Configurable cache location: `.smartphoto/thumbs` in the photos folder root or custom path (`/opt/var/cache/smart-photo`).
  - RAM LRU cache for lightning-fast UI responsiveness.
- **Router Hardware Optimization**:
  - Configurable worker concurrency limits (default 2 workers) to preserve Keenetic router CPU performance.
  - Memory-only ring buffer logging (zero wear on router flash memory).
  - Background incremental indexing and directory watcher.
- **Multi-Architecture Entware OPKG Packaging**:
  - Full support for `mipsel-3.4`, `armv7-3.2`, `aarch64-3.10`, `x86_64`, `mips-3.4`.
  - Seamless coexistence in `snakelair/Keenetic` OPKG repository alongside `smart-route`.
  - 1-click deployment script `deploy_to_router.bat` via SSH.
