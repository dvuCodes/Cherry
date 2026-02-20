# Changelog

All notable changes to Voicebox will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-25

### Added

#### Core Features
- **Voice Cloning** - Clone voices from audio samples using Qwen3-TTS (1.7B and 0.6B models)
- **Voice Profile Management** - Create, edit, and organize voice profiles with multiple samples
- **Speech Generation** - Generate high-quality speech from text using cloned voices
- **Generation History** - Track all generations with search and filtering capabilities
- **Audio Transcription** - Automatic transcription powered by Whisper
- **In-App Recording** - Record audio samples directly in the app with waveform visualization

#### Desktop App
- **Tauri Desktop App** - Native desktop application for macOS, Windows, and Linux
- **Local Server Mode** - Embedded Python server runs automatically
- **Remote Server Mode** - Connect to a remote Voicebox server on your network
- **Auto-Updates** - Automatic update notifications and installation

#### API
- **REST API** - Full REST API for voice synthesis and profile management
- **OpenAPI Documentation** - Interactive API docs at `/docs` endpoint
- **Type-Safe Client** - Auto-generated TypeScript client from OpenAPI schema

#### Technical
- **Voice Prompt Caching** - Fast regeneration with cached voice prompts
- **Multi-Sample Support** - Combine multiple audio samples for better voice quality
- **GPU/CPU/MPS Support** - Automatic device detection and optimization
- **Model Management** - Lazy loading and VRAM management
- **SQLite Database** - Local data persistence

### Technical Details

- Built with Tauri v2 (Rust + React)
- FastAPI backend with async Python
- TypeScript frontend with React Query and Zustand
- Qwen3-TTS for voice cloning
- Whisper for transcription

### Platform Support

- macOS (Apple Silicon and Intel)
- Windows
- Linux (AppImage)

---

## [Unreleased]

### Security
- Require a configured API token for remote backend bindings and reject unauthenticated remote requests.
- Tighten backend CORS defaults to explicit local origins and remove credentialed wildcard behavior.
- Harden Tauri production security with explicit CSP, disabled webview devtools, and reduced shell/fs permissions.

### Added
- Add backend security configuration support for API token, allowed CORS origins, docs exposure, and upload size limits.
- Add bounded upload helpers that enforce maximum file sizes during stream reads.
- Add backend tests for auth token parsing/validation and upload size limit enforcement.
- Add API token field in server connection settings for secured remote backends.
- **Makefile** - Comprehensive development workflow automation with commands for setup, development, building, testing, and code quality checks.
  Includes Python version detection warnings, self-documenting help output, and parallel dev server support.

### Changed
- Send API tokens across REST, media, and SSE requests for remote secured mode.
- Hide backend OpenAPI docs by default outside development unless explicitly enabled.
- Return sanitized 500 responses while logging full server-side exceptions for diagnostics.
- **README** - Add Makefile-based quick start guidance alongside manual setup instructions.

### Removed
- Remove duplicate legacy updater hook module in favor of a single maintained implementation.
- Remove unnecessary Tauri shell execute/spawn and filesystem read-all capabilities.

### Fixed
- Audio export failing when Tauri save dialog returns object instead of string path
- Preserve intended `/generate` and `/transcribe` HTTP statuses (including 202/404) instead of collapsing them to 500.
- Fix updater auto-check dependency handling in `useAutoUpdater`.
- Fix backend progress test imports to use package-qualified module paths.

---

## [Unreleased - Planned]

### Planned
- Real-time streaming synthesis
- Conversation mode with multiple speakers
- Voice effects (pitch shift, reverb, M3GAN-style)
- Timeline-based audio editor
- Additional voice models (XTTS, Bark)
- Voice design from text descriptions
- Project system for saving sessions
- Plugin architecture

---

[0.1.0]: https://github.com/jamiepine/voicebox/releases/tag/v0.1.0
