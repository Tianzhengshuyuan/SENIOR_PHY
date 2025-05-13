import pdfplumber
import re

def extract_sentences_with_font_conditions(pdf_path, target_font, target_size):
    """
    从 PDF 中提取文本，并根据字体和关键词过滤条件处理句子。
    
    :param pdf_path: PDF 文件路径
    :param target_font: 目标字体名称
    :param target_size: 目标字体大小
    :return: 满足条件的句子列表
    """
    filtered_sentences = []

    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取页面中的文本块
            chars = page.chars  # 获取每个字符的字体信息
            if not chars:
                continue

            # 将页面字符按顺序拼接成完整句子，保留字体信息
            sentence_data = []
            current_sentence = []
            for char in chars:
                text = char.get("text", "")
                font = char.get("fontname", "")
                size = char.get("size", 0)

                # 判断是否是句子结束符
                if text in "。！？":
                    current_sentence.append((text, font, size))
                    sentence_data.append(current_sentence)
                    current_sentence = []
                else:
                    current_sentence.append((text, font, size))

            # 处理每个句子
            for sentence in sentence_data:
                # 获取句子的文字部分
                sentence_text = "".join([char[0] for char in sentence])

                # 检查字体和大小是否满足条件
                font_match_count = sum(
                    1 for char in sentence
                    if char[1] == target_font and char[2] == target_size
                )
                # if font_match_count > 0:
                #     print(sentence,end=": ")
                #     print(font_match_count / len(sentence))
                if font_match_count / len(sentence) >= 0.8:
                    # 检查关键词过滤条件
                    if not re.search(r"你|我|他|它|例如|图|表|这|编写|本册|[a-zA-Z]|？", sentence_text) and \
                       not sentence_text.startswith("可见") and \
                       not sentence_text.startswith("当时") and \
                       not sentence_text.startswith("此时") and \
                       not sentence_text.startswith("由此可见") and \
                       not sentence_text.startswith("从此") and \
                       not sentence_text.startswith("换句话说") and \
                       not sentence_text.startswith("也就是说") and \
                       not sentence_text.startswith("后来") and \
                       not sentence_text.startswith("但是") and \
                       not sentence_text.startswith("换句话说") and \
                       not sentence_text.startswith("因此") and \
                       not sentence_text.startswith("为此") and \
                       not sentence_text.startswith("当然") and \
                       not sentence_text.startswith("然而") and \
                       not sentence_text.startswith("类似地") and \
                       not sentence_text.startswith("与此类似") and \
                       not sentence_text.startswith("一方面") and \
                       not sentence_text.startswith("另一方面") and \
                       not sentence_text.startswith("另外") and \
                       not sentence_text.startswith("反之") and \
                       not sentence_text.startswith("此外") and \
                       not sentence_text.startswith("所以") and \
                       not sentence_text.startswith("再如") and \
                       not sentence_text.startswith("第一") and \
                       not sentence_text.startswith("第二") and \
                       not sentence_text.startswith("第三") and \
                       not sentence_text.startswith("不过"):
                        filtered_sentences.append(sentence_text)

    return filtered_sentences


# PDF 文件路径
pdf_path = "senior_optional_3.pdf"

# 目标字体和大小
target_font = "GSQGML+FZSSK--GBK1-0"
target_size = 12.0

# 提取满足条件的句子
result_sentences = extract_sentences_with_font_conditions(pdf_path, target_font, target_size)

# 输出结果
print("满足条件的句子：")
for sentence in result_sentences:
    print(sentence)