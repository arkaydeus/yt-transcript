import datetime
from urllib.parse import quote, unquote

from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi.middleware.cors import CORSMiddleware


from api.yt_id import get_yt_id

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/decode/")
def decode(url: str):

    decoded: str = unquote(url)
    yt_id: str = get_yt_id(decoded)
    transcript_text = "Video not found"
    if yt_id:
        transcript: list = YouTubeTranscriptApi.get_transcript(yt_id)
        if transcript and isinstance(transcript, list):
            lines: list[str] = [str(x["text"]) for x in transcript]
            transcript_text = "\n".join(lines)

    return {"video_id": yt_id, "transcript": transcript_text}


@app.get("/")
def main():
    return {"message": "Path not found"}
