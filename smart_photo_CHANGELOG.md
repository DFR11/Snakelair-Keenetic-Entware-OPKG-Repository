# 📦 Smart-Photo Changelog

## [1.0.40] - 2026-09-04

### Community links & discussion integration
- **Integration of official community and discussion links**:
  - Quick, neat pill buttons were added to the header of the web panel: **Telegram** (`t.me/KeeneticSmartPhoto`) and **Keenetic Forum** (official discussion thread).
  - An interactive feedback block for Android mobile app and TV client users was added to the **Clients and Integration** section.
  - Direct buttons to the Telegram channel and forum topic were added to the **Thank the author** section.
  - Links to release discussions were added to the version history and self-update modal window.

## [1.0.39] - 2026-09-03

### Clean OPKG installation & unified API status
- **Eliminated duplicate information during OPKG installation**:
  - `package/entware/control/postinst` was switched to quiet background launch (detached graceful restart) without showing stale banners with empty IPs.
  - Added `GET /api/status` system endpoint returning `status`, `version`, `router_model`, and `web_port`.
  - The router model (`router_model`) is now detected correctly from `/tmp/sysinfo/model`, Device Tree, and `ndmc`.
  - The `install.sh` script now includes port occupancy checks and startup timeout diagnostics.
  - Installation completion output was fully aligned with **Smart-Utils**.

## [1.0.38] - 2026-09-02

### Self-update system (Smart-Utils style)
- **Interactive self-update system in Smart-Utils style**:
  - Clickable version badge in the header (`#appVersionBadge`) to view the changelog at any time.
  - Pulsating new-version indicator (`.update-pulse-badge`, `.update-pulse-dot`) next to the version number when an update is available.
  - Update modal window with version comparison banner (Current → Available), a formatted list of changes, and an instant update button.
  - Built-in live installation console and automatic service restart polling with page reload.
  - Fixed closing behavior for the folder selection modal (`folderPickerModal`).

## [1.0.37] - 2026-09-02

### OPKG repository release & cache busting
- **Official release of OPKG in the Keenetic repository (`snakelair/Keenetic`)**:
  - Built packages for all architectures (`mipsel-3.4`, `armv7-3.2`, `aarch64-3.10`, `x86_64`, `mips-3.4`).
  - Added versioned query parameters to CSS and JS bundles (`style.css?v=1.0.37`, `app.js?v=1.0.37`) to instantly reset browser cache.
  - Guaranteed display of the “Clients” and “Thank the author” sections without forcing a browser cache refresh.

## [1.0.36] - 2026-09-02

### Native clients & integration hub (section “Clients”)
- **New section “📱 Clients and Integration”**:
  - Added a new tab to the top menu of the web interface.
  - Detailed description of the architecture of interaction between the Keenetic server (ports: 8089 and :18089) and native clients.
  - Detailed description of the capabilities of the mobile client **SmartPhotoSync (Android)**: chronological timeline in Google Photos style, photo statuses (LOCAL, SERVER, SYNCED, UPLOADING), background upload queue, and direct gallery synchronization.
  - Detailed description of the capabilities of the TV client **SmartPhoto TV**: 100% optimization for the remote control (D-Pad), cinematic slideshow with Ken Burns effects (60 FPS), cross-device synchronization, and full-screen playback.
  - Links to direct download of the latest APK builds (`SmartPhotoAndroid.apk` and `SmartPhotoTV.apk`) from the shared Keenetic repository, as well as links to launch the built-in Web TV PWA.
  - Summary of all pairing protocols (cloud 6-digit PIN via `ntfy.sh`, local rotating 4-digit PIN, persistent tokens).

## [1.0.35] - 2026-09-02

### Donate / support author section (Thank the author)
- **New section “Thank the author”**:
  - A new tab was added to the web interface navigation.
  - Support for gratitude methods: YuMoney (Russian bank cards, wallet, SBP, quick amounts), Boosty (foreign and Russian cards, subscriptions and one-time donations), T-Bank (SBP, QR codes).
  - Card of the Smart ecosystem (Smart-Photo, Smart-Route, Smart-Utils) with links to the Keenetic and GitHub repositories.
  - Quick copy of wallet details and account numbers to the clipboard.

## [1.0.34] - 2026-08-30

