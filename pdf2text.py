from PyPDF2 import PdfReader

# 打开PDF文件
pdf_file_path = "senior_optional_3.pdf"
reader = PdfReader(pdf_file_path)

# 提取所有文字
all_text = ""
for page in reader.pages:
    all_text += page.extract_text()

# 保存到文件
with open("so3_output.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("文字提取完成，已保存到 so3_output.txt")