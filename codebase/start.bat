@echo off
chcp 65001 >nul
title AI Chăm Sóc Sức Khỏe

echo ============================================
echo    AI CHAM SOC SUC KHOE - KHOI DONG
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Python chua duoc cai dat!
    pause
    exit /b 1
)

:: Install dependencies if needed
if not exist ".deps_installed" (
    echo [1/4] Cai dat thu vien...
    pip install -r requirements.txt -q
    echo. > .deps_installed
    echo     Hoan thanh!
)

:: Copy .env if not exists
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [2/4] Tao file .env tu .env.example
    )
)

echo [3/4] Khoi dong Streamlit...
echo.
echo ============================================
echo   URL noi bo: http://localhost:8501
echo ============================================
echo.

:: Start Streamlit in background
start "" cmd /c "streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false"

:: Wait for Streamlit to start
echo Dang khoi dong Streamlit...
timeout /t 4 /nobreak >nul

:: Check if cloudflared is available
where cloudflared >nul 2>&1
if not errorlevel 1 (
    echo [4/4] Bat dau Cloudflare Tunnel...
    echo.
    echo ============================================
    echo  Dang tao duong dan cong khai qua Cloudflare...
    echo ============================================
    echo.
    cloudflared tunnel --url http://localhost:8501
) else (
    echo [4/4] Cloudflared chua duoc cai dat.
    echo.
    echo De su dung Cloudflare Tunnel:
    echo   1. Tai cloudflared tu: https://github.com/cloudflare/cloudflared/releases
    echo   2. Dat vao thu muc co trong PATH
    echo   3. Chay lai file nay
    echo.
    echo Ung dung dang chay tai: http://localhost:8501
    echo.
    start http://localhost:8501
    pause
)