### 6-digit cloud pairing via ntfy.sh relay (zero typing)
- **Cloud pairing via 6-digit PIN**:
  - Generation of a temporary 6-digit PIN code (5-minute lifetime) with automatic publication of the server address.
  - Server endpoints: `POST /api/system/cloud-pair/create`, `GET /api/system/cloud-pair/status`.
  - Integration into the Settings web UI: display of 6 large PIN cells, countdown timer (5 minutes), and secure pairing flow.
  - Integration into the SmartPhoto TV PWA: when entering the 6 digits, the client automatically requests parameters from `ntfy.sh`, determines the server address and token, and logs in without manual entry.

## [1.0.33] - 2026-08-30

### Multi-token support & 4-digit rotating pairing PIN
- **Support for multiple access tokens (Multi-Token)**:
  - Ability to create, name, and revoke individual access tokens for each device (Smart TV, phones, PC) in the server settings.
  - Maintaining backward compatibility with the main `sync_token`.
  - Token management endpoints: `GET /api/system/tokens`, `POST /api/system/tokens`, `DELETE /api/system/tokens`.
- **Quick pairing using a 4-digit PIN (Rotating PIN)**:
  - Automatic generation and rotation of a 4-digit PIN code every minute with a countdown timer in the settings.
  - Pairing endpoint: `POST /api/v1/auth/pair` — when the user enters 4 digits on the client, the server generates and returns a permanent access token.
  - Integration into the SmartPhoto TV PWA: the authorization window automatically recognizes the 4-digit code and binds the device without a manual entry step.

## [1.0.32] - 2026-08-30

### SmartPhoto TV PWA integration & Smart TV auto-detection
- **SmartPhoto TV PWA client integration**:
  - PWA client from the `SmartPhotoTV` repository (`dist/web-tv`) is embedded in the server and available under `/pwa/`, `/pwa`, `/tv`, `/tv/` on the base domain.
  - Static PWA files (HTML, CSS, JS, manifest, service worker) are accessible on the synchronization port without requiring a token.
  - Automatic detection of Smart TV devices (Tizen, WebOS, Android TV, Apple TV, Roku, FireTV, and TV browsers) by User-Agent, with automatic redirection to the full-screen 10-foot UI at `/pwa`.
  - Automatic detection of the server address using `window.location.origin` without manually entering the IP when launched from the embedded PWA.
  - Built-in synchronization mechanism for PWA distribution across all build scripts (`scripts/build_packages.go`, `build.bat`, `build_all.bat`, `build.ps1`, `deploy_silent.ps1`).

## [1.0.31] - 2026-08-30

### Client-selected sync direction modes
- **Support for client-side synchronization direction selection**:
  - The `direction` parameter was added to the `POST /api/v1/sync/diff` request:
    - `"two_way"` (default) — calculates lists `to_upload` (server) and `to_download` (client);
    - `"upload_only"` (or `"backup"`, `"client_to_server"`) — calculates only backup from the client to the router;
    - `"download_only"` (or `"restore"`, `"server_to_client"`) — calculates only downloads from the router photo archive to the client.
  - Improved CPU and RAM load for unidirectional scenarios.

## [1.0.30] - 2026-08-30

### Android client API on the Smart-Sync port
- **REST API extension on Smart-Sync port (18089)**:
  - A complete gallery endpoint set was released for building a full Android mobile client with single sign-on via token (`X-Sync-Token`, `Authorization: Bearer`, or URL query token).
    - `GET /api/v1/photos` — photo feed with filtering (years, months, days, folders, camera, favorites) and pagination;
    - `GET /api/v1/photos/{id}` — detailed photo metadata (EXIF, coordinates, resolution, size);
    - `GET /api/v1/photos/{id}/thumb` — thumbnail retrieval (`size=small|large`);
    - `GET /api/v1/photos/{id}/file` (or `/original`) — original streaming with HTTP Range support;
    - `POST /api/v1/photos/{id}/favorite` — toggle the Favorite status;
    - `GET /api/v1/albums` — list of albums with cover art and photo counts;
    - `GET /api/v1/folders` — folder tree structure;
    - `GET /api/v1/timeline/summary` — summary of dates for quick scrollbar navigation;
    - `GET /api/v1/stats` — indexer statistics.

## [1.0.29] - 2026-08-30

