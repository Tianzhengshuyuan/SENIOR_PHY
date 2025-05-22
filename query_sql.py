import mysql.connector
import random
import openai
import json
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
def extract_statements_from_response(response):
    """
    从 DeepSeek API 的返回中提取陈述列表
    :param response: API 返回的字符串
    :return: 提取出的陈述列表
    """
    statements = []
    lines = response.split('\n')  # 按行分隔返回内容
    for line in lines:
        # 提取以数字开头的陈述，例如 "1. 陈述1"
        if line.strip() and line[0].isdigit():
            statements.append(line.split('. ', 1)[-1].strip())  # 去掉序号部分
    return statements

def generate_questions(deep_nodes, query_name):

    all_correct_descriptions = []  # 存储所有正确描述
    all_incorrect_descriptions = []  # 存储所有错误描述

    # 题目总数设定
    correct_all = 230
    incorrect_all = 230
    
    # 当前需要生成的题目数
    if round(len(deep_nodes) * 0.5) < correct_all:
        correct_now = round(len(deep_nodes) * 0.5)
    else:
        correct_now = correct_all
    
    if (len(deep_nodes) - correct_now) < incorrect_all:
        incorrect_now = len(deep_nodes) - correct_now
    else:   
        incorrect_now = incorrect_all
    
    # 还需要生成的题目数
    correct_need = correct_all - correct_now
    incorrect_need = incorrect_all - incorrect_now
    
    # 在 deep_nodes 中随机选出 correct_now 个节点
    # correct_nodes = deep_nodes[-correct_now:]  
    correct_nodes = deep_nodes[:correct_now]  
    # correct_nodes = random.sample(deep_nodes, correct_now)
    
    remain_nodes = [node for node in deep_nodes if node not in correct_nodes]
    incorrect_nodes = random.sample(remain_nodes, incorrect_now)
    
    # 为每个正确节点生成 Prompt
    print(f"已有正确陈述数量：{len(correct_nodes)}")
    for node in correct_nodes:
        print(f"正在处理正确节点：{node}")
        if node.startswith("他"):
            continue
        prompt_correct = (
            f"""判断下面的描述语义是否完整，比如“后人把悬浮微粒的这种无规则运动叫作布朗运动”语义不完整，因为“这种”不知道指代的是什么。“他的目的是：测量金属的遏止电压Uc与入射光的波长λ”语义不完整，因为不知道“他”指的是谁。“因此，我们把分子这种永不停息的无规则运动叫作热运动”语义不完整，因为不知道原因。
            如果描述语义不完整，则放弃转换该句子并生成一个和{query_name}有关且正确的陈述句。
            如果描述语义完整，则在其基础上变换。要求变换后的描述语义完整，可以作为一个物理学科选择题的选项。
            只回复转换或生成的句子：\n{node}"""
            )

        # 调用 DeepSeek API
        response = call_deepseek_api(prompt_correct)
        print(f"API 返回：{response}")
        if response != "API 调用失败":
            # 累积到正确描述列表中
            all_correct_descriptions.append(response)

    # 为每个错误节点生成 Prompt
    print(f"已有错误陈述数量：{len(incorrect_nodes)}")
    for node in incorrect_nodes:
        print(f"正在处理错误节点：{node}")
        if node.startswith("他"):
            continue
        prompt_incorrect = (
            f"""判断下面的描述语义是否完整，比如“后人把悬浮微粒的这种无规则运动叫作布朗运动”语义不完整，因为“这种”不知道指代的是什么。“他的目的是：测量金属的遏止电压Uc与入射光的波长λ”语义不完整，因为不知道“他”指的是谁。“因此，我们把分子这种永不停息的无规则运动叫作热运动”语义不完整，因为不知道原因。
            如果描述语义不完整，则放弃转换该句子并生成一个和{query_name}有关但错误的陈述句。
            如果描述语义完整，则在其基础上变换，使其成为错误的描述，不符合物理学规律。要求变换后的描述语义完整，可以作为一个物理学科选择题的选项。
            只回复转换或生成的句子：\n{node}"""
        )

        # 调用 DeepSeek API
        response = call_deepseek_api(prompt_incorrect)
        print(f"API 返回：{response}")
        if response != "API 调用失败":
            # 累积到错误描述列表中
            all_incorrect_descriptions.append(response)

    # 如果现有的正确描述数量不足，继续生成
    if correct_need > 0:
        prompt_new_correct = (
            f"帮我生成{correct_need}个和物理学中{query_name}有关的陈述句，要求陈述的都是该领域的事实，请按照下面的格式返回，不要添加其他任何信息：\n"
            f"1. 陈述1\n"
            f"2. 陈述2\n"
            f"3. 陈述3\n"
        )
        
        # 调用 DeepSeek API
        response = call_deepseek_api(prompt_new_correct)
        print(f"API 返回的正确陈述：{response}")
        
        # 提取返回的陈述并加入 all_correct_descriptions
        correct_statements = extract_statements_from_response(response)
        all_correct_descriptions.extend(correct_statements)        
        
    # 如果现有的错误描述数量不足，继续生成
    if incorrect_need > 0:
        prompt_new_incorrect = (
            f"帮我生成{incorrect_need}个和物理学中{query_name}有关的陈述句，要求陈述的都和该领域相关，但不是事实，请按照下面的格式返回，不要添加其他任何信息：\n"
            f"1. 陈述1\n"
            f"2. 陈述2\n"
            f"3. 陈述3\n"
        )
        
        # 调用 DeepSeek API
        response = call_deepseek_api(prompt_new_incorrect)
        print(f"API 返回的错误陈述：{response}")    
        incorrect_statements = extract_statements_from_response(response)
        all_incorrect_descriptions.extend(incorrect_statements)

        print("当前所有陈述：")
        print(all_correct_descriptions)
        print(all_incorrect_descriptions)
        

    # 随机生成 10 道题目
    questions = []
    for i in range(120):
        if i%2 == 0:
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
            answer = chr(65 + incorrect_index)  # 计算正确答案的字母选项（A, B, C, D）

            # 组装题目为 JSON 格式
            question_json = {
                "question": "下面的说法错误的是：",
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3],
                "answer": answer
            }
            questions.append(question_json)
        else:
            # 随机选择 1 个正确选项
            selected_correct = random.choice(all_correct_descriptions)
            # 随机选择 3 个错误选项
            selected_incorrect = random.sample(all_incorrect_descriptions, 3)

            # 将所有选项放入列表
            options = [selected_correct] + selected_incorrect
            # 随机打乱选项顺序
            random.shuffle(options)

            # 确定正确选项的位置（索引）
            correct_index = options.index(selected_correct)
            answer = chr(65 + correct_index)
            # 组装题目为 JSON 格式
            question_json = {
                "question": "下面的说法正确的是：",
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3],
                "answer": answer
            }
            questions.append(question_json)
    # 存储题目到 JSON 文件
    with open('questions.json', 'w', encoding='utf-8') as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

def connect_db():
    """连接数据库"""
    return mysql.connector.connect(
        host="localhost",     # 数据库地址（自行修改）
        user="root",          # 数据库用户名（自行修改）
        password="",          # 数据库密码（自行修改）
        database="phy_senior"  # 数据库名称
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

def get_name_by_id(cursor, kp_id):
    query = "SELECT name FROM knowledge_point WHERE kp_id = %s"
    cursor.execute(query, (kp_id,))
    result = cursor.fetchone()
    return result[0] if result else "未知节点"

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
                    query_name = get_name_by_id(cursor, parent_id)
                    if deep_nodes:
                        # for node in deep_nodes:
                        #     print(node)
                        print(f"生成{query_name}相关的问题：")
                        quesitions = generate_questions(deep_nodes, query_name)  # 生成题目
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