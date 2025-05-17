import re
import fitz  # PyMuPDF
import pdfplumber

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

def check_sentence(sentence_text):
    if "，" in sentence_text:  # 中文逗号
        first_comma_index = sentence_text.index("，")
        if first_comma_index == 1:  # 第一个逗号前只有一个字符（下标为1表示只有一个字）
            return False  # 排除该句子
        
    if len(sentence_text) < 10:
        return False
    
    # 检查关键词过滤条件
    if not re.search(r"你|我|他|它|图|这|编写|册|索引|例如|下表|表格|表1|表2|表3|[a-zA-Z]|？", sentence_text) and \
        not sentence_text.startswith("但") and \
        not sentence_text.startswith("再") and \
        not sentence_text.startswith("可见") and \
        not sentence_text.startswith("所示") and \
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
        not sentence_text.startswith("第一") and \
        not sentence_text.startswith("第二") and \
        not sentence_text.startswith("第三") and \
        not sentence_text.startswith("如此") and \
        not sentence_text.startswith("可是") and \
        not sentence_text.startswith("一方面") and \
        not sentence_text.startswith("类似地") and \
        not sentence_text.startswith("由此可") and \
        not sentence_text.startswith("也就是说") and \
        not sentence_text.startswith("换句话说") and \
        not sentence_text.startswith("另一方面") and \
        not sentence_text.startswith("实验结果") and \
        not sentence_text.startswith("与此类似"):
        return True

