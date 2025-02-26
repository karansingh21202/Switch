# import os
# from fastapi import FastAPI, BackgroundTasks
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from groq import Groq
# from RealtimeTTS import TextToAudioStream, EdgeEngine

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create and mount a static directory to serve audio files
# os.makedirs("static", exist_ok=True)
# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")

# GROQ_API_KEY = "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"
# groq_client = Groq(api_key=GROQ_API_KEY)

# engine = EdgeEngine()
# engine.set_voice("en-GB-RyanNeural")
# engine.rate = 10
# engine.pitch = -26
# stream = TextToAudioStream(engine)

# # Global variables to track interview stage and candidate topic.
# # stage can be "initial", "awaiting_topic", or "interviewing"
# stage = "initial"
# candidate_topic = None
# # We'll build conversation_history once the candidate topic is set.
# conversation_history = []

# # Global variable for our audio file path.
# CURRENT_AUDIO_FILE = "static/response.mp3"

# class QueryRequest(BaseModel):
#     text: str
#     stop_audio: bool = False

# @app.get("/stop_audio")
# async def stop_audio():
#     # Stop any ongoing audio generation in the TTS stream.
#     stream.stop()  # Ensure your TTS engine's stop() works correctly.
#     return {"status": "Audio stopped"}

# def generate_speech_async(text: str):
#     """
#     Background task that feeds text to the TTS engine,
#     generates the audio and saves it to CURRENT_AUDIO_FILE.
#     Adjust this method to your TTS engine's API.
#     """
#     stream.feed(text)
#     # Replace stream.play() with your actual TTS function that returns binary audio data.
#     audio_data = stream.play()
#     with open(CURRENT_AUDIO_FILE, "wb") as f:
#         f.write(audio_data)

# @app.post("/query")
# async def query(request: QueryRequest, background_tasks: BackgroundTasks):
#     global stage, candidate_topic, conversation_history
#     # Stop any current audio before processing a new request.
#     await stop_audio()

#     user_query = request.text.strip()

#     try:
#         # Stage 1: Initial – Always ask "What are you pursuing?" regardless of user input.
#         if stage == "initial":
#             stage = "awaiting_topic"
#             response_text = "What are you pursuing?"
#             # (Optionally, you could log the user_query somewhere if needed.)
#             background_tasks.add_task(generate_speech_async, response_text)
#             return {"response": response_text}

#         # Stage 2: Awaiting candidate's field response.
#         elif stage == "awaiting_topic":
#             candidate_topic = user_query
#             # Update the system prompt based on the candidate's field.
#             system_prompt = (
#                 f"You are an interviewer at a software company. "
#                 f"The candidate is preparing for an interview in {candidate_topic}. "
#                 f"Ask the candidate 5 short, unique technical questions related to {candidate_topic}. "
#                 f"After each question, wait for the candidate's answer before asking the next question. "
#                 f"Keep each question and response very brief, crisp, and to the point. "
#                 f"At the end, evaluate the candidate's answers and give clear, constructive feedback. "
#                 f"Keep your language plain and natural, without bullet points, asterisks, or any special characters. "
#                 f"Speak as naturally as possible so that the converted speech sounds human. "
#                 f"Avoid repeating the same questions in different sessions. Always vary the questions."
#             )
#             # Initialize conversation history with the new system prompt.
#             conversation_history = [{"role": "system", "content": system_prompt}]
#             # Generate the first interview question.
#             chat_completion = groq_client.chat.completions.create(
#                 messages=conversation_history,
#                 model="llama-3.3-70b-versatile",
#             )
#             response_text = chat_completion.choices[0].message.content.strip()
#             conversation_history.append({"role": "assistant", "content": response_text})
#             stage = "interviewing"
#             background_tasks.add_task(generate_speech_async, response_text)
#             return {"response": response_text}

#         # Stage 3: Interviewing – Continue the conversation.
#         elif stage == "interviewing":
#             conversation_history.append({"role": "user", "content": user_query})
#             chat_completion = groq_client.chat.completions.create(
#                 messages=conversation_history,
#                 model="llama-3.3-70b-versatile",
#             )
#             response_text = chat_completion.choices[0].message.content.strip()
#             conversation_history.append({"role": "assistant", "content": response_text})
#             background_tasks.add_task(generate_speech_async, response_text)
#             return {"response": response_text}

#         else:
#             # Fallback for unexpected stage.
#             return {"response": "Unexpected conversation state."}

#     except Exception as e:
#         return {"response": f"Error: {str(e)}"}

