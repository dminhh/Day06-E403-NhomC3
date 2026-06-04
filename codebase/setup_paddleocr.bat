@echo off
chcp 65001 >nul
title Cai dat PaddleOCR

echo ============================================
echo    CAI DAT PADDLEOCR CHO TIENG VIET
echo ============================================
echo.
echo Qua trinh nay co the mat 5-15 phut...
echo.

:: Install PaddlePaddle (CPU version)
echo [1/3] Cai dat PaddlePaddle (CPU)...
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
if errorlevel 1 (
    echo Thu cai dat tu PyPI...
    pip install paddlepaddle
)

:: Install PaddleOCR
echo.
echo [2/3] Cai dat PaddleOCR...
pip install paddleocr

:: Test installation
echo.
echo [3/3] Kiem tra cai dat...
python -c "from paddleocr import PaddleOCR; print('PaddleOCR da san sang!')" 2>nul
if errorlevel 1 (
    echo [LOI] Cai dat that bai. Ung dung van hoat dong - se su dung che do nhap tay.
) else (
    echo [OK] PaddleOCR da duoc cai dat thanh cong!
)

echo.
pause
