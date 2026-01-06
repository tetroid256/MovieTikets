class Movie:#値段を持つだけ
    def __init__(self, title: str, image_url: str, base: int, teen: int, kids: int, baby: int, senior: int):
        self.title = title
        self.image_url = image_url
        self.base = base
        self.teen = teen
        self.kids = kids
        self.baby = baby
        self.senior = senior
    
class Ticket:
    def __init__(self, age: int, is_member: bool, movie: Movie, count: int = 1):
        self.age = age
        self.is_member = is_member
        self.movie = movie
        self.count = count

    def fee_calc(self):
        BABY, KIDS, TEEN, SENIOR = 3, 15, 18, 60
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
            fee = max(fee - 300 , 0)
        if self.count % 10 == 0:
            fee = max(fee - 300 , 0)
        return fee