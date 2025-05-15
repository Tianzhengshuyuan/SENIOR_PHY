import mysql.connector

def connect_db():
    """连接数据库"""
    return mysql.connector.connect(
        host="localhost",     # 数据库地址（自行修改）
        user="root",          # 数据库用户名（自行修改）
        password="",  # 数据库密码（自行修改）
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

def display_options(options):
    """
    显示选项列表
    :param options: 选项列表
    """
    print("\n请选择以下选项：")
    for i, (kp_id, name) in enumerate(options, start=1):
        print(f"{i}. {name}")
    print("0. 返回上一级")

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
            choice = input("请输入选项编号：")
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