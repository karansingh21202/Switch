from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from the src package
from src.Prepbk import prep_router
from src.Quiz import quiz_router
from src.Voic import voic_router  # Assuming you have refactored Voic similarly

app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes so endpoints are namespaced
app.include_router(prep_router, prefix="/prepbk")
app.include_router(quiz_router, prefix="/quiz")
app.include_router(voic_router, prefix="/voic")

@app.get("/")
def read_root():
    return {"message": "Main API is working"}

if __name__ == "__main__":
    import uvicorn
    # For local testing, use port 7000 (or any port you choose)
    uvicorn.run(app, host="127.0.0.1", port=7000)
