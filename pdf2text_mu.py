import fitz  # PyMuPDF

# 打开PDF文件
pdf_file_path = "senior_physics_textbooks/senior_optional_2.pdf"
doc = fitz.open(pdf_file_path)

# 提取所有文字
all_text = ""
for page in doc:
    all_text += page.get_text()

# 保存到文件
with open("so2_output.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("文字提取完成，已保存到 so2_output.txt")