import settings
from pydantic import BaseModel, Field
from typing import List, Dict

class Movie(BaseModel):
    id: str
    title: str
    image_url: str
    duration: int
    
    prices: Dict[str, int] = Field(default_factory=dict)
    start_time: List[str] = Field(default_factory=list)
    
class Ticket:
    def __init__(self, age: int, is_member: int, movie: Movie, count: int = 1):
        self.age = age
        self.is_member = is_member
        self.movie = movie
        self.count = count

    def fee_calc(self):#映倫規定により
        BABY, KIDS, TEEN, SENIOR = settings.BABY, settings.KIDS, settings.TEEN, settings.SENIOR
        DISCOUNT = settings.DISCOUNT

        price_dict = self.movie.prices

        if self.age < 15 and price_dict.get("kids") == -1:
            return -1

        # 料金設定
        prices = {
            "baby": price_dict.get("baby", 0),
            "kids": price_dict.get("kids", 0),
            "teen": price_dict.get("teen", 0),
            "base": price_dict.get("base", 0),
            "senior": price_dict.get("senior", 0)
        }

        fee = 0
        if self.age < BABY:
            fee = prices["baby"]
        elif self.age < KIDS:
            fee = prices["kids"]
        elif self.age < TEEN:
            fee = prices["teen"]
        elif self.age > SENIOR:
            fee = prices["senior"]
        else:
            fee = prices["base"]
        
        if self.is_member == True:
            fee = max(fee - DISCOUNT , 0)
        if self.count % 10 == 0:
            fee = max(fee - DISCOUNT , 0)
        return fee
    
    def get_type_label(self):
        BABY, KIDS, TEEN, SENIOR = settings.BABY, settings.KIDS, settings.TEEN, settings.SENIOR
        if self.age < BABY: return "幼児"
        if self.age < KIDS: return "小学生"
        if self.age < TEEN: return "中高生"
        if self.age >= SENIOR: return "シニア"
        return "一般"

class Order:
    def __init__(self):
        self.tickets = []
        self.discount = 0

    def add_ticket(self, ticket: Ticket):
        if len(self.tickets) >= 4:
            raise ValueError("4枚までです")
        self.tickets.append(ticket)
    
    def total_price(self):
        total = 0
        for tiket in self.tickets:
            total += tiket.fee_calc()
        return total
    
    def set_coupon(self, discount: int):
        self.discount = discount
    
    def apply_coupon(self):
        total = self.total_price()
        return max(total - self.discount, 0)
    
    def get_subtotal(self):
        total = 0
        for ticket in self.tickets:
            total += ticket.fee_calc()
        return total
    
    def get_total_price(self):
        return max(self.get_subtotal() - self.discount, 0)
    
class CalcRequest(BaseModel):
    movie_id: str
    ages: List[int]
    is_members: List[int]
    coupon_code: str = "" 
    
class OrderLog(BaseModel):
    order_id: str
    timestamp: str
    movie_title: str
    watch_date: str
    watch_time: str
    seat: str
    representative: str
    head_count: int
    total_price: int
    coupon_used: str