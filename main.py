import sqlite3
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Проверяем наличие папки templates
templates = Jinja2Templates(directory="templates")

# Функция инициализации БД (создает файл users.db, если его нет)
def init_db():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'student'
            )
        ''')
        conn.commit()
        conn.close()
        print("--- База данных готова к работе ---")
    except Exception as e:
        print(f"Ошибка при создании БД: {e}")

init_db()

# --- МАРШРУТЫ ---

@app.get("/", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def read_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/recovery", response_class=HTMLResponse)
async def read_recovery(request: Request):
    return templates.TemplateResponse("recovery.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # В будущем мы будем передавать сюда имя пользователя из базы
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": "Ученик"})

# ОБРАБОТКА РЕГИСТРАЦИИ (тот самый POST запрос)
@app.post("/register")
async def post_register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("student")
):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username, email, password, role)
        )
        conn.commit()
        conn.close()
        return RedirectResponse(url="/auth", status_code=303)
    except sqlite3.IntegrityError:
        return HTMLResponse("<h1>Ошибка: Почта уже занята!</h1><a href='/register'>Назад</a>")
    except Exception as e:
        return HTMLResponse(f"<h1>Ошибка сервера: {e}</h1>")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)