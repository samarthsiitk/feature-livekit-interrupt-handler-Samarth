# simple_filler_agent.py

import asyncio
import logging
from typing import Set
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, deepgram, silero, elevenlabs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === INLINE FILTER CLASS (No separate plugin needed) ===
class SimpleFillerFilter:
    def __init__(self, ignored_words: list[str]):
        self.ignored_words: Set[str] = set(w.lower() for w in ignored_words)
        self.agent_speaking = False
    
    def should_allow(self, text: str, confidence: float = 1.0) -> bool:
        # Agent not speaking? Always allow
        if not self.agent_speaking:
            return True
        
        # Low confidence? Block
        if confidence < 0.65:
            logger.info(f"❌ BLOCKED (low conf): '{text}'")
            return False
        
        # Check if only fillers
        words = text.lower().split()
        non_fillers = [w for w in words if w not in self.ignored_words]
        
        if len(non_fillers) == 0:
            logger.info(f"❌ BLOCKED (filler only): '{text}'")
            return False
        
        logger.info(f"✅ ALLOWED: '{text}'")
        return True


# Global filter
filler_filter = SimpleFillerFilter([
    'uh', 'um', 'umm', 'hmm', 'haan', 'ah', 'mm'
])


async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    agent = Agent(instructions="You are a helpful assistant.")
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=elevenlabs.TTS(),
    )
    
    @session.on("agent_state_changed")
    def on_agent_state(event):
        if event.new_state == "speaking":
            filler_filter.agent_speaking = True
        else:
            filler_filter.agent_speaking = False
    
    @session.on("user_speech_committed")
    def on_user_speech(event):
        if not filler_filter.should_allow(event.transcript):
            # Block this interruption
            pass  # Implement blocking logic based on API
    
    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="Greet the user")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

