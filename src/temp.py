# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from googlesearch import search

app = FastAPI()

# Configure CORS (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the job profile data
class JobProfile(BaseModel):
    name: str
    age: int
    experience: int
    education: str
    skills: str
    certifications: str
    preferredJobTitles: str
    industries: str
    locations: str
    salaryExpectations: str
    languages: str
    linkedIn: str
    summary: str

# Initialize the Groq client (secure your API key in production)
client = Groq(api_key="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")

@app.post("/api/generate-jobs")
async def generate_jobs(profile: JobProfile):
    # Build a profile summary from the provided data
    profile_summary = (
        f"Summary: {profile.summary}. "
        f"Skills: {profile.skills}. "
        f"Preferred Job Titles: {profile.preferredJobTitles}. "
        f"Industries: {profile.industries}. "
        f"Locations: {profile.locations}."
    )
    
    # Updated prompt to generate a query specifically for recent, relevant job postings
    prompt = (
        f"Based on the following candidate profile, generate a precise Google search query that finds "
        f"recent and relevant job listings on linkedin.com/jobs. The query should target the candidate's "
        f"preferred job titles and locations, include keywords such as 'recent', 'new', or 'job posting', "
        f"and avoid irrelevant results (like management-level positions) if they don't match the candidate's profile. "
        f"Focus on current individual contributor roles where possible:\n\n{profile_summary}"
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating query from Groq model")
    
    # Extract and strip the generated query text
    generated_query = completion.choices[0].message.content.strip()
    if not generated_query:
        generated_query = "Software Engineer recent job posting site:linkedin.com/jobs"
    
    # Ensure the query explicitly includes the site filter
    if "site:" not in generated_query.lower():
        generated_query += " site:linkedin.com/jobs"
    
    results = []
    try:
        # Retrieve a larger set of results to filter from
        for url in search(generated_query, num_results=10):
            if "linkedin.com/jobs" in url:
                results.append(url)
        # If no results are found, use a fallback query
        if not results:
            fallback_query = "Software Engineer recent job posting site:linkedin.com/jobs"
            for url in search(fallback_query, num_results=10):
                if "linkedin.com/jobs" in url:
                    results.append(url)
        # Limit to five results
        results = results[:5]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching search results")
    
    return {"query": generated_query, "results": results}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
