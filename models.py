class Ticket:
    def __init__(self, age: int, is_member: bool, count: int = 1):
        self.age = age
        self.is_member = is_member
        self.count = count

    def fee_calc(self):
        BABY, KIDS = 3, 13
        # 料金設定
        prices = {
            "FREE": 0,
            "U13": 500,
            "MEMBER10": 500,
            "MEMBER": 700,
            "NORMAL": 1000
        }

        if self.age < BABY:
            return prices["FREE"]
        elif self.age < KIDS:
            return prices["U13"]
        
        if self.is_member:
            return prices["MEMBER10"] if self.count % 10 == 0 else prices["MEMBER"]
        return prices["NORMAL"]