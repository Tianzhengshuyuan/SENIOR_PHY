def find_text_in_log(file_path, target_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        print(f"Total lines in file: {len(lines)}")

    target_len = len(target_text)
    print(f"Target text length: {target_len}")
    print(f"Target text: {target_text}")
    results = []

    # 使用滑动窗口检查连续行组合
    for start in range(len(lines) - target_len + 1):
        # 获取当前窗口内的文本片段
        segment = ''.join(lines[start + i][4] for i in range(target_len))
        
        # 检查拼接后的字符串是否与目标字符串匹配
        if segment == target_text:
            results.append(start + 1)  # 行号从1开始

    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python script.py <file_path> <target_text>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    target_text = sys.argv[2]
    results = find_text_in_log(file_path, target_text)
    
    if results:
        print(f"Found '{target_text}' starting at line(s): {', '.join(map(str, results))}")
    else:
        print(f"'{target_text}' not found in the file.")