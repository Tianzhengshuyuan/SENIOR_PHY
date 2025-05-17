def standardize_sql(input_file, output_file):

    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 用于存储标准化后的 SQL 行
    standardized_lines = []

    # 遍历每一行，查找并修复问题
    for i, line in enumerate(lines):
        line = line.rstrip()  # 去除行末的空白字符
        if line == "" and i > 0 and i < len(lines) - 1:
            # 如果当前行是空行，且下一行以 "INSERT" 开头
            if lines[i + 1].strip().startswith("INSERT"):
                # 修改空行前一行的结尾为分号
                if standardized_lines[-1].endswith(","):
                    previous_line = standardized_lines[-1].rstrip(",")
                    standardized_lines[-1] = previous_line + ";\n"
        else:
            # 添加当前行到结果列表
            standardized_lines.append(line)

    # 确保最后一行以分号结尾
    if not standardized_lines[-1].endswith(";"):
        standardized_lines[-1] = standardized_lines[-1].rstrip(",") + ";\n"

    # 将标准化后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(standardized_lines) + "\n")

    print(f"SQL 文件已标准化并保存到: {output_file}")
    
standardize_sql("sql/phy_senior.sql", "sql/phy_senior.sql")