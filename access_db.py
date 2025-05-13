import mysql.connector
import random
import json

def connect_to_db():
    """连接到MySQL数据库"""
    try:
        connection = mysql.connector.connect(
            host="localhost",       # 数据库主机地址
            user="root",            # 数据库用户名
            password="",            # 数据库密码，留空表示无密码
            database="phy_senior3"  # 数据库名称
        )
        print("数据库连接成功！")
        return connection
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

def get_sections(connection, parent_id):
    """获取指定章节下的小节"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT kp_id, name, description 
        FROM knowledge_point 
        WHERE parent_id = %s;
        """
        cursor.execute(query, (parent_id,))
        sections = cursor.fetchall()
        return sections
    except mysql.connector.Error as err:
        print(f"查询失败: {err}")
        return []
    finally:
        cursor.close()

def get_knowledge_points(connection, parent_id):
    """获取指定小节下的知识点"""
    try:
        cursor = connection.cursor()
        query = """
        SELECT kp_id, name, description 
        FROM knowledge_point 
        WHERE parent_id = %s;
        """
        cursor.execute(query, (parent_id,))
        points = cursor.fetchall()
        return points
    except mysql.connector.Error as err:
        print(f"查询失败: {err}")
        return []
    finally:
        cursor.close()

def get_questions(connection, parent_id):
    """获取指定知识点下的问题"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT kp_id, name, description 
        FROM knowledge_point 
        WHERE parent_id = %s;
        """
        cursor.execute(query, (parent_id,))
        questions = cursor.fetchall()
        return questions
    except mysql.connector.Error as err:
        print(f"查询失败: {err}")
        return []
    finally:
        cursor.close()

def generate_question_json(questions):
    """从问题中随机选择并生成 JSON 格式的题目"""
    # 按照 name 分类问题
    correct_questions = [q for q in questions if q['name'] == "正确"]
    incorrect_questions = [q for q in questions if q['name'] == "错误"]

    if not correct_questions or len(incorrect_questions) < 3:
        print("问题不足以生成题目！")
        return None

    # 随机选取1个正确问题和3个错误问题
    correct = random.choice(correct_questions)
    incorrect = random.sample(incorrect_questions, 3)

    # 构造题目选项
    options = incorrect + [correct]
    random.shuffle(options)

    # 找到正确答案的位置
    correct_index = options.index(correct)
    answer = chr(65 + correct_index)  # 转换为 A, B, C, D

    # 构造 JSON 对象
    question_json = {
        "question": "下面几个选项中正确的是",
        "A": options[0]['description'],
        "B": options[1]['description'],
        "C": options[2]['description'],
        "D": options[3]['description'],
        "answer": answer
    }

    return question_json

def display_options(options, level_name="选项"):
    """显示选项并提示用户选择"""
    print(f"\n以下是 {level_name}：")
    for idx, option in enumerate(options):
        print(f"{idx + 1}. {option[1]} - {option[2]}")
    print("0. 返回上一级")

    while True:
        try:
            choice = int(input(f"请选择 0-{len(options)}：")) - 1
            if choice == -1:
                return None  # 返回上一级
            elif 0 <= choice < len(options):
                return options[choice]
            else:
                print("输入无效，请重新选择。")
        except ValueError:
            print("输入无效，请输入数字。")

def main():
    # 连接数据库
    connection = connect_to_db()
    if not connection:
        return

    try:
        # 一级菜单：选择 CH01 的小节
        while True:
            print("\n获取 CH01 分子动理论的小节...")
            sections = get_sections(connection, "2401000000")  # CH01 的 kp_id
            if not sections:
                print("未找到小节内容。")
                return
            
            selected_section = display_options(sections, "CH01 的小节")
            if selected_section is None:
                print("已退出程序。")
                return
            
            # 二级菜单：选择小节下的知识点
            while True:
                print(f"\n获取 {selected_section[1]} 下的知识点...")
                knowledge_points = get_knowledge_points(connection, selected_section[0])  # 小节的 kp_id
                if not knowledge_points:
                    print("未找到知识点内容。")
                    break  # 返回上一级

                selected_point = display_options(knowledge_points, f"{selected_section[1]} 的知识点")
                if selected_point is None:
                    break  # 返回上一级
                
                # 三级菜单：从知识点中随机生成题目
                while True:
                    print(f"\n获取 {selected_point[1]} 下的问题...")
                    questions = get_questions(connection, selected_point[0])  # 知识点的 kp_id
                    if not questions:
                        print("未找到问题内容。")
                        break  # 返回上一级

                    # 生成题目 JSON
                    question_json = generate_question_json(questions)
                    if question_json:
                        print("\n生成的题目 JSON：")
                        print(json.dumps(question_json, ensure_ascii=False, indent=4))
                    
                    input("按回车键返回上一级...")
                    break  # 返回到知识点选择菜单

    finally:
        # 关闭数据库连接
        connection.close()
        print("\n数据库连接已关闭。")

if __name__ == "__main__":
    main()