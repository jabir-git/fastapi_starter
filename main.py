import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import create_db_tables

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/api/msg")
def read_root():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    create_db_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
