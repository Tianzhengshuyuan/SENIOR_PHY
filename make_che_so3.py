import re
import fitz  # PyMuPDF
import pdfplumber
import os
import openai
import argparse
from openai import OpenAI
from mistralai import Mistral
from volcenginesdkarkruntime import Ark

# 配置 DeepSeek API 客户端
deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")
doubao_client = Ark(api_key="196b33be-8abb-4af3-9fba-6e266b2dd942")
mistral_client = Mistral(api_key="zWUDyBGqEIdJAtJoxnsr6ACcLTgz1auH")

TITLE_FONT = "XNKZPT+FZLTZHK--GBK1-0"
TITLE_SIZE = 14
BODY_FONT = "GSQGML+FZSSK--GBK1-0"
BODY_SIZE = 12
PAGE_FONT = "SPHFXD+FZZDXJW--GB1-0"
TERM_FONT = "XNKZPT+FZLTZHK--GBK1-0"
TERM_SIZE = 12
BRACKET_FONT = "GSQGML+FZSSK--GBK1-0"
BRACKET_SIZE = 12
PARA_FONT = "SQAQXD+FZKTK--GBK1-0"

def is_chinese(char):
    """判断一个字符是否是汉字"""
    return '\u4e00' <= char <= '\u9fff'

def save_text(sentence):
    """保存文本到文件"""
    sentence_text = "".join([c[0] for c in sentence])
    with open("texts.txt", "a", encoding="utf-8") as f:
        f.write(sentence_text + "\n")
        
def call_deepseek_api(question):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"
   
def call_gpt_api(question):
    """
    调用 gpt API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    os.environ["HTTP_PROXY"] = "http://localhost:7890"
    os.environ["HTTPS_PROXY"] = "http://localhost:7890"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败" 

def call_kimi_api(question):
    """
    调用 Kimi API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = kimi_client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "API 调用失败"
    
