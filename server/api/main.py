from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.routers.video_router import router as video_router
from src.routers.module_router import router as module_router
from src.routers.course_router import router as course_router
from src.routers.custom_color_router import router as custom_color_router
from src.routers.image_router import router as image_router
from src.routers.user_router import router as user_router
from src.routers.users_courses_router import router as users_courses_router
from src.routers.users_views_router import router as users_views_router

app = FastAPI(
    title="Videohosting API", 
    description="Данная API предназначена для работы видеохостинга", 
    version="1.0.0"
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/public", StaticFiles(directory=Path("./public")), name="public")

@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")

app.include_router(video_router)

app.include_router(module_router)

app.include_router(course_router)

app.include_router(custom_color_router)

app.include_router(image_router)

app.include_router(user_router)

app.include_router(users_courses_router)

app.include_router(users_views_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)