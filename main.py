from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
# 自分の作ったファイルをインポートする
from models import Ticket

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # index.html ファイルを読み込んで返す
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/greet")
def greet_user(name: str, age: int, is_member: bool):
    # models.py の Ticket クラスを使う
    cur_ticket = Ticket(age=age, is_member=is_member)
    fee = cur_ticket.fee_calc()
    return {"reply": f"こんにちは {name}様", "fee": fee}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)