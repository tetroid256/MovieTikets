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
        BABY, KIDS, TEEN, SENIOR = 3, 13, 18, 60
        # 料金設定
        prices = {#Movieから値段を取ってくる
            "baby": self.movie.kids,
            "kids": self.movie.kids,
            "teen": self.movie.teen,
            "base": self.movie.base,
            "senior": self.movie.senior
        }

        if self.age < BABY:
            return prices["FREE"]
        elif self.age < KIDS:
            return prices["U13"]
        
        if self.is_member:
            return prices["MEMBER10"] if self.count % 10 == 0 else prices["MEMBER"]
        return prices["NORMAL"]