import settings
class Movie:#値段を持つだけ
    def __init__(
        self, 
        id: str,
        title: str,
        image_url: str,
    ):
        #self.id = id,？？？ここにカンマ置いたやつ絶対に許さない。
        self.id = id
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