from fastapi import FastAPI

from app.mocks.openai import router as openai_router

app = FastAPI(title="LangGrinch Sandbox Mock Server")

app.include_router(openai_router, prefix="/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
