from PyPDF2 import PdfReader

def check_tags(pdf_path):
    """
    检查 PDF 文件是否包含结构化标签。
    """
    reader = PdfReader(pdf_path)
    if "/MarkInfo" in reader.metadata:
        print("PDF 包含结构化标签（Tagged PDF）。")
    else:
        print("PDF 不包含结构化标签。")

# 示例使用
pdf_path = "senior_optional_3.pdf"  # 替换为你的 PDF 文件路径
check_tags(pdf_path)