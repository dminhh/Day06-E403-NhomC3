# Hướng dẫn cài đặt và chạy

## Yêu cầu

- Python 3.10+
- pip

## Cài đặt

```bash
cd codebase
pip install -r requirements.txt
```

## Cấu hình

```bash
cp .env.example .env
# Điền LLM_API_KEY vào file .env
```

## Chạy app

```bash
streamlit run app.py
```

Mở trình duyệt tại `http://localhost:8501`

## Tính năng

### 1. Phân tích đơn thuốc
- Nhập text hoặc tải ảnh đơn thuốc
- AI trích xuất danh sách thuốc
- Giải thích từng thuốc bằng tiếng Việt
- Cảnh báo tương tác nguy hiểm

### 2. Tra cứu thuốc
- Tìm kiếm theo tên thuốc
- Dữ liệu từ RxNorm + OpenFDA
- Kiểm tra tương tác nhiều thuốc

## Tech stack

| Thành phần | Công nghệ |
|---|---|
| Frontend | Streamlit |
| LLM | GPT-OSS-20B (FPT Cloud) |
| OCR | PaddleOCR |
| Drug DB | RxNorm API |
| Drug Info | OpenFDA API |
