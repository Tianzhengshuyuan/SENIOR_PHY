import pdfplumber

def extract_section_text(pdf_path, section_title):
    """
    提取 PDF 中特定标题模块的所有文本。

    :param pdf_path: PDF 文件路径
    :param section_title: 要提取的模块标题（如 "练习与应用"）
    :return: 提取的模块文本
    """
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取页面中的所有文本
            text = page.extract_text()
            if section_title in text:
                # 找到包含特定标题的部分
                lines = text.split('\n')  # 按行分割文本
                start_extracting = False
                for line in lines:
                    if section_title in line:
                        start_extracting = True  # 开始提取
                    elif start_extracting and line.strip() == "":  # 遇到空行时停止提取
                        break
                    elif start_extracting:
                        extracted_text.append(line.strip())
    return "\n\n".join(extracted_text)

# 示例用法
pdf_path = "senior_optional_3.pdf"  # 替换为你的 PDF 文件路径
section_title = "问题"  # 模块标题
module_text = extract_section_text(pdf_path, section_title)

# 输出提取的文本
print("提取的模块文本：")
print(module_text)