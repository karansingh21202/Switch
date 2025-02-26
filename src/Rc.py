from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from time import time
import re
from urllib.parse import unquote
import requests
from googlesearch import search


# For YouTube search functionality:
from youtubesearchpython import VideosSearch  # For video search
# We use pytube.request to fetch raw HTML for playlist scraping.
from pytube import request
from bs4 import BeautifulSoup

# For the AI model query (Groq)
from groq import Groq

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
        # Extract title from the <title> tag
        title_tag = playlist_soup.find('title')
        title = title_tag.get_text().replace(" - YouTube", "").strip() if title_tag else "Playlist"
        # Extract thumbnail from the og:image meta tag
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
# Initialize Groq client with your API key (replace with your own key)
groq_client = Groq(api_key="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")

def query_groq(user_input: str) -> str:
    """
    Queries the Groq API (an AI model) with the user query to produce a very short summary/preparation hint.
    """
    completion = groq_client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages = Direction + [{"role": "user", "content": user_input}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content if completion.choices else "No response from Groq"

# ---------------------------
# FastAPI App
# ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get_resources")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
