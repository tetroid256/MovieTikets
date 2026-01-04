from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import csv

# 自分の作ったファイルをインポートする
from models import Ticket

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_movie_data():
    movies = []
    # encoding='utf-8' は日本語を含む場合に必須
    with open('movies.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append(row)
    return movies

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # 1. データを取得
    movie_list = get_movie_data()
    
    # 2. テンプレートに "movies" という名前でリストを渡す
    return templates.TemplateResponse("index.html", {
        "request": request,
        "movies": movie_list
    })

@app.get("/greet")
def greet_user(name: str, age: int, is_member: bool):
    # models.py の Ticket クラスを使う
    cur_ticket = Ticket(age=age, is_member=is_member)
    fee = cur_ticket.fee_calc()
    return {"reply": f"こんにちは {name}様", "fee": fee}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)