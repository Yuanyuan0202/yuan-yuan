/ License Generator
一個用於生許可證的 Web。包含前端和後端，並使用 Docker 進行容器化。

/ 目錄
簡介
功能
安裝
使用方法

/ 簡介
本專案提供一個網頁介面，用戶可以通過該介面填寫相關信息生成軟體許可證。後端負責處理生成許可證的邏輯，並將生成的許可證文件儲存或上傳到指定位置。

/ 功能
用戶可以通過表單輸入信息來生成許可證
生成的許可證可以自動打包為壓縮文件
支持將許可證文件上傳到指定的遠程伺服器

/ 安裝
- 先決條件
安裝 Docker
- 安裝步驟
1. clone 儲存庫
git clone https://github.com/Yuanyuan0202/yuan-yuan.git
cd yuan-yuan

2.構建 Docker 映像
docker build -t license_generator .

3.運行 Docker 容器
docker run -d -p 8000:8000 license_generator

/ 使用方法
打開瀏覽器進入 http://localhost:8000
填寫表單，並點擊「License Generate」按鈕。


前端：HTML, CSS, JavaScript
後端：Python, FastAPI
容器化：Docker
