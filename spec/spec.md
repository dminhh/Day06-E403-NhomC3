# SPEC — Đọc Đơn Thuốc (Nhóm C3)

> Sản phẩm giải thích đơn thuốc bằng ngôn ngữ thông thường cho bệnh nhân vừa nhận đơn từ bác sĩ.

---

## 1. Bằng chứng

**Nỗi đau đến từ đâu?**

| Bằng chứng | Nguồn | Điều này nói lên gì |
|---|---|---|
| Long Châu yêu cầu điền form + chờ dược sĩ gọi lại, không có giải thích tức thì | [nhathuoclongchau.com.vn/don-thuoc](https://nhathuoclongchau.com.vn/don-thuoc) | User cần câu trả lời ngay — quy trình hiện tại chậm và phụ thuộc người thật |
| Không có app y tế Việt Nam nào giải thích đơn thuốc bằng ngôn ngữ thông thường | Khảo sát competitor: Long Châu, Jio Health, Ada Health | Đây là khoảng trống thật sự — pain có thật nhưng chưa ai giải quyết |
| Đơn thuốc thường viết tắt, dùng thuật ngữ chuyên môn, không có giải thích đi kèm | Trải nghiệm trực tiếp của các thành viên nhóm | User không hiểu công dụng, liều dùng, tương tác — dẫn đến uống sai hoặc bỏ uống |

**Nhóm có phải user thật không?** Có — các thành viên đều từng nhận đơn thuốc và gặp khó khi đọc hiểu.

**Pain statement:**
> Bệnh nhân vừa nhận đơn thuốc gặp khó ở bước đọc và hiểu đơn, vì đơn viết tắt, chuyên môn, không có giải thích đi kèm, và quy trình tư vấn hiện tại của Long Châu yêu cầu chờ dược sĩ gọi lại — không có ngay. Hậu quả là uống thuốc sai cách, sai liều, hoặc bỏ uống vì không hiểu.

---

## 2. Lát cắt để build

**Một người dùng, một công việc, một quyết định AI, một kết quả:**

> Cho bệnh nhân vừa nhận đơn thuốc từ bác sĩ nhưng không hiểu cách dùng — AI đọc nội dung đơn thuốc (text hoặc ảnh chụp) và giải thích từng thuốc bằng ngôn ngữ thông thường, trả về bản tóm tắt ngắn gọn dạng bullet dễ đọc trên điện thoại.

**Kết quả cụ thể với mỗi thuốc:**
- Thuốc này dùng để làm gì
- Uống lúc nào, liều bao nhiêu
- Lưu ý quan trọng (không uống với gì, tác dụng phụ thường gặp)

---

## 3. AI Product Canvas

### Value — Giá trị
- **Dành cho ai:** Bệnh nhân sau khi rời phòng khám với đơn thuốc trên tay
- **Đau ở đâu:** Không hiểu tên thuốc, liều dùng, lưu ý — nhưng không có ai giải thích ngay lúc đó
- **AI giải được gì mà cách hiện tại chưa làm tốt:** Giải thích tức thì, bằng tiếng Việt thông thường, không cần chờ dược sĩ gọi lại

### Trust — Niềm tin
- **Khi AI trả lời sai**, người dùng nhận ra qua:
  - Cảnh báo rõ ràng khi AI không nhận ra tên thuốc: *"Không tìm thấy thông tin, vui lòng hỏi dược sĩ"*
  - Highlight đỏ khi phát hiện tương tác thuốc nguy hiểm kèm yêu cầu xác nhận với bác sĩ
  - Câu hỏi làm rõ thay vì tự đoán khi đơn mờ hoặc thiếu thông tin
- **Cách sửa:** User nhập thêm thông tin (dị ứng, bệnh nền) để AI điều chỉnh; hoặc chuyển sang dược sĩ thật

### Feasibility — Tính khả thi
- **Chi phí mỗi lượt gọi:** ~$0.01–0.03 tùy độ dài đơn (GPT-4o / Claude Haiku)
- **Độ trễ:** < 5 giây cho đơn thông thường (3–5 thuốc)
- **Dữ liệu cần có:** Tên thuốc, liều dùng từ đơn (text hoặc OCR từ ảnh)
- **Rủi ro lớn nhất:** AI bỏ sót tương tác thuốc nguy hiểm → xử lý bằng cảnh báo bắt buộc xác nhận với chuyên gia
- **Ngưỡng dừng:** Nếu độ chính xác nhận diện thuốc < 80% hoặc false negative trên tương tác thuốc > 5% trong test → không ship, yêu cầu human-in-the-loop hoàn toàn

### Tín hiệu học
- Khi user chỉnh sửa hoặc báo sai → lưu lại cặp (input đơn, correction) vào tập kiểm thử
- Dữ liệu correction giúp cải thiện prompt và phát hiện các loại thuốc AI thường nhầm

---

## 4. Tăng năng lực hay tự động hóa

**Quyết định: Augmentation (tăng năng lực)**

AI giải thích và gợi ý — user và dược sĩ giữ quyền quyết định cuối.

**Lý do:** Đơn thuốc liên quan trực tiếp đến sức khỏe. Sai có thể nguy hiểm và khó hoàn tác (đã uống thuốc). Con người giữ quyền quyết định ở bước hành động cuối — đặc biệt với tương tác thuốc hoặc case phức tạp.

**Human role:** reviewer / decider

---

## 5. Bốn đường đi của trải nghiệm

| Đường đi | Tình huống | Prototype xử lý thế nào |
|---|---|---|
| **Đường thuận** | Đơn rõ ràng, 3 thuốc thông dụng (Paracetamol, Amoxicillin, Omeprazole) | AI giải thích đúng, đủ, dễ hiểu — chấp nhận bằng một thao tác |
| **Khi AI không chắc** | Tên thuốc viết tắt hoặc không phổ biến | Hiển thị *"Không chắc chắn về thuốc này, vui lòng xác nhận với dược sĩ"* kèm tên gốc |
| **Khi AI sai** | AI không nhận ra thuốc hoặc phát hiện tương tác nguy hiểm | Cảnh báo highlight đỏ, không tự bịa thông tin, yêu cầu xác nhận với bác sĩ/dược sĩ |
| **Khi người dùng sửa** | User nhập thêm dị ứng, bệnh nền, hoặc chỉnh liều | AI cập nhật lưu ý phù hợp; dữ liệu correction được lưu lại |

---

## 6. Những kiểu lỗi đáng lo nhất

### Lỗi 1: Bỏ sót tương tác thuốc nguy hiểm
- **Xuất hiện khi nào:** Đơn có nhiều thuốc, hoặc tên thuốc viết generic thay vì brand name
- **Ai chịu thiệt và nặng đến đâu:** User — có thể gây phản ứng nghiêm trọng hoặc giảm hiệu quả điều trị
- **Xử lý:** Highlight đỏ + cảnh báo bắt buộc xác nhận với bác sĩ/dược sĩ; không cho phép bỏ qua

### Lỗi 2: Nhận diện sai tên thuốc (hallucination)
- **Xuất hiện khi nào:** Tên viết tắt, chữ mờ, hoặc thuốc không phổ biến tại Việt Nam
- **Ai chịu thiệt:** User — uống nhầm liều hoặc nhầm thuốc
- **Xử lý:** Hiển thị cảnh báo *"Không tìm thấy thông tin"*, không tự điền thông tin, hướng dẫn hỏi dược sĩ

### Lỗi 3: OCR đọc sai từ ảnh chụp mờ
- **Xuất hiện khi nào:** Ảnh chụp thiếu sáng, góc nghiêng, chữ tay khó đọc
- **Ai chịu thiệt:** User — nhận thông tin sai từ đầu
- **Xử lý:** Hỏi lại user xác nhận nội dung đọc được trước khi giải thích; cho phép chỉnh sửa text trước khi submit

---

## 7. Kế hoạch kiểm thử và bằng chứng demo

### Hai đầu vào chuẩn bị sẵn cho demo

**Đầu vào 1 — Đường thuận:**
```
Paracetamol 500mg - uống 1 viên x 3 lần/ngày sau ăn
Amoxicillin 500mg - uống 1 viên x 3 lần/ngày, uống hết liều
Omeprazole 20mg - uống 1 viên trước ăn sáng
```

**Đầu vào 2 — Đường khó (tương tác thuốc):**
```
Warfarin 5mg - uống 1 viên/ngày
Aspirin 100mg - uống 1 viên/ngày
```
*(Cặp này có tương tác nguy hiểm — AI phải cảnh báo rõ)*

### Bằng chứng cần có trong repo
- [ ] Ảnh chụp màn hình 4 path đã chạy thật
- [ ] Nhật ký prompt đã dùng (prompt engineering log)
- [ ] Danh sách test case và kết quả (bao gồm failure path)
- [ ] Ghi chú những đánh đổi đã cân nhắc khi quyết định thiết kế

---

## 8. Phân công

| Thành viên | Phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| **Hồ Đức Minh** | SPEC + Product Canvas + slides | `spec/spec.md` hoàn chỉnh, `spec/demo-slides.pdf` |
| **Nguyễn Thành Huy** | Code core flow (AI integration) | Code chạy được, demo 4 path |
| **Nguyễn Đức Hiếu** | UI/UX + demo script + error cases | Giao diện hoàn chỉnh, kịch bản demo, ghi lại kết quả error cases |

---

*Phiên bản: Day 06 — Nhóm C3 (E403)*
