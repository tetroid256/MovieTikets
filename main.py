from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv
import random
from typing import List
from pydantic import BaseModel
import uuid
import datetime
import os
import io
import base64
import qrcode

# 自分の作ったファイルをインポートする
from models import Ticket, Movie, Order, OrderLog, CalcRequest
from settings import MOVIES_CSV, PRICES_CSV, SCHEDULES_CSV, ORDERS_CSV, COUPONS
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_movie_data():
    # encoding='utf-8' は日本語を含む場合に必須
    with open(MOVIES_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        movie_database = {}
        for row in reader:
            ids:str = row['movie_id']
            movie = Movie(
                id = ids,
                title = row['title'],
                image_url = row['image_url'],
                duration = int(row['duration']),
            )
            movie_database[ids] = movie

    with open(PRICES_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row['movie_id']
            cat = row['category']
            price = int(row['price'])
            movie_database[mid].prices[cat] = price

    with open(SCHEDULES_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row['movie_id']
            start_time = row['start_time']
            if mid in movie_database:
                movie_database[mid].start_time.append(start_time)

    return movie_database

def save_order_to_csv(order_data: OrderLog):
    file_exists = os.path.isfile(ORDERS_CSV)
    
    with open(ORDERS_CSV, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow([
                "order_id", "timestamp", "movie_title", 
                "watch_date", "watch_time", "seat", 
                "representative", "head_count", "total_price", "coupon_used"
            ])
            
        writer.writerow([
            order_data.order_id,
            order_data.timestamp,
            order_data.movie_title,
            order_data.watch_date,
            order_data.watch_time,
            order_data.seat,
            order_data.representative,
            order_data.head_count,
            order_data.total_price,
            order_data.coupon_used
        ])

def make_qr_code(data: str):
    # QRコード生成
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 画像をメモリ上に保存してBase64文字列に変換
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # HTMLの<img>タグで使える形式で返す
    return f"data:image/png;base64,{img_str}"
    
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

@app.post("/api/calc")
def calculate_price_api(data: CalcRequest):
    movie = MOVIE_DB.get(data.movie_id)
    if not movie:
        return {"status": "error", "message": "映画が見つかりません"}
    current_order = Order()

    for age, is_member_int in zip(data.ages, data.is_members):
        is_member_bool = (is_member_int == 1)
        ticket = Ticket(age=age, is_member=is_member_bool, movie=movie)
        fee = ticket.fee_calc()
        if fee == -1:
            return {
                "status": "error", 
                "message": "R-15指定作品のため、対象年齢未満の方は購入できません"
            }
        
        current_order.add_ticket(ticket)

    import settings 
    discount_amount = settings.COUPONS.get(data.coupon_code, 0)
    current_order.set_coupon(discount_amount)

    return {
        "status": "ok",
        "subtotal": current_order.get_subtotal(),
        "total_price": current_order.get_total_price(),
        "discount": discount_amount
    }

@app.post("/result", response_class=HTMLResponse)
def show_result(
    request: Request,
    movie_id: str = Form(...),
    date: str = Form(...),
    seat: str = Form(...),
    names: List[str] = Form(...),
    ages: List[int] = Form(...),
    is_members: List[int] = Form(...),
    coupon_code: str = Form(""),
):
    movie_db = MOVIE_DB
    watch_movie = movie_db.get(movie_id)
    if not watch_movie:
        return HTMLResponse("エラー", status_code=404)
    
    current_order = Order()
    ticket_details = []

    #計算部
    for name, age, is_member_int in zip(names, ages, is_members):
        is_member_bool = (is_member_int == 1)
        ticket = Ticket(age=age, is_member=is_member_bool, movie=watch_movie)
        
        if ticket.fee_calc() == -1:
            return HTMLResponse("R-15エラー", status_code=400)
        
        current_order.add_ticket(ticket)

        ticket_details.append({
            "name": name,
            "type_label": ticket.get_type_label(),
            "price": ticket.fee_calc(),
            "is_member": is_member_bool
        })

    import settings
    discount = settings.COUPONS.get(coupon_code, 0)
    current_order.set_coupon(discount)
    subtotal = current_order.get_subtotal()
    total_fee = current_order.get_total_price()

    #CSV保存
    new_order_id = str(uuid.uuid4())
    try:
        w_date, w_time = date.split(' ')
    except ValueError:
        w_date, w_time = date, ""

    order_log = OrderLog(
        order_id=new_order_id,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        movie_title=watch_movie.title,
        watch_date=w_date,
        watch_time=w_time,
        seat=seat,
        representative=names[0], # 代表者名
        head_count=len(names),
        total_price=total_fee,
        coupon_used=coupon_code
    )

    save_order_to_csv(order_log)

    #QRコード化
    qr_code_data = make_qr_code(new_order_id)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "name": names[0],
        "movie": watch_movie,
        "date": date,
        "seat": seat,
        "ticket_details": ticket_details,
        "subtotal": subtotal,
        "discount": discount,
        "total_price": total_fee,
        "order_id": new_order_id,
        "qr_code": qr_code_data
})