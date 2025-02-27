from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse

from src.utils.custom_logging import setup_logging
from config import Config

from src.routers.video_router import router as video_router
from src.routers.module_router import router as module_router
from src.routers.course_router import router as course_router
from src.routers.color_config_router import router as color_config_router
from src.routers.user_router import router as user_router
from src.routers.user_courses_router import router as user_courses_router
from src.routers.video_view_router import router as video_view_router
from src.routers.course_key_router import router as course_key_router
from src.routers.image_router import router as image_router

app = FastAPI(
    title="Videohosting API", 
    description="Данная API предназначена для работы видеохостинга", 
    version="1.0.3",
)

favicon_path = './favicon.ico'
config = Config()
log = setup_logging()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/public", StaticFiles(directory=Path("./public")), name="public")

# common section
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")

# routers section
app.include_router(video_router)

app.include_router(module_router)

app.include_router(course_router)

app.include_router(color_config_router)

app.include_router(user_router)

app.include_router(user_courses_router)

app.include_router(course_key_router)

app.include_router(video_view_router)

app.include_router(image_router)

if __name__ == "__main__":
    import logging
    import uvicorn
    import yaml

    uvicorn_log_config = 'logging.yaml'

    with open(uvicorn_log_config, 'r') as f:
        uvicorn_config = yaml.safe_load(f.read())
        logging.config.dictConfig(uvicorn_config)

    if config.__getattr__("DEBUG") == "TRUE":
        reload = True
    elif config.__getattr__("DEBUG") == "FALSE":
        reload = False
    else:
        raise Exception("Not init debug mode in env file")
    uvicorn.run("main:app", host=config.__getattr__("HOST"), port=int(config.__getattr__("SERVER_PORT")),
                ssl_keyfile="/etc/letsencrypt/live/me-course.com/privkey.pem" ,
                ssl_certfile="/etc/letsencrypt/live/me-course.com/fullchain.pem",
                log_config=uvicorn_log_config, reload=reload)