def extract_catalog_and_chapters_with_pages(pdf_path, output_sql_path):
    """
    从 PDF 文件中提取目录页信息，包括章节标题、小节标题及其对应页码，并生成 SQL 插入语句。
    :param pdf_path: PDF 文件路径
    :param output_sql_path: 输出 SQL 文件路径
    """
    # 用 PyMuPDF 提取完整的目录页文本
    with fitz.open(pdf_path) as doc:
        catalog_text = ""
        for page in doc:
            text = page.get_text("text")
            if "目  录" in text:
                catalog_text = text
                break

        if not catalog_text:
            print("未找到目录页")
            return

    # 将目录文本按行分割
    catalog_lines = catalog_text.splitlines()

    # Step 1: 提取页码列表
    page_numbers = []
    remaining_lines = []
    start = False
    for line in catalog_lines:
        stripped_line = line.strip()
        if "目  录" in line:
            start = True
            continue
        if start:
            if stripped_line.isdigit():  # 判断是否为数字页码
                page_numbers.append(int(stripped_line))
            else:
                remaining_lines.append(stripped_line)

    # Step 2: 解析章节和小节标题
    chapters = []
    current_chapter = None
    page_index = 0  # 页码列表的索引
    for line in remaining_lines:
        line = line.strip()

        # 检查是否是章节标题（如 "第一章 分子动理论"）
        if line.startswith("第") and "章" in line:
            # 如果当前章节未结束，保存到章节列表
            if current_chapter:
                chapters.append(current_chapter)
                
            # 使用正则表达式删除开头的 "第某某章" 和空格
            chapter_title = re.sub(r"^第.*?章\s*", "", line)
            
            # 创建新章节
            current_chapter = {
                "title": chapter_title,
                "page": page_numbers[page_index],
                "sections": []
            }
            page_index += 1  # 页码索引递增

        # 检查是否是小节标题（如 "1. 分子动理论的基本内容"）
        elif current_chapter and line[0].isdigit() and "." in line:
            # 使用正则表达式删除开头的 "数字. "（包括空格）
            section_title = re.sub(r"^\d+\.\s*", "", line)
            current_chapter["sections"].append({
                "title": section_title,
                "page": page_numbers[page_index]
            })
            page_index += 1  # 页码索引递增

    # 添加最后一个章节
    if current_chapter:
        chapters.append(current_chapter)

    # Step 3: 打印章节和页码信息
    for chapter in chapters:
        print(f"章节: {chapter['title']} (起始页: {chapter['page']})")
        for section in chapter["sections"]:
            print(f"  小节: {section['title']} (页码: {section['page']})")

        
    with open(output_sql_path, "a", encoding="utf-8") as sql_file:                      
        # Step 4: 解析 PDF 字符内容
        filtered_sentences = []
        with pdfplumber.open(pdf_path) as pdf:
            for chapter_index, chapter in enumerate(chapters):
                # 插入章信息到 SQL文件
                chapter_id = f"010102{str(chapter_index+1).zfill(2)}000000"
                chapter_code = f"CH{str(chapter_index+1).zfill(2)}"
                sql_file.write("\n")
                sql_file.write(
                    f"INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id) \n"
                    f"VALUES \n"
                    f"('{chapter_id}', 'PHYSICS', 'SENIOR', 'TERM_2', "
                    f"'{chapter_code}', '{chapter['title']}', '', NULL),\n"
                )
                
                for section_index, section in enumerate(chapter["sections"]):
                    # 插入节信息到 SQL文件
                    section_id = f"010102{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}0000"
                    section_code = f"{chapter_code}.SEC{str(section_index+1).zfill(2)}"
                    sql_file.write(
                        f"('{section_id}', 'PHYSICS', 'SENIOR', 'TERM_2', "
                        f"'{section_code}', '{section['title']}', '', '{chapter_id}'),\n"
                    )
                    
                    # 计算起始页和结束页
                    start_page = section["page"] + 4  # 偏移计算，得到真实的当前页数，而非页面中标注的
                    if chapter_index == len(chapters) - 1 and section_index == len(chapter["sections"]) - 1:
                        end_page = len(pdf.pages) - 1
                    elif section_index == len(chapter["sections"]) - 1:
                        end_page = chapters[chapter_index+1]["page"] - 1 + 4
                    else:
                        end_page = chapter["sections"][section_index + 1]["page"] - 1 + 4

                    print(f"\n解析小节: {section['title']} (起始页: {start_page}, 结束页: {end_page})")
                    
                    knowledge_points = []
                    current_knowledge_point = None
                    kp_index = 0
                    q_index = 0
                    for page_number in range(start_page, end_page + 1):
                        current_page = pdf.pages[page_number]
                        char_index = 0
                        
                        # 初始化当前句子和前一个字符的字体信息
                        current_sentence = []
                        previous_font = None
                        previous_size = None
                        space = False
                        
                        while char_index < len(current_page.chars):
                            char = current_page.chars[char_index]
                            
                            # 检查字体和大小是否符合知识点标题的条件
                            if char.get("fontname") == "DXJOEH+FZLTZHK--GBK1-0" and round(char.get("size")) == 14 and char.get("text") != "问" and char.get("text") != "题":
                                # 如果当前有未结束的知识点标题，保存到知识点列表
                                if current_knowledge_point:
                                    knowledge_points.append(current_knowledge_point)

                                # 开始扫描完整的知识点标题
                                kp_title = char["text"]  # 初始化知识点标题
                                last_scanned_index = char_index  # 记录当前索引
                                for next_char_index in range(char_index + 1, len(current_page.chars)):
                                    next_char = current_page.chars[next_char_index]
                                    # 如果字体和大小与知识点标题一致，则继续拼接标题
                                    if next_char.get("fontname") == "DXJOEH+FZLTZHK--GBK1-0" and round(next_char.get("size")) == 14:
                                        kp_title += next_char["text"]
                                        last_scanned_index = next_char_index  # 更新最后扫描的索引
                                    else:
                                        # 字体或大小不一致时，结束扫描
                                        break

                                # 创建章节标题的字典
                                current_knowledge_point = {
                                    "title": kp_title.strip(),  # 去除多余空格
                                    "options": []
                                }
                                print(f"知识点标题: {current_knowledge_point['title']}")  # 打印知识点标题
                                
                                # 插入知识点信息到 SQL文件
                                kp_id = f"010102{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}{str(kp_index+1).zfill(2)}00"
                                kp_code = f"{section_code}.KP{str(kp_index+1).zfill(2)}"
                                sql_file.write(
                                    f"('{kp_id}', 'PHYSICS', 'SENIOR', 'TERM_2', "
                                    f"'{kp_code}', '{current_knowledge_point['title']}', '', '{section_id}'),\n"
                                )
                                kp_index += 1  # 更新知识点索引
                                op_index = 0  # 重置题目索引
                                
                                # 更新外层循环的索引，跳过已扫描的字符
                                char_index = last_scanned_index
                                previous_font = "DXJOEH+FZLTZHK--GBK1-0"
                                previous_size = 14
                            # 检查知识点中的正文，是否符合条件
                            elif current_knowledge_point:
                                text = char.get("text", "")
                                font = char.get("fontname", "")
                                size = round(char.get("size", 0), 1)  # 舍入到 1 位小数
                                # print(f"text is: {text}, font is: {font}, size is: {size}")  # 打印当前字符的信息
                                
                                # 跳过空格字符
                                if text.strip() == "":
                                    space = True
                                    char_index += 1
                                    continue

                                # 判断是否需要分割句子
                                if (
                                    previous_font is not None
                                    and previous_size is not None
                                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                                    and space == True
                                ):
                                    # print(current_sentence)
                                    # print("1")
                                    # 检查前后都是汉字的情况
                                    if current_sentence and is_chinese(current_sentence[-1][0]):
                                        # 如果字体变化且后面是汉字，分割句子并保留后半部分
                                        current_sentence = [(text, font, size)]
                                        previous_font = font
                                        previous_size = size
                                        space = False  # 重置空格标志
                                        # print("situation1——text is: "+text)
                                        char_index += 1
                                        continue
                                elif (
                                    previous_font is not None
                                    and previous_size is not None
                                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                                    and space == False
                                ):
                                    # print("2")
                                    if current_sentence and is_chinese(text) and is_chinese(current_sentence[-1][0]):
                                        # 如果字体变化且前后都是汉字，分割句子并保留后半部分
                                        current_sentence = [(text, font, size)]
                                        previous_font = font
                                        previous_size = size
                                        space = False  # 重置空格标志
                                        # print("situation2——text is: "+text)
                                        char_index += 1
                                        continue

                                # 添加当前字符到当前句子
                                current_sentence.append((text, font, size))
                                # print(current_sentence)
                                # print(text, font, size)
                                previous_font = font
                                previous_size = size
                                # print("text is: "+text,"current_sentence is: "+str(current_sentence))
                                # 如果遇到句子结束符，结束当前句子
                                if text in "。！？":
                                    proportion = calculate_font_proportion(current_sentence, "GYKJDL+FZSSK--GBK1-0", 12)
                                    # print("proportion is "+str(proportion))
                                    if proportion >= 0.8:  # 字体比例需超过 80%
                                        sentence_text = "".join([c[0] for c in current_sentence])
                                        if check_sentence(sentence_text):
                                            filtered_sentences.append(sentence_text)
                                            # 插入选项信息到 SQL文件
                                            op_id = f"010102{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}{str(kp_index+1).zfill(2)}{str(op_index+1).zfill(2)}"
                                            op_code = f"{kp_code}.OP{str(op_index+1).zfill(2)}"
                                            sql_file.write(
                                                f"('{op_id}', 'PHYSICS', 'SENIOR', 'TERM_2', "
                                                f"'{op_code}', '{sentence_text}', '', '{kp_id}'),\n"
                                            )
                                            op_index += 1  # 更新知识点索引
                                            print(sentence_text)
                                        
                                    current_sentence = []
                                space = False  # 重置空格标志

                            char_index += 1
                        # 添加最后一个章节（如果有）
                    if current_knowledge_point:
                        knowledge_points.append(current_knowledge_point)
                    print(knowledge_points)

# 示例用法
pdf_path = "senior_physics_textbooks/senior_2.pdf"  # 替换为你的 PDF 文件路径
output_sql_path = "sql/phy_senior.sql"
extract_catalog_and_chapters_with_pages(pdf_path, output_sql_path)
