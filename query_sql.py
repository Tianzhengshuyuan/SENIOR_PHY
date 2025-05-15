import mysql.connector
import random
import openai
from openai import OpenAI


# 初始化 DeepSeek API 客户端
client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")

def call_deepseek_api(question):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"

def generate_questions(deep_nodes):
    """
    根据 deep_nodes 中的描述生成题目。
    :param deep_nodes: 最深节点列表
    :return: 生成的题目字符串
    """
    all_correct_descriptions = []  # 存储所有正确描述
    all_incorrect_descriptions = []  # 存储所有错误描述

    correct_all = 10
    incorrect_all = 5
    
    correct_now = round(len(deep_nodes) * 0.75)
    incorrect_now = len(deep_nodes) - correct_num
    
    correct_need = correct_all - correct_now
    incorrect_need = incorrect_all - incorrect_now
    
    for node in deep_nodes:
        print(f"正在处理节点：{node}")
        # 为每个节点生成 Prompt
        prompt_correct = (
            f"把下面这个和物理学有关的描述换个说法，表达相同的意思，只回复转换后的句子：\n{node}"
        )
        for i in range(3):
            # 调用 DeepSeek API
            response = call_deepseek_api(prompt_correct)
            print(f"API 返回：{response}")
            # 分析 API 返回结果，将正确和错误的描述分开
            if response != "API 调用失败":
                # 累积到总的列表中
                all_correct_descriptions.append(response)

        # 为每个节点生成 Prompt
        prompt_incorrect = (
            f"把下面这个和物理学有关的描述做微小的改变，使其成为一句错误的描述，不符合物理学规律，只回复转换后的句子：\n{node}"
        )
        for i in range(3):
            # 调用 DeepSeek API
            response = call_deepseek_api(prompt_incorrect)
            print(f"API 返回：{response}")
            # 分析 API 返回结果，将正确和错误的描述分开
            if response != "API 调用失败":
                # 累积到总的列表中
                all_incorrect_descriptions.append(response)

    # 检查是否有足够的数据生成题目
    if len(all_correct_descriptions) >= 3 and len(all_incorrect_descriptions) >= 1:
        # 随机选择 3 个正确选项
        selected_correct = random.sample(all_correct_descriptions, 3)
        # 随机选择 1 个错误选项
        selected_incorrect = random.choice(all_incorrect_descriptions)

        # 将所有选项放入列表
        options = selected_correct + [selected_incorrect]
        # 随机打乱选项顺序
        random.shuffle(options)

        # 确定错误选项的位置（索引）
        incorrect_index = options.index(selected_incorrect)
        correct_answer = chr(65 + incorrect_index)  # 计算正确答案的字母选项（A, B, C, D）

        # 组装题目
        question = (
            "下面的说法错误的是：\n"
            f"A. {options[0]}\n"
            f"B. {options[1]}\n"
            f"C. {options[2]}\n"
            f"D. {options[3]}\n"
            f"答案：{correct_answer}"
        )
        return question
    else:
        return "无法生成题目，因为正确或错误的描述数量不足。"

def connect_db():
    """连接数据库"""
    return mysql.connector.connect(
        host="localhost",     # 数据库地址（自行修改）
        user="root",          # 数据库用户名（自行修改）
        password="",          # 数据库密码（自行修改）
        database="phy_senior3"  # 数据库名称
    )

def get_options(cursor, parent_id):
    """
    获取子节点选项
    :param cursor: 数据库游标
    :param parent_id: 父级ID（NULL表示顶级）
    :return: 子节点列表
    """
    if parent_id is None:
        query = "SELECT kp_id, name FROM knowledge_point WHERE parent_id IS NULL"
    else:
        query = f"SELECT kp_id, name FROM knowledge_point WHERE parent_id = '{parent_id}'"
        
    cursor.execute(query)
    return cursor.fetchall()

def get_all_deepest_nodes(cursor, parent_id):
    """
    获取指定节点下所有最深节点的名称
    :param cursor: 数据库游标
    :param parent_id: 当前父节点ID
    :return: 最深节点名称列表
    """
    query = f"SELECT kp_id, name, code FROM knowledge_point WHERE parent_id = '{parent_id}'"
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:  # 如果没有子节点，返回当前节点的名称
        return []

    all_deep_nodes = []
    for kp_id, name, code in results:
        # 递归调用获取子节点的最深节点
        child_deep_nodes = get_all_deepest_nodes(cursor, kp_id)
        if not child_deep_nodes and "OP" in code:  # 如果子节点没有更深的子节点，当前节点是最深的
            all_deep_nodes.append(name)
        else:
            all_deep_nodes.extend(child_deep_nodes)
    
    return all_deep_nodes

def display_options(options):
    """
    显示选项列表
    :param options: 选项列表
    """
    print("\n请选择以下选项：")
    for i, (kp_id, name) in enumerate(options, start=1):
        print(f"{i}. {name}")
    print("0. 返回上一级")
    print("ok. 展示当前选项下所有最深节点")


def interactive_query():
    """交互式查询知识点"""
    connection = connect_db()
    cursor = connection.cursor()
    
    history = []  # 用于记录用户的选择路径

    try:
        parent_id = None  # 初始从顶层开始
        while True:
            options = get_options(cursor, parent_id)
            
            if not options:
                print("没有更多的子项了，返回上一级。")
                if history:
                    parent_id = history.pop()  # 返回上一级
                else:
                    break  # 已经是顶层，退出
                continue

            display_options(options)

            # 用户输入选择
            choice = input("请输入选项编号：").strip()
            if choice == "ok":  # 展示当前节点下所有最深节点
                if parent_id is None:
                    print("当前为顶层，无法展示最深节点！")
                else:
                    deep_nodes = get_all_deepest_nodes(cursor, parent_id)
                    print("\n当前选项下的所有最深节点：")
                    if deep_nodes:
                        # for node in deep_nodes:
                        #     print(node)
                        quesition = generate_questions(deep_nodes)  # 生成题目
                        print(f"生成的题目：\n{quesition}")
                    else:
                        print("没有最深节点可显示！")
                continue

            if not choice.isdigit():
                print("请输入有效数字！")
                continue

            choice = int(choice)
            if choice == 0:  # 返回上一级
                if history:
                    parent_id = history.pop()
                else:
                    print("已经是顶层，无法返回！")
                continue

            if 1 <= choice <= len(options):
                selected_id, selected_name = options[choice - 1]
                print(f"已选择：{selected_name}")

                # 更新状态，进入下一级
                history.append(parent_id)  # 保存当前parent_id以支持返回
                parent_id = selected_id
            else:
                print("无效选项，请重新输入！")
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        cursor.close()
        connection.close()
        print("已断开数据库连接。")

# 运行交互式查询
interactive_query()