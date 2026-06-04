# Thin SPEC — Nhóm Thiếu Thuốc

## 1. Track, product/app và user

**Track:** Healthcare / Y tế
**Product/app thật:** Nhà Thuốc Long Châu (nhathuoclongchau.com.vn)
**User cụ thể:** Bệnh nhân vừa nhận đơn thuốc từ bác sĩ nhưng không hiểu cách dùng
**Nhóm có phải user thật không? Nếu không, khác ở đâu?** Có — các thành viên trong nhóm đều từng nhận đơn thuốc và gặp khó khăn khi đọc hiểu

## 2. Evidence summary

| Evidence | Nguồn | User/pain nói lên điều gì? | SPEC phải đổi gì? |
|---|---|---|---|
| Long Châu yêu cầu điền form + chờ dược sĩ gọi lại, không có giải thích tức thì | https://nhathuoclongchau.com.vn/don-thuoc | User cần câu trả lời ngay, quy trình hiện tại chậm và phụ thuộc người thật | Prototype phải trả lời tức thì, không cần chờ |
| Không có app y tế VN nào giải thích đơn thuốc bằng ngôn ngữ thông thường | Khảo sát competitor: Long Châu, Jio Health, Ada Health | Đây là cơ hội trống — pain có thật nhưng chưa ai giải quyết | Giữ nguyên build slice |
| Đơn thuốc thường viết tắt, chuyên môn, không có giải thích đi kèm | Self-use | User không hiểu công dụng, liều dùng, tương tác thuốc | AI cần giải thích bằng ngôn ngữ thông thường |

## 3. Pain statement

```text
User là bệnh nhân vừa nhận đơn thuốc đang gặp khó ở bước đọc và hiểu đơn thuốc,
vì đơn thuốc viết tắt, chuyên môn, không có giải thích đi kèm,
và quy trình tư vấn hiện tại của Long Châu yêu cầu chờ dược sĩ gọi lại — không có ngay,
dẫn tới uống thuốc sai cách, sai liều, hoặc bỏ uống vì không hiểu.
Bằng chứng chính là quy trình tư vấn tại https://nhathuoclongchau.com.vn/don-thuoc
và không có app y tế VN nào giải quyết pain này.
```

## 4. Build slice

```text
Cho bệnh nhân vừa nhận đơn thuốc từ bác sĩ nhưng không hiểu cách dùng,
prototype sẽ dùng AI để đọc nội dung đơn thuốc (text hoặc ảnh chụp)
và giải thích từng thuốc bằng ngôn ngữ thông thường:
  - Thuốc này dùng để làm gì
  - Uống lúc nào, liều bao nhiêu
  - Lưu ý quan trọng (không uống với gì, tác dụng phụ thường gặp)
tạo ra bản tóm tắt ngắn gọn dạng bullet, dễ đọc trên điện thoại,
và xử lý failure mode bằng:
  - Nếu AI không nhận ra tên thuốc → hiển thị cảnh báo "Không tìm thấy thông tin, vui lòng hỏi dược sĩ"
  - Nếu phát hiện tương tác thuốc nguy hiểm → highlight đỏ và yêu cầu xác nhận với bác sĩ
  - Nếu đơn mờ/thiếu thông tin → hỏi lại user thay vì tự đoán
```

## 5. Auto/Aug decision

Chọn một:

- [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
- [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
- [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:** Đơn thuốc liên quan trực tiếp đến sức khỏe — sai có thể nguy hiểm. AI giải thích và gợi ý, nhưng user/dược sĩ giữ quyền quyết định cuối, đặc biệt với tương tác thuốc hoặc case phức tạp.
**Human role:** reviewer / decider

## 6. Four paths

| Path | Prototype phải thể hiện gì? |
|---|---|
| Happy | Đơn rõ ràng, 3 thuốc thông dụng → AI giải thích đúng, đủ, dễ hiểu |
| Low-confidence | Tên thuốc viết tắt hoặc không phổ biến → AI hiển thị "không chắc, vui lòng xác nhận với dược sĩ" |
| Failure | AI giải thích sai liều hoặc không nhận ra thuốc → cảnh báo rõ, không tự bịa |
| Correction | User nhập thêm thông tin (dị ứng, bệnh nền) → AI điều chỉnh lưu ý phù hợp |

## 7. Failure mode nguy hiểm nhất

```text
Nếu user nhập đơn có tương tác thuốc nguy hiểm,
AI có thể bỏ sót hoặc không nhận ra tương tác,
hậu quả là user uống thuốc sai gây hại cho sức khỏe.
Prototype sẽ xử lý bằng: highlight đỏ cảnh báo tương tác + yêu cầu xác nhận với bác sĩ/dược sĩ.
Owner kiểm thử path này là Hồ Đức Minh.
```

## 8. Owner plan cho sáng Day 06

| Thành viên | Việc phụ trách | Bằng chứng cần có trong repo |
|---|---|---|
| Nguyễn Đức Hiếu | Research / evidence + SPEC | thin-spec.md hoàn chỉnh |
| Nguyễn Thành Huy | Prototype core (AI integration) | app.py, modules/llm.py, RxNorm/OpenFDA |
| Hồ Đức Minh | Drug interaction + risk engine + test failure path | drug_interaction.py, risk_engine.py |
