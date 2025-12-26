# Python 3.11が入った軽量Linuxをベースにする
FROM python:3.11-slim

# コンテナ内の作業場所を /app に設定
WORKDIR /app

# 先にライブラリだけインストール（ビルド高速化のため）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 残りのプログラムファイルをすべてコピー
COPY . .

# FastAPIを起動（0.0.0.0で全開放するのがDockerの鉄則）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]