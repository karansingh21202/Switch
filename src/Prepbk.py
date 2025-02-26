from fastapi import APIRouter, HTTPException
from typing import Dict
import re
import os
from dotenv import load_dotenv
import requests
from googlesearch import search
from youtubesearchpython import VideosSearch
from pytube import request
from bs4 import BeautifulSoup
from groq import Groq

prep_router = APIRouter()

# Load environment variables from the project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

system_prompt = """
user will ask abaout any topic to prepare so your task is to give a very simple way of preparing for the goal which 
the user want to learn.
your reply should be very precise
"""
Direction = [
    {"role": "system", "content": system_prompt}
]

# ---------------------------
# YouTube & Learning Functions
# ---------------------------
def search_youtube_playlists(query: str, num_playlists: int = 3):
    query_string = query.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query_string}&sp=EgIQAw%3D%3D"
    html = request.get(url)
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
        playlist_html = request.get(playlist_url)
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

# ---------------------------
# Groq AI Query Function
# ---------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY_1")
groq_client = Groq(api_key=GROQ_API_KEY)

def query_groq(user_input: str) -> str:
    completion = groq_client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=Direction + [{"role": "user", "content": user_input}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content if completion.choices else "No response from Groq"

# ---------------------------
# API Endpoints using the Router
# ---------------------------
@prep_router.get("/")
def read_prepbk():
    return {"message": "Prepbk API is working"}

@prep_router.post("/get_resources")
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
