# LiveKit Filler Handler Plugin

A Python plugin for LiveKit Agents that adds robust interruption handling, filtering out common filler sounds ("uh", "umm", "haan", "hmm", etc) using a configurable word list/environment variable. Compatible with multi-language and real-time agent extension layers.

## Features
- Ignores filler interruptions while agent is speaking
- Registers same words as valid speech when agent is quiet
- Configurable list of ignored words and confidence threshold
- Easy to integrate in LiveKit event loop (no changes to base SDK)
- Logging for debugging false/valid interruptions
- Multi-language: English + Hindi fillers by default, easily extendable

## Requirements
- Python 3.9+
- [livekit-agents](https://pypi.org/project/livekit-agents/) >=1.0.0
- API keys for: LiveKit Cloud, OpenAI, Deepgram, ElevenLabs (see `.env`)

## Installation

pip install -e .

## Configuration
Set environment variables (in your .env, never publicly!):
LIVEKIT_URL=Your-LiveKit-URL
LIVEKIT_API_KEY=Your-LiveKit-API-Key
LIVEKIT_API_SECRET=Your-LiveKit-API-Secret
OPENAI_API_KEY=Your-OpenAI-Key
DEEPGRAM_API_KEY=Your-Deepgram-Key
ELEVEN_API_KEY=Your-ElevenLabs-Key
FILLER_WORDS=uh,um,umm,hmm,haan,ah,er
FILLER_CONFIDENCE_THRESHOLD=0.65
FILLER_MIN_WORD_LENGTH=2

## Usage Example
Import and use in your agent handler:
from livekit.plugins.filler_handler import FillerWordFilter, FillerConfig

filler_filter = FillerWordFilter(
ignored_words=FillerConfig.get_filler_words(),
confidence_threshold=FillerConfig.get_confidence_threshold(),
min_word_length=FillerConfig.get_min_word_length()
)
See `examples/filler_agent_demo.py` for integration in an agent session.

## License
Apache-2.0
