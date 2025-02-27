import nest_asyncio
nest_asyncio.apply()

import os
import re
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Added for CORS support
from pydantic import BaseModel
from dotenv import load_dotenv
from googlesearch import search
from youtubesearchpython import VideosSearch
from pytube import request as pytube_request
from bs4 import BeautifulSoup
from groq import Groq
from RealtimeTTS import TextToAudioStream, EdgeEngine
from jose import jwt, JWTError

# Load environment variables (assumes .env is in the same directory)
load_dotenv()

# Initialize FastAPI app and add CORS middleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------------------------------
# Prepbk Functionality (Prefix: /prepbk)
# ---------------------------------------------------

# System prompt and direction for Groq (Prepbk)
system_prompt = """
user will ask abaout any topic to prepare so your task is to give a very simple way of preparing for the goal which 
the user want to learn.
your reply should be very precise
"""
Direction = [{"role": "system", "content": system_prompt}]

def search_youtube_playlists(query: str, num_playlists: int = 3):
    query_string = query.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query_string}&sp=EgIQAw%3D%3D"
    html = pytube_request.get(url)
    playlist_ids = re.findall(r'"playlistId":"(.*?)"', html)
    unique_ids = []
    for pid in playlist_ids:
        if pid not in unique_ids:
            unique_ids.append(pid)
        if len(unique_ids) == num_playlists:
            break
    playlists = []
    for pid in unique_ids:
        playlist_url = f"https://www.youtube.com/playlist?list={pid}"
        playlist_html = pytube_request.get(playlist_url)
        playlist_soup = BeautifulSoup(playlist_html, 'html.parser')
        title_tag = playlist_soup.find('title')
        title = title_tag.get_text().replace(" - YouTube", "").strip() if title_tag else "Playlist"
        thumbnail_meta = playlist_soup.find('meta', property="og:image")
        thumbnail = thumbnail_meta.get("content") if thumbnail_meta else ""
        playlists.append({
            "link": playlist_url,
            "title": title,
            "thumbnail": thumbnail
        })
    return playlists

def search_youtube_videos(query: str, num_videos: int = 7):
    video_search = VideosSearch(query, limit=num_videos)
    videos_data = video_search.result()
    videos = []
    for item in videos_data.get("result", []):
        videos.append({
            "link": item.get("link"),
            "title": item.get("title"),
            "thumbnail": item.get("thumbnails")[0].get("url") if item.get("thumbnails") and len(item.get("thumbnails")) > 0 else ""
        })
    return videos

def search_learning_websites(query: str, num_links: int = 5):
    return list(search(query, num_results=num_links))

# Initialize Groq client for Prepbk using key GROQ_API_KEY_1
groq_client_prepbk = Groq(api_key=os.getenv("GROQ_API_KEY_1"))

def query_groq(user_input: str) -> str:
    completion = groq_client_prepbk.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=Direction + [{"role": "user", "content": user_input}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content if completion.choices else "No response from Groq"

@app.get("/prepbk")
def read_prepbk():
    return {"message": "Prepbk API is working"}

@app.post("/prepbk/get_resources")
def get_resources(data: Dict[str, str]):
    user_query = data.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    groq_response = query_groq(user_query)
    videos = search_youtube_videos(user_query)
    playlists = search_youtube_playlists(user_query, num_playlists=3)
    learning_links = search_learning_websites(user_query, num_links=5)

    return {
        "groq_response": groq_response,
        "videos": videos,
        "playlists": playlists,
        "learning_resources": learning_links
    }

# ---------------------------------------------------
# Quiz Functionality (Prefix: /quiz)
# ---------------------------------------------------

class QuizRequest(BaseModel):
    subject: str = "DSA"
    difficulty: str = "Easy"
    proficiency: str = "Beginner"

@app.post("/quiz/generate-quiz")
def generate_quiz(data: QuizRequest):
    subject = data.subject.strip()
    difficulty = data.difficulty
    proficiency = data.proficiency

    if subject.upper() == "DSA":
        subject = "Data Structures and Algorithms"

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent MCQ generator and evaluator. Your task is to create multiple-choice questions (MCQs) "
                "based on the user's specified subject, difficulty level, and proficiency. Please generate the quiz as a strictly valid JSON array. "
                "Do not include any markdown formatting or extra text. Each object in the array should have the following keys:\n"
                " - id (a unique number)\n"
                " - question (a string)\n"
                " - options (an array of objects; each object has keys 'id' and 'text')\n"
                " - correctAnswer (the id of the correct option)\n"
                " - estimatedTime (a string, e.g., '30 seconds')\n"
                " - concept (a string representing the specific concept or topic that this question covers, e.g., 'Stacks', 'Queues', etc.)\n"
                "Note: If the subject is provided as 'DSA', it should be interpreted as 'Data Structures and Algorithms'."
            )
        },
        {
            "role": "user",
            "content": (
                f"I'm a {proficiency} level student who wants to prepare for {subject} at a {difficulty} difficulty level. "
                "Please ensure that each question specifically indicates the topic or concept it covers."
            )
        }
    ]

    groq_client_quiz = Groq(api_key=os.getenv("GROQ_API_KEY_2"))
    completion = groq_client_quiz.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    quiz_content_str = completion.choices[0].message.content
    print("Raw quiz content from AI:", quiz_content_str)

    try:
        quiz_array = json.loads(quiz_content_str)
    except Exception as e:
        print("Direct JSON parsing failed:", e)
        start = quiz_content_str.find('[')
        end = quiz_content_str.rfind(']')
        if start != -1 and end != -1:
            json_string = quiz_content_str[start:end+1]
            try:
                quiz_array = json.loads(json_string)
            except Exception as e:
                print("Fallback JSON parsing failed:", e)
                quiz_array = []
        else:
            quiz_array = []
    
    return {"quiz": quiz_array}

class IncorrectQuestion(BaseModel):
    id: int
    question: str
    concept: Optional[str] = None
    userAnswer: int
    correctAnswer: int

class FeedbackRequest(BaseModel):
    incorrectQuestions: List[IncorrectQuestion]

@app.post("/quiz/generate-feedback")
def generate_feedback(data: FeedbackRequest):
    incorrect_questions = data.incorrectQuestions
    questions_text = ""
    for q in incorrect_questions:
        questions_text += f"Question ID {q.id}: {q.question}\n"
        if q.concept:
            questions_text += f"Concept: {q.concept}\n"
        questions_text += f"User Answer: {q.userAnswer}, Correct Answer: {q.correctAnswer}\n\n"
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert tutor in Data Structures and Algorithms. Based on the list of questions a student answered incorrectly, "
                "analyze the underlying topics and provide detailed feedback on which specific areas the student needs to focus on, along with actionable suggestions for improvement. "
                "Your response should be in plain text."
            )
        },
        {
            "role": "user",
            "content": f"Here are the questions answered incorrectly:\n{questions_text}"
        }
    ]

    groq_client_quiz = Groq(api_key=os.getenv("GROQ_API_KEY_2"))
    completion = groq_client_quiz.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        stop=None,
    )

    feedback = completion.choices[0].message.content
    return {"feedback": feedback}

@app.get("/quiz")
def read_quiz():
    return {"message": "Quiz API is working"}

# ---------------------------------------------------
# Voic Functionality (Prefix: /voic)
# ---------------------------------------------------

# Setup logging for voice endpoints
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voic")

# Initialize Groq client for Voic using key GROQ_API_KEY_3
groq_client_voic = Groq(api_key=os.getenv("GROQ_API_KEY_3"))

# Initialize TTS engine and audio stream
engine = EdgeEngine()
engine.set_voice("en-GB-RyanNeural")
engine.rate = 10
engine.pitch = -26
stream = TextToAudioStream(engine)

# Global state for conversation (single-session demo)
stage = "initial"         # can be "initial", "awaiting_topic", or "interviewing"
candidate_topic = None
conversation_history = []
CURRENT_AUDIO_FILE = "static/response.mp3"

class QueryRequest(BaseModel):
    text: str
    stop_audio: bool = False

def stop_current_audio():
    try:
        stream.stop()
        logger.info("Audio stopped successfully.")
    except Exception as e:
        logger.error(f"Error stopping audio: {e}")

@app.get("/voic/stop_audio")
async def stop_audio():
    stop_current_audio()
    return {"status": "Audio stopped"}

def generate_speech_async(text: str):
    try:
        logger.info(f"Generating speech for text: {text}")
        stream.feed(text)
        audio_data = stream.play()
        with open(CURRENT_AUDIO_FILE, "wb") as f:
            f.write(audio_data)
        logger.info("Audio file generated successfully.")
    except Exception as e:
        logger.error(f"Error in TTS generation: {e}")

@app.post("/voic/query")
async def query(request: QueryRequest, background_tasks: BackgroundTasks):
    global stage, candidate_topic, conversation_history
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
            chat_completion = groq_client_voic.chat.completions.create(
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
            chat_completion = groq_client_voic.chat.completions.create(
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

@app.get("/voic/response.mp3")
async def get_audio():
    if os.path.exists(CURRENT_AUDIO_FILE):
        return FileResponse(CURRENT_AUDIO_FILE, media_type="audio/mpeg")
    else:
        return JSONResponse(status_code=404, content={"error": "Audio file not found"})

@app.get("/voic")
def read_voic():
    return {"message": "Voic API is working"}

# ---------------------------------------------------
# Optional: Run with Uvicorn if executed directly
# ---------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)
