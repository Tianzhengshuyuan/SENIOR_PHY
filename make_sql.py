import pdfplumber

def extract_catalog_and_chapters(pdf_path, output_sql_path):
    """
    从 PDF 文件中提取目录页信息，并生成 SQL 插入语句。
    :param pdf_path: PDF 文件路径
    :param output_sql_path: 输出 SQL 文件路径
    """
    with pdfplumber.open(pdf_path) as pdf:
        catalog_page = None

        # Step 1: 找到目录页
        for page_num, page in enumerate(pdf.pages, start=1):
            for number, char in enumerate(page.chars):
                if char["text"] == "目" and \
                   char.get("fontname") == "XNKZPT+FZLTZHK--GBK1-0" and \
                   round(char.get("size")) == 14:
                    next_char = page.chars[number + 3] 
                    if next_char["text"] == "录" and \
                       next_char.get("fontname") == "XNKZPT+FZLTZHK--GBK1-0" and \
                       round(next_char.get("size")) == 14:   
                        catalog_page = page
                        catalog_page_num = page_num
                        break
            if catalog_page:
                print(f"目录页在第 {catalog_page_num} 页")
                break

        if not catalog_page:
            print("未找到目录页")
            return

        # Step 2: 提取章节标题和章节内容
        chapters = []
        current_chapter = None
        char_index = 0
        while char_index < len(catalog_page.chars):
            print(f"当前索引：{char_index}")
            char = catalog_page.chars[char_index]
            if char["text"] == "目" and catalog_page.chars[char_index + 3]["text"] == "录":
                char_index += 4
                continue
            
            # 检查章节标题的起始条件：字体和大小符合章节标题的条件
            if char.get("fontname") == "XNKZPT+FZLTZHK--GBK1-0" and round(char.get("size")) == 14:
                # 如果当前有未结束的章节标题，保存到章节列表
                if current_chapter:
                    chapters.append(current_chapter)

                # 开始扫描完整的章节标题
                chapter_title = char["text"]  # 初始化章节标题
                last_scanned_index = char_index  # 记录当前索引
                for next_char_index in range(char_index + 1, len(catalog_page.chars)):
                    next_char = catalog_page.chars[next_char_index]
                    # 如果字体和大小与章节标题一致，则继续拼接标题
                    if next_char.get("fontname") == "XNKZPT+FZLTZHK--GBK1-0" and round(next_char.get("size")) == 14:
                        chapter_title += next_char["text"]
                        last_scanned_index = next_char_index  # 更新最后扫描的索引
                    else:
                        # 字体或大小不一致时，结束扫描
                        break

                # 创建章节标题的字典
                current_chapter = {
                    "title": chapter_title.strip(),  # 去除多余空格
                    "sections": []
                }

                # 更新外层循环的索引，跳过已扫描的字符
                char_index = last_scanned_index

            # 检查章节中的小节：字体和大小符合小节的条件
            elif current_chapter and char.get("fontname") == "SQAQXD+FZKTK--GBK1-0" and round(char.get("size")) == 12:
                # 小节标题的拼接逻辑
                section_title = char["text"]
                last_scanned_index = char_index  # 记录当前索引
                for next_char_index in range(char_index + 1, len(catalog_page.chars)):
                    next_char = catalog_page.chars[next_char_index]
                    # 如果小节的字体和大小一致，则继续拼接
                    if next_char.get("fontname") == "SQAQXD+FZKTK--GBK1-0" and round(next_char.get("size")) == 12:
                        section_title += next_char["text"]
                        last_scanned_index = next_char_index  # 更新最后扫描的索引
                    else:
                        # 字体或大小不一致时，结束扫描
                        break

                # 将小节标题添加到当前章节的 sections 列表
                current_chapter["sections"].append(section_title.strip())

                # 更新外层循环的索引，跳过已扫描的字符
                char_index = last_scanned_index
            char_index += 1
        # 添加最后一个章节（如果有）
        if current_chapter:
            chapters.append(current_chapter)

        # Step 3: 生成 SQL 插入语句
        with open(output_sql_path, "w", encoding="utf-8") as sql_file:
            for chapter_index, chapter in enumerate(chapters, start=1):
                chapter_id = f"2401{str(chapter_index).zfill(2)}0000"
                chapter_code = f"CH{str(chapter_index).zfill(2)}"
                sql_file.write(
                    f"INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, parent_id) \n"
                    f"VALUES ('{chapter_id}', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', "
                    f"'PHYSICS/SENIOR/GRADE_3/TERM_2', '{chapter_code}', '{chapter['title']}', '', NULL);\n"
                )

                # 添加章节中的小节
                for section_index, section in enumerate(chapter["sections"], start=1):
                    section_id = f"{chapter_id[:6]}{str(section_index).zfill(2)}0000"
                    section_code = f"{chapter_code}.SEC{str(section_index).zfill(2)}"
                    sql_file.write(
                        f"INSERT INTO knowledge_point (kp_id, subject_code, stage_code, grade_code, term_code, code_path, code, name, description, parent_id) \n"
                        f"VALUES ('{section_id}', 'PHYSICS', 'SENIOR', 'GRADE_3', 'TERM_2', "
                        f"'PHYSICS/SENIOR/GRADE_3/TERM_2/{chapter_code}', '{section_code}', '{section}', '', '{chapter_id}');\n"
                    )

        print(f"SQL 文件已生成：{output_sql_path}")


# 示例用法
pdf_path = "senior_optional_3.pdf"  # 替换为你的 PDF 文件路径
output_sql_path = "so3.sql"
extract_catalog_and_chapters(pdf_path, output_sql_path)