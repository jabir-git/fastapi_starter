from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
import uvicorn
from livereload import router as livereload_router
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()
app.include_router(livereload_router)

# Mount static folder
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Mount templates
templates_folder_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(templates_folder_path)


@app.get("/")
def index(request: Request):
    is_debug = os.getenv("DEBUG", "false").lower() == "true"
    return templates.TemplateResponse(request=request, name="index.html", context={"is_debug": is_debug})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
