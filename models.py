import settings
class Movie:#値段を持つだけ
    def __init__(
        self, 
        id: int,
        title: str,
        image_url: str,
    ):
        self.id = id,
        self.title = title
        self.image_url = image_url
        self.prices = {}
    
class Ticket:
    def __init__(self, age: int, is_member: bool, movie: Movie, count: int = 1):
        self.age = age
        self.is_member = is_member
        self.movie = movie
        self.count = count

    def fee_calc(self):#映倫規定により
        if self.age < 15 and self.movie.kids == -1:
            return -1

        BABY, KIDS, TEEN, SENIOR = settings.BABY, settings,KIDS, settings.TEEN, settings.SENIOR
        DISCOUNT = settings.DISCOUNT

        # 料金設定
        prices = {#Movieから値段を取ってくる
            "baby": self.movie.baby,
            "kids": self.movie.kids,
            "teen": self.movie.teen,
            "base": self.movie.base,
            "senior": self.movie.senior
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