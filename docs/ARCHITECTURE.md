# SMERKA service and desktop shell

## Scope
This branch starts a fresh, modular implementation in the existing `Thesmilingface/Omni-1.0` repository. The Python service is local-only (127.0.0.1), stores chat turns in SQLite, and supports Groq/OpenAI-compatible chat endpoints and Gemini REST. The Rust client is a native egui application with a procedural 2D face and chat panel.

## Acceptance status
This is a foundation, not completion of the full product specification. The desktop currently shows the companion inside the main window; it is not a transparent always-on-top companion window. No Live2D SDK/model is included. Voice capture, transcription, TTS/audio playback synchronization, streaming, web search, Java integration, installer, and packaged ZIP are not implemented. See KNOWN_LIMITATIONS.