# # Endpoint to serve the generated audio file.
# @app.get("/response.mp3")
# async def get_audio():
#     if os.path.exists(CURRENT_AUDIO_FILE):
#         return FileResponse(CURRENT_AUDIO_FILE, media_type="audio/mpeg")
#     else:
#         return {"error": "Audio file not found"}, 404

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


import os
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from RealtimeTTS import TextToAudioStream, EdgeEngine
import os
from dotenv import load_dotenv
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create and mount a static directory to serve audio files
os.makedirs("static", exist_ok=True)
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Groq and TTS engine
GROQ_API_KEY= os.getenv("GROQ_API_KEY_3")

groq_client = Groq(api_key=GROQ_API_KEY)

engine = EdgeEngine()
engine.set_voice("en-GB-RyanNeural")
engine.rate = 10
engine.pitch = -26
stream = TextToAudioStream(engine)

# Global conversation state (for a single session; adjust for multi-user)
stage = "initial"  # can be "initial", "awaiting_topic", or "interviewing"
candidate_topic = None
conversation_history = []

# Global variable for our audio file path.
CURRENT_AUDIO_FILE = "static/response.mp3"

class QueryRequest(BaseModel):
    text: str
    stop_audio: bool = False

def stop_current_audio():
    """Helper to stop any ongoing TTS generation."""
    try:
        stream.stop()  # Stop ongoing audio generation
        logger.info("Audio stopped successfully.")
    except Exception as e:
        logger.error(f"Error stopping audio: {e}")

@app.get("/stop_audio")
async def stop_audio():
    stop_current_audio()
    return {"status": "Audio stopped"}

def generate_speech_async(text: str):
    """
    Background task that feeds text to the TTS engine,
    generates the audio, and saves it to CURRENT_AUDIO_FILE.
    """
    try:
        logger.info(f"Generating speech for text: {text}")
        stream.feed(text)
        # Generate audio (this call should return binary audio data)
        audio_data = stream.play()  # blocking call; adjust if asynchronous
        with open(CURRENT_AUDIO_FILE, "wb") as f:
            f.write(audio_data)
        logger.info("Audio file generated successfully.")
    except Exception as e:
        logger.error(f"Error in TTS generation: {e}")

@app.post("/query")
async def query(request: QueryRequest, background_tasks: BackgroundTasks):
    global stage, candidate_topic, conversation_history

    # Stop any ongoing audio before processing the new request.
    stop_current_audio()

    user_query = request.text.strip()
    logger.info(f"Received query: {user_query} | Current stage: {stage}")

    try:
        if stage == "initial":
            stage = "awaiting_topic"
            response_text = "What are you pursuing?"
            background_tasks.add_task(generate_speech_async, response_text)
            return {"response": response_text}

        elif stage == "awaiting_topic":
            candidate_topic = user_query
            system_prompt = (
                f"You are an interviewer at a software company. "
                f"The candidate is preparing for an interview in {candidate_topic}. "
                f"Ask the candidate 5 short, unique technical questions related to {candidate_topic}. "
                f"After each question, wait for the candidate's answer before asking the next question. "
                f"Keep each question and response very brief, crisp, and to the point. "
                f"At the end, evaluate the candidate's answers and give clear, constructive feedback. "
                f"Keep your language plain and natural, without bullet points, asterisks, or any special characters. "
                f"Speak as naturally as possible so that the converted speech sounds human. "
                f"Avoid repeating the same questions in different sessions. Always vary the questions."
            )
            conversation_history = [{"role": "system", "content": system_prompt}]
            chat_completion = groq_client.chat.completions.create(
                messages=conversation_history,
                model="llama-3.3-70b-versatile",
            )
            response_text = chat_completion.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": response_text})
            stage = "interviewing"
            background_tasks.add_task(generate_speech_async, response_text)
            return {"response": response_text}

        elif stage == "interviewing":
            conversation_history.append({"role": "user", "content": user_query})
            chat_completion = groq_client.chat.completions.create(
                messages=conversation_history,
                model="llama-3.3-70b-versatile",
            )
            response_text = chat_completion.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": response_text})
            background_tasks.add_task(generate_speech_async, response_text)
            return {"response": response_text}

        else:
            raise HTTPException(status_code=400, detail="Unexpected conversation state.")
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return {"response": f"Error: {str(e)}"}

@app.get("/response.mp3")
async def get_audio():
    if os.path.exists(CURRENT_AUDIO_FILE):
        return FileResponse(CURRENT_AUDIO_FILE, media_type="audio/mpeg")
    else:
        return JSONResponse(status_code=404, content={"error": "Audio file not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
