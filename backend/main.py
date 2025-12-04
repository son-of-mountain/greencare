from fastapi import FastAPI

app = FastAPI(
    title="GreenCare API",
    description="API du module RSE pour Numih dh",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "GreenCare V5 API is running", "status": "healthy"}