### Native Smart-Sync REST API & WebDAV integration
- **Native lightweight Smart-Sync REST API (Option 1)**:
  - Default dedicated port: `18089` (configurable in the web interface).
  - Secure authorization using a secret token (`X-Sync-Token` / `Bearer`).
  - Streaming chunked uploads with a < 2 MB RAM buffer and SHA-256 hash verification.
  - Conflict resolution policies (`keep_both`, `server_wins`, `client_wins`, `backup_only`).
  - Endpoints: `/api/v1/sync/ping`, `/api/v1/sync/diff`, `/api/v1/sync/upload/init`, `/api/v1/sync/upload/{id}/chunk`, `/api/v1/sync/upload/{id}/complete`, `/api/v1/sync/download`, `/api/v1/sync/...`.
- **WebDAV server (Option 2)**:
  - Default dedicated port: `28089` (configurable in the web interface).
  - Supports mobile photo auto-upload apps (PhotoSync, FolderSync) and network drives (Windows/macOS/Linux).
  - Basic Auth authorization with password support.
- **Integration into the web interface and diagnostics**:
  - The “Synchronization and Integration” block in the Settings section with generation and copying of tokens.
  - Checking status of both services in System Doctor.

## [1.0.28] - 2026-08-29

### Albums dual view (grid & tree) & custom scrollbar fix
- **Two display modes for albums and folders**:
  - **Card Grid**: classic card view with album covers, photo counts, and disk size.
  - **Tree Explorer**:
    - Interactive directory tree with real-time folder search.
    - “Expand All” and “Collapse All” buttons.
    - Quick preview of selected folders directly in the tree or via “Open in photo feed”.
    - Selected display mode stored in `localStorage`.
- **Scroll fix**:
  - The global smooth scrollbar in all browsers (Firefox, Chrome, Edge, Safari) was restored and restyled with a modern glassmorphism design.

## [1.0.27] - 2026-08-28

### System Doctor self-diagnostics revamp (Smart-Route style)
- **Upgraded system self-diagnosis**:
  - Self-diagnosis card in Smart-Route style with summary badges (`🟢 SUCCESS`, `🟡 WARNINGS`, `🔴 ERRORS`).
  - Categorized list of checks (System, Kernel, RAM Heap, USB Mount Points, Photo Directories, Cache Write Permissions, Indexer, Web Server, Security).
  - Collapsible raw output block (`df -h`, `free -m`, `mount`, `uname -a`).
  - Button to quickly copy the report to the clipboard for support.

## [1.0.26] - 2026-08-28

### Navigation tabs reordered
- **The “Settings” section moved to the last position**:
  - The Settings tab now closes the navigation menu in the order `Photo feed → Albums → Favorites → Filters & Search → Indexing → Logs → Settings`.

## [1.0.25] - 2026-08-28

### Real-time live logs terminal (Smart-Route style)
- **Real Time Syslog**:
  - Live log stream via SSE without page refresh.
  - Convenient log-level filter (`ALL`, `INFO`, `SUCCESS`, `WARN`, `ERROR`, `DEBUG`).
  - Instant text search with auto-filtering as you type.
  - Auto-scroll to new entries with the option to lock the scroll position.
  - Accurate timestamps with milliseconds and branded color differentiation.

## [1.0.24] - 2026-08-28

### Web UI update indicator & in-place one-click updater
- **Update indicator next to the version**:
  - When a new version appears in the repository, an animated pulsing badge appears near the version number in the header.
- **Changelog modal window**:
  - Clicking the indicator opens a modal with a detailed list of changes from the current version to the available one.
- **Seamless one-click update**:
  - The “Update now” button automatically triggers a background OPKG package update, tracks the installation progress, and reloads the page when finished.

## [1.0.23] - 2026-08-28

### Unified header & navigation menu design (Smart-Utils style)
- **Updated header and menu design in Smart-Utils style**:
  - Corporate logo with gradient glow `linear-gradient(135deg, #1f6feb, #38d39f)`.
  - Header status indicators: `Keenetic Router` badge, online status, live SSE connection indicator `Live: Connected`.
  - Modernized navigation bar `.app-nav` with compact buttons, gradient active highlight, and a smooth glass effect.

## [1.0.22] - 2026-08-28

### URL hash routing & state restoration on F5
- **Displaying the open section in the URL**:
  - The current tab is synchronized with the URL hash (`#photos`, `#albums`, `#favorites`, `#explore`, `#status`, `#settings`).
  - Reloading the page with F5 or following a direct link restores the state instantly.

## [1.0.21] - 2026-08-28

### Web interface password protection (optional)
- **Web interface password in settings**:
  - The “Web interface password (optional)” field was added to the settings form.
