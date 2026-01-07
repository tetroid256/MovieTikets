from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv
import random

# 自分の作ったファイルをインポートする
from models import Ticket,Movie

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_movie_data():
    # encoding='utf-8' は日本語を含む場合に必須
    with open('movies.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        movie_database = {}
        for row in reader:
            ids:str = row['movie_id']
            movie = Movie(
                id = ids,
                title = row['title'],
                image_url = row['image_url'],
            )
            movie_database[ids] = movie
    with open('prices.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row['movie_id']
            cat = row['category']
            price = int(row['price'])

            movie_database[mid].prices[cat] = price
    return movie_database
    
MOVIE_DB = get_movie_data()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    movie_db = MOVIE_DB
    movie_list = list(movie_db.values())
    amount = min(len(movie_list),4)
    rec_list = random.sample(movie_list,amount)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "movies": movie_list,
        "recommendations": rec_list
    })

#booking用

@app.get("/booking", response_class=HTMLResponse)
def get_booking_page(request: Request, movie_id: str):
    movie = MOVIE_DB.get(movie_id)
    return templates.TemplateResponse("booking.html", {
        "request": request,
        "movie": movie
    })

@app.post("/result", response_class=HTMLResponse)
def show_result(
    request: Request,
    movie_id: str = Form(...),
    date: str = Form(...),
    seat: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    is_member: bool = Form(False)
):
    movie_db = MOVIE_DB
    watch_movie = movie_db.get(movie_id)
    if not watch_movie:
        return HTMLResponse("エラー", status_code=404)
    ticket = Ticket(age=age,is_member=is_member,movie=watch_movie,count = 1)
    fee = ticket.fee_calc()
    if fee == -1:
        return HTMLResponse("""
            <h1>予約エラー</h1>
            <p>この作品はR-15指定です。15歳未満の方はご鑑賞いただけません。</p>
            <a href="/">トップに戻る</a>
        """, status_code=400)
    else:
        return templates.TemplateResponse("result.html", {
        "request": request,
        "name": name,
        "movie": watch_movie,
        "date": date,
        "seat": seat,
        "price": fee
    })