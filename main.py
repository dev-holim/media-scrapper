from fastapi import FastAPI

app = FastAPI()

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    from uvicorn import run
    run(app)