import pdfplumber
import re

def is_chinese(char):
    """判断一个字符是否是汉字"""
    return '\u4e00' <= char <= '\u9fff'

def calculate_font_proportion(sentence, target_font, target_size):
    """
    计算句子中满足指定字体和字号的字符比例
    :param sentence: 当前句子（包含字符、字体和字号的列表）
    :param target_font: 目标字体
    :param target_size: 目标字号
    :return: 满足条件的字符比例（0~1）
    """
    if not sentence:
        return 0
    matching_count = sum(1 for char, font, size in sentence if font == target_font and size == target_size)
    return matching_count / len(sentence)

def extract_sentences_with_font_conditions(pdf_path, target_font, target_size):
    """
    从 PDF 中精细提取文本，并根据字体和关键词过滤条件处理句子。
    
    :param pdf_path: PDF 文件路径
    :param target_font: 目标字体名称
    :param target_size: 目标字体大小
    :return: 满足条件的句子列表
    """
    filtered_sentences = []

    # 打开 PDF 文件
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取页面中的字符块
            chars = page.chars  # 获取页面中的每个字符及其字体信息
            if not chars:
                continue

            # 初始化当前句子和前一个字符的字体信息
            current_sentence = []
            previous_font = None
            previous_size = None
            space = False

            for char in chars:
                text = char.get("text", "")
                font = char.get("fontname", "")
                size = round(char.get("size", 0), 1)  # 舍入到 1 位小数

                # 跳过空格字符
                if text.strip() == "":
                    space = True
                    continue

                # 判断是否需要分割句子
                if (
                    previous_font is not None
                    and previous_size is not None
                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                    and space == True
                ):
                    # print(current_sentence)
                    # print("text is: "+text)
                    # 检查前后都是汉字的情况
                    if current_sentence and is_chinese(current_sentence[-1][0]):
                        # 如果字体变化且后面是汉字，分割句子并保留后半部分
                        current_sentence = [(text, font, size)]
                        previous_font = font
                        previous_size = size
                        space = False  # 重置空格标志
                        # print("situation1——text is: "+text)
                        continue
                elif (
                    previous_font is not None
                    and previous_size is not None
                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                    and space == False
                ):
                    if current_sentence and is_chinese(text) and is_chinese(current_sentence[-1][0]):
                        # 如果字体变化且前后都是汉字，分割句子并保留后半部分
                        current_sentence = [(text, font, size)]
                        previous_font = font
                        previous_size = size
                        space = False  # 重置空格标志
                        # print("situation2——text is: "+text)
                        continue

                # 添加当前字符到当前句子
                current_sentence.append((text, font, size))
                # print(text, font, size)
                previous_font = font
                previous_size = size
                # print("text is: "+text,"current_sentence is: "+str(current_sentence))
                # 如果遇到句子结束符，结束当前句子
                if text in "。！？":
                    proportion = calculate_font_proportion(current_sentence, target_font, target_size)
                    # print("proportion is "+str(proportion))
                    if proportion >= 0.8:  # 字体比例需超过 80%
                        sentence_text = "".join([c[0] for c in current_sentence])
                        filtered_sentences.append(sentence_text)
                        # print(sentence_text)
                        
                    current_sentence = []
                    
                space = False  # 重置空格标志


    # 过滤不符合条件的句子
    result_sentences = []
    for sentence_text in filtered_sentences:
        # 检查是否包含逗号，且第一个逗号前只有一个字
        if "，" in sentence_text:  # 中文逗号
            first_comma_index = sentence_text.index("，")
            if first_comma_index == 1:  # 第一个逗号前只有一个字符（下标为1表示只有一个字）
                continue  # 排除该句子
            
        if len(sentence_text) < 10:
            continue
        
        # 检查关键词过滤条件
        if not re.search(r"你|我|他|它|图|这|编写|册|索引|例如|下表|表格|表1|表2|表3|[a-zA-Z]|？", sentence_text) and \
           not sentence_text.startswith("但") and \
           not sentence_text.startswith("可见") and \
           not sentence_text.startswith("于是") and \
           not sentence_text.startswith("当时") and \
           not sentence_text.startswith("此时") and \
           not sentence_text.startswith("从此") and \
           not sentence_text.startswith("后来") and \
           not sentence_text.startswith("以后") and \
           not sentence_text.startswith("因此") and \
           not sentence_text.startswith("为此") and \
           not sentence_text.startswith("当然") and \
           not sentence_text.startswith("然而") and \
           not sentence_text.startswith("另外") and \
           not sentence_text.startswith("反之") and \
           not sentence_text.startswith("此外") and \
           not sentence_text.startswith("此后") and \
           not sentence_text.startswith("前面") and \
           not sentence_text.startswith("上面") and \
           not sentence_text.startswith("上述") and \
           not sentence_text.startswith("原来") and \
           not sentence_text.startswith("所以") and \
           not sentence_text.startswith("不过") and \
           not sentence_text.startswith("再如") and \
           not sentence_text.startswith("第一") and \
           not sentence_text.startswith("第二") and \
           not sentence_text.startswith("第三") and \
           not sentence_text.startswith("一方面") and \
           not sentence_text.startswith("类似地") and \
           not sentence_text.startswith("由此可") and \
           not sentence_text.startswith("也就是说") and \
           not sentence_text.startswith("换句话说") and \
           not sentence_text.startswith("另一方面") and \
           not sentence_text.startswith("实验结果") and \
           not sentence_text.startswith("与此类似"):
            result_sentences.append(sentence_text)

    return result_sentences


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