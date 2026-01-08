#年齢区分
BABY, KIDS, TEEN, SENIOR = 3, 13, 18, 60

#割引額
DISCOUNT = 300

import os

# データの入っているフォルダ名
DATA_DIR = "data"

# 各ファイルのパスを自動で作る
MOVIES_CSV = os.path.join(DATA_DIR, "movies.csv")
PRICES_CSV = os.path.join(DATA_DIR, "prices.csv")
SCHEDULES_CSV = os.path.join(DATA_DIR, "schedules.csv")