from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, google, silero, cartesia  # Added cartesia
from livekit.plugins.filler_handler import FillerWordFilter, FillerConfig

load_dotenv()

class MyAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a friendly voice assistant.")

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    agent = MyAgent()
    
    filler_filter = FillerWordFilter(
        ignored_words=FillerConfig.get_filler_words(),
        confidence_threshold=FillerConfig.get_confidence_threshold(),
        min_word_length=FillerConfig.get_min_word_length()
    )
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=cartesia.TTS(),  # Simple, no complex auth needed
        allow_interruptions=True,
        min_interruption_words=2,
    )
    
    @session.on("agent_state_changed")
    def on_agent_state(event):
        is_speaking = (event.new_state == "speaking")
        filler_filter.set_agent_speaking_state(is_speaking)
        if is_speaking:
            print(f"🎙️ Agent started speaking")
        else:
            print(f"👂 Agent stopped speaking (state: {event.new_state})")
    
    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="Greet the user and offer assistance.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))