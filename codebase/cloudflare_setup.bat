@echo off
chcp 65001 >nul
echo ============================================
echo  CLOUDFLARE TUNNEL - CAU HINH URL CO DINH
echo ============================================
echo.
echo Buoc 1: Dang nhap Cloudflare
cloudflared tunnel login

echo.
echo Buoc 2: Tao tunnel ten "ai-healthcare"
cloudflared tunnel create ai-healthcare

echo.
echo Buoc 3: Lay Tunnel ID tu output tren, nhap vao day:
set /p TUNNEL_ID="Nhap Tunnel ID: "

echo.
echo Buoc 4: Tao file cau hinh...
(
echo tunnel: %TUNNEL_ID%
echo credentials-file: %USERPROFILE%\.cloudflared\%TUNNEL_ID%.json
echo.
echo ingress:
echo   - hostname: ai-healthcare.yourdomain.com
echo     service: http://localhost:8501
echo   - service: http_status:404
) > "%USERPROFILE%\.cloudflared\config.yml"

echo.
echo Buoc 5: Them DNS (thay 'yourdomain.com' bang domain cua ban):
echo   cloudflared tunnel route dns ai-healthcare ai-healthcare.yourdomain.com
echo.
echo Buoc 6: Chay tunnel co dinh:
echo   cloudflared tunnel run ai-healthcare
echo.
pause