def call_doubao_api(question):
    """
    调用 豆包 API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = doubao_client.chat.completions.create(
            model="doubao-1.5-pro-32k-250115",
            # model="doubao-1.5-thinking-pro-250415",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 豆包 API 时出错: {e}")
        return "API 调用失败"
    

def call_mistral_api(question):
    """
    调用 Mistral API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = mistral_client.chat.complete(
            model="mistral-large-2407",
            # model="mistral-medium-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            temperature=args.temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Mistral API 时出错: {e}")
        return "API 调用失败"
    
def gen_multi_sentence(knowledge_point, sql_file, api_name="deepseek", temperature=0.5):
    chapter_index = knowledge_point['chaptor_index']
    section_index = knowledge_point['section_index']
    kp_index = knowledge_point['kp_index']
    kp_id = knowledge_point['kp_id']
    kp_code = knowledge_point['kp_code']
    
    full_text = '\n'.join(knowledge_point['options'])
        
    prompt = """任务描述：
            从提供的文本中提取适合用作物理学科选择题的条目。每个条目应该是一个完整且独立的物理学事实或规律。请严格按照以下步骤处理文本：
            第1步：跳过无关内容：
            遍历所有句子，忽略与物理规律或事实无关的句子，例如那些仅描述操作步骤的句子（如“下面我们做一个类似的实验”）。
            第2步：跳过错误内容：
            再次遍历所有句子，忽略本身有问题的句子，例如“第一章分子动理论3家用扫描隧道显微镜拍摄的石墨表面的原子”。
            第3步：跳过未知变量：
            再次遍历所有句子，跳过包含变量的句子，例如“当r＝r0时，分子间的作用力F为0，这个位置称为平衡位置。”，只要遇到变量就跳过该句子。   
            第4步：句子的完整性：
            再次遍历所有句子，如果一个句子能够独立表达完整的意思，则单独作为一个条目。
            如果一个句子指代前文或者和前文有因果关系，包含“例如”、“这”、“再如”、“可见”、“因此”等关键词，特别是以这些词开头，则需要与前面的句子结合为一个条目，以表达完整意思。例如“观察布朗运动，温度越高，悬浮微粒的运动就越明显。”和“可见，分子的无规则运动与温度有关系，温度越高，这种运动越剧烈。”应该合并到一个条目。
            第5步：条目的编号：
            给每个合格的条目前应添加序号，从“1. ”开始。

            示例：
            针对下面双引号中的文本：
            “ 我们知道，1mol水中含有水分子的数量就达6.02×1023个。
            ②这足以表明，组成物体的分子是大量的。
            人们用肉眼无法直接看到分子，就是用高倍的光学显微镜也看不到。
            直至1982年，人们研制了能放大几亿倍的扫描隧道显微镜③，才观察到物质表面原子的排列。
            第一章分子动理论3家用扫描隧道显微镜拍摄的石墨表面的原子，图中每个亮斑都是一个碳原子。
            从许多实验和生活现象中我们都会发现，不同种物质能够彼此进入对方。
            在物理学中，人们把这类现象叫作扩散（diffusion）。
            扩散现象并不是外界作用（例如对流、重力作用等）引起的，也不是化学反应的结果，而是由物质分子的无规则运动产生的。
            扩散现象是物质分子永不停息地做无规则运动的证据之一。
            扩散现象在科学技术中有很多应用。
            例如，在生产半导体器件时，需要在纯净半导体材料中掺入其他元素。
            这一过程可以在高温条件下通过分子的扩散来完成。
            19世纪初，一些人观察到，悬浮在液体中的小颗粒总在不停地运动。
            1827年，英国植物学家布朗首先在显微镜下研究了这种运动。
            下面我们做一个类似的实验。”
            应该整理成下面的形式：
            1. 我们知道，1mol水中含有水分子的数量就达6.02×1023个。这足以表明，组成物体的分子是大量的。
            2. 人们用肉眼无法直接看到分子，就是用高倍的光学显微镜也看不到。直至1982年，人们研制了能放大几亿倍的扫描隧道显微镜，才观察到物质表面原子的排列。
            3. 从许多实验和生活现象中我们都会发现，不同种物质能够彼此进入对方。在物理学中，人们把这类现象叫作扩散（diffusion）。
            4. 扩散现象并不是外界作用（例如对流、重力作用等）引起的，也不是化学反应的结果，而是由物质分子的无规则运动产生的。
            5. 扩散现象是物质分子永不停息地做无规则运动的证据之一。
            6. 扩散现象在科学技术中有很多应用。例如，在生产半导体器件时，需要在纯净半导体材料中掺入其他元素。这一过程
            可以在高温条件下通过分子的扩散来完成。
            7. 19世纪初，一些人观察到，悬浮在液体中的小颗粒总在不停地运动。1827年，英国植物学家布朗首先在显微镜下研究了这种运动。

            根据任务描述和示例，整理下面文本，只输出整理好的文本即可：
            """
    send_text = prompt + full_text
    
    if args.api == "deepseek":
        response = call_deepseek_api(send_text)
    elif args.api == "gpt":
        response = call_gpt_api(send_text)
    elif args.api == "kimi":
        response = call_kimi_api(send_text)
    elif args.api == "doubao":
        response = call_doubao_api(send_text)
    elif args.api == "mistral":
        response = call_mistral_api(send_text)
        
    print("response is: "+response)
    # 使用正则表达式匹配并去除编号
    result_lines = []
    for line in response.split('\n'):
        line = line.strip()
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            content = m.group(2)
            if content.startswith("他"):
                continue
            if re.search(r"栏目", content):
                continue
            result_lines.append(content)

    for op_index, sentence_text in enumerate(result_lines):
        # 插入选项信息到 SQL文件
        op_id = f"010106{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}{str(kp_index+1).zfill(2)}{str(op_index+1).zfill(2)}"
        op_code = f"{kp_code}.OP{str(op_index+1).zfill(2)}"
        sql_file.write(
            f"('{op_id}', 'PHYSICS', 'SENIOR', 'TERM_6', "
            f"'{op_code}', '{sentence_text}', '', '{kp_id}'),\n"
        )
        # print(sentence_text)
def calculate_font_proportion(sentence):
    if not sentence:
        return 0

    matching_count = 0
    i = 0
  
    while i < len(sentence):
        char, font, size = sentence[i]

        # 查看是否是普通正文字体
        if font == BODY_FONT and size == BODY_SIZE:
            matching_count += 1

        # 查看是否是定义概念时使用的字体
        elif font == TERM_FONT and size == TERM_SIZE:
            start = i
            while i < len(sentence) and sentence[i][1] == TERM_FONT and sentence[i][2] == TERM_SIZE:
                i += 1
            if i < len(sentence) and sentence[i][0] == "（" and sentence[i][1] == BRACKET_FONT and sentence[i][2] == BRACKET_SIZE:
                while i < len(sentence) and sentence[i][0] != "）":
                    i += 1
                matching_count += (i + 1 - start)

        # Move to the next character
        i += 1

    # Calculate the proportion
    return matching_count / len(sentence)

def check_sentence(sentence_text):
    # 检查关键词过滤条件
    if re.search(r"图|编写|册|索引|下表|表格|表1|表2|表3|？", sentence_text):
        return False
    if re.search(r"\（\d+\）", sentence_text):
        return False
    # 检查是否以问号结尾
    if sentence_text.strip().endswith("？") or sentence_text.strip().endswith("！"):
        return False
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
    # print(page_numbers)

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
        with pdfplumber.open(pdf_path) as pdf:
            for chapter_index, chapter in enumerate(chapters):
                # 插入章信息到 SQL文件
                chapter_id = f"010106{str(chapter_index+1).zfill(2)}000000"
                chapter_code = f"CH{str(chapter_index+1).zfill(2)}"
                sql_file.write("\n")
                sql_file.write(
                    f"INSERT INTO knowledge_point (kp_id, subject_code, category1_code, category2_code, code, name, description, parent_id) \n"
                    f"VALUES \n"
                    f"('{chapter_id}', 'PHYSICS', 'SENIOR', 'TERM_6', "
                    f"'{chapter_code}', '{chapter['title']}', '', NULL),\n"
                )
                
                for section_index, section in enumerate(chapter["sections"]):
                    # 插入节信息到 SQL文件
                    section_id = f"010106{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}0000"
                    section_code = f"{chapter_code}.SEC{str(section_index+1).zfill(2)}"
                    if section['title'].strip().startswith("实验："):
                        continue
                    sql_file.write(
                        f"('{section_id}', 'PHYSICS', 'SENIOR', 'TERM_6', "
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

                    # print(f"\n解析小节: {section['title']} (起始页: {start_page}, 结束页: {end_page})")
                    
                    current_knowledge_point = None
                    kp_index = 0
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
                            if char.get("fontname") == TITLE_FONT and round(char.get("size")) == 14 and char.get("text") != "问" and char.get("text") != "题" and char.get("text").strip() != "":
                                # 如果当前有未结束的知识点标题，保存到知识点列表
                                if current_knowledge_point:
                                    gen_multi_sentence(current_knowledge_point, sql_file)

                                # 开始扫描完整的知识点标题
                                kp_title = char["text"]  # 初始化知识点标题
                                last_scanned_index = char_index  # 记录当前索引
                                for next_char_index in range(char_index + 1, len(current_page.chars)):
                                    next_char = current_page.chars[next_char_index]
                                    # 如果字体和大小与知识点标题一致，则继续拼接标题
                                    if next_char.get("fontname") == TITLE_FONT and round(next_char.get("size")) == 14:
                                        kp_title += next_char["text"]
                                        last_scanned_index = next_char_index  # 更新最后扫描的索引
                                    else:
                                        # 字体或大小不一致时，结束扫描
                                        break

                                # 插入知识点信息到 SQL文件
                                kp_id = f"010106{str(chapter_index+1).zfill(2)}{str(section_index+1).zfill(2)}{str(kp_index+1).zfill(2)}00"
                                kp_code = f"{section_code}.KP{str(kp_index+1).zfill(2)}"
                                sql_file.write(
                                    f"('{kp_id}', 'PHYSICS', 'SENIOR', 'TERM_6', "
                                    f"'{kp_code}', '{kp_title.strip()}', '', '{section_id}'),\n"
                                )
                                
                                # 创建章节标题的字典
                                current_knowledge_point = {
                                    "title": kp_title.strip(),  # 去除多余空格
                                    "options": [],
                                    "chaptor_index": chapter_index,
                                    "section_index": section_index,
                                    "kp_index": kp_index,
                                    "kp_id": kp_id,
                                    "kp_code": kp_code,
                                }
                                
                                kp_index += 1  # 更新知识点索引
                                
                                # 更新外层循环的索引，跳过已扫描的字符
                                char_index = last_scanned_index
                                previous_font = TITLE_FONT
                                previous_size = 14
                                space = False
                                
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
                                # 先考虑空格隔开两端字体不同的文本的情况
                                if (
                                    previous_font is not None
                                    and previous_size is not None
                                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                                    and space == True
                                ):
                                    font_right = False
                                    for i in range(char_index, len(current_page.chars)):
                                        check_char = current_page.chars[i]
                                        check_text = check_char.get("text", "")
                                        # 检查是否是中文字符
                                        if is_chinese(check_text):
                                            check_font = check_char.get("fontname", "")
                                            if check_font == BODY_FONT:
                                                font_right = True   
                                                break
                                                
                                    # 如果字体变化且前面是汉字，分割句子并保留后半部分
                                    if current_sentence and font_right and ((is_chinese(current_sentence[-1][0]) and current_sentence[-1][1] == PARA_FONT)  or current_sentence[-1][1] == PAGE_FONT):
                                        # print("current_sentence[-1][0] is: "+current_sentence[-1][0])
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
                                    and (previous_font == TITLE_FONT and previous_size == TITLE_SIZE)  # 检测字体或字号变化
                                    and (font == BODY_FONT and size == BODY_SIZE)
                                    and not current_knowledge_point["options"]
                                ):
                                    current_sentence = [(text, font, size)]
                                    previous_font = font
                                    previous_size = size
                                    space = False  # 重置空格标志
                                    char_index += 1
                                    continue
                                elif (
                                    previous_font is not None
                                    and previous_size is not None
                                    and (font != previous_font or size != previous_size)  # 检测字体或字号变化
                                    and font == BODY_FONT
                                    and space == False
                                ):
                                    # print("find font change: "+text)
                                    # print("current_sentence is: ",end=" ")
                                    # print(current_sentence)
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
                                previous_font = font
                                previous_size = size
                                # print("text is: "+text,"current_sentence is: "+str(current_sentence))
                                # 如果遇到句子结束符，结束当前句子
                                if text in "。！？":
                                    proportion = calculate_font_proportion(current_sentence)
                                    st = "".join([c[0] for c in current_sentence])  
                                    # print("sentence is: "+st)
                                    # print("proportion is "+str(proportion))
                                    if proportion >= 0.6:
                                        sentence_text = "".join([c[0] for c in current_sentence])
                                        print("length of sentence is: "+str(len(sentence_text)))
                                        save_text(current_sentence)  # 保存当前句子到文件
                                        
                                        if check_sentence(sentence_text):
                                            current_knowledge_point["options"].append(sentence_text)  # 添加到知识点选项列表
                                        
                                    current_sentence = []
                                space = False  # 重置空格标志

                            char_index += 1
                        # 添加最后一个章节（如果有）
                    if current_knowledge_point:
                        gen_multi_sentence(current_knowledge_point, sql_file)
                        

# 添加命令行参数解析
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析 PDF 文件并生成 SQL")
    parser.add_argument("--input", default="senior_chemistry_textbooks/senior_optional_3.pdf", help="输入 PDF 文件路径")
    parser.add_argument("--output", default="sql/che_senior.sql", help="输出 SQL 文件路径")
    parser.add_argument("--api", default="deepseek", choices=["deepseek", "gpt", "kimi", "doubao", "mistral"], help="调用的 API 类型")
    parser.add_argument("--temperature", type=float, default=1.0, help="生成内容的随机性（默认值为 0.5）")
    args = parser.parse_args()

    # 调用主函数
    extract_catalog_and_chapters_with_pages(
        pdf_path=args.input,
        output_sql_path=args.output
    )
