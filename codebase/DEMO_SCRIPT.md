# Demo Script — AI Đọc Đơn Thuốc

## Happy Case (paste vào ô nhập tay)

```
Bệnh nhân: Nguyễn Văn A, 55 tuổi, nam
Chẩn đoán: Tăng huyết áp, Đái tháo đường type 2
Ngày kê: 04/06/2026
Bác sĩ: BS. Trần Minh Tuấn - BV Bạch Mai

1. Amlodipine 5mg - uống 1 viên/ngày vào buổi sáng
2. Metformin 500mg - uống 2 viên/ngày, sau ăn sáng và tối
3. Omeprazole 20mg - uống 1 viên/ngày trước ăn sáng 30 phút
```

**Expected:** AI giải thích từng thuốc bằng tiếng Việt, không có cảnh báo đỏ.

---

## Error Case — Tương tác nguy hiểm (dùng tính năng Kiểm tra tương tác)

```
Warfarin
Aspirin
Ibuprofen
```

**Expected:** Highlight đỏ tương tác Warfarin + Aspirin, yêu cầu xác nhận bác sĩ.

---

## Low-confidence Case

```
Amo 5 - 1v/n
MTF 500 x2
Ome 20 trc an
```

**Expected:** Cảnh báo vàng "không tìm thấy thông tin đầy đủ" cho các tên viết tắt.

---

## Thứ tự demo (5 phút)

| Phút | Người | Nội dung |
|------|-------|----------|
| 0:00 | Hiếu | Problem + painpoint Long Châu |
| 1:30 | Huy | Demo happy case (nhập text đơn thuốc) |
| 2:30 | Huy | Demo tra cứu thuốc Metformin |
| 3:30 | Minh | Demo error case (tương tác Warfarin+Aspirin) |
| 4:30 | Minh | Augment vs Automate + kết luận |
