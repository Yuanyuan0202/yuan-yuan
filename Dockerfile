# 使用官方的Python映像作為基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的內容到工作目錄中
COPY . /app

# 安裝所需的Python依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 確保gen_license腳本有可執行權限
RUN chmod +x /app/gen_license/gen_license

# 暴露應用程式運行的端口
EXPOSE 8000

# 定義容器啟動時運行的命令
CMD ["python", "main.py"]

