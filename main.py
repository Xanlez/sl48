from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def read_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/recovery", response_class=HTMLResponse)
async def read_recovery(request: Request):
    return templates.TemplateResponse("recovery.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)