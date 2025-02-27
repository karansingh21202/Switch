from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import re
from groq import Groq
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from the project root (.env)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

# Create an APIRouter instance for quiz endpoints
quiz_router = APIRouter()

# Instantiate the Groq client with your API key for quiz functionality
GROQ_API_KEY = os.getenv("GROQ_API_KEY_2")
groq_client = Groq(api_key=GROQ_API_KEY)

class QuizRequest(BaseModel):
    subject: str = "DSA"
    difficulty: str = "Easy"
    proficiency: str = "Beginner"

@quiz_router.post("/generate-quiz")
def generate_quiz(data: QuizRequest):
    subject = data.subject.strip()
    difficulty = data.difficulty
    proficiency = data.proficiency

    if subject.upper() == "DSA":
        subject = "Data Structures and Algorithms"

    # Define a system prompt that instructs the AI to generate MCQs with a concept field.
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

    # Use the groq_client to generate the quiz
    completion = groq_client.chat.completions.create(
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

    # Try to parse the output as JSON
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

@quiz_router.post("/generate-feedback")
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

    completion = groq_client.chat.completions.create(
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

@quiz_router.get("/")
def read_quiz():
    return {"message": "Quiz API is working"}
