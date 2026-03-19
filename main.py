from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Указываем, где лежат наши HTML-шаблоны
templates = Jinja2Templates(directory="templates")

# Подключаем папку для CSS/картинок (создай её пустой рядом с main.py)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_about(request: Request):
    # Страница "О нас" (входная точка по твоей схеме)
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def read_auth(request: Request):
    # Страница "Авторизация"
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/recovery", response_class=HTMLResponse)
async def read_recovery(request: Request):
    # Страница "Восстановление ака"
    return templates.TemplateResponse("recovery.html", {"request": request})

@app.get("/main", response_class=HTMLResponse)
async def read_main(request: Request):
    # "Главная" страница личного кабинета
    return templates.TemplateResponse("main_page.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)