from fastapi import FastAPI
from app.backend.controllers.detection_controller import router as detection_router

app = FastAPI()

app.include_router(detection_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
