import pdfplumber
import argparse
def extract_modules_by_fonts(pdf_path):
    """
    根据字体样式和位置提取模块内容。
    """
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            # 提取每个字符的字体和大小
            for char in page.chars:
                print(f"文字: {char['text']}, 字体: {char['fontname']}, 大小: {char['size']}")
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析 PDF 文件并生成 SQL")
    parser.add_argument("--input", default="senior_physics_textbooks/senior_optional_3.pdf", help="输入 PDF 文件路径")
    args = parser.parse_args()
    extract_modules_by_fonts(args.input)