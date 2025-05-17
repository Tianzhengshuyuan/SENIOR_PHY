#!/bin/bash

# 设置脚本为严格模式，捕获错误
set -e

# 文件路径
START_SQL="sql/start.sql"
PHY_SENIOR_SQL="sql/phy_senior.sql"

# 第一步：将 start.sql 的内容复制到 phy_senior.sql 中
if [[ -f "$START_SQL" ]]; then
    cp "$START_SQL" "$PHY_SENIOR_SQL"
    echo "成功将 $START_SQL 的内容复制到 $PHY_SENIOR_SQL 中。"
else
    echo "错误: 文件 $START_SQL 不存在！"
    exit 1
fi

# 第二步：按顺序执行 Python 脚本
COMMANDS=(
    "python make_sql_s1.py"
    "python make_sql_s2.py"
    "python make_sql_s3.py"
    "python make_sql_so1.py"
    "python make_sql_so2.py"
    "python make_sql_so3.py"
    "python standardize_sql.py"
)

for CMD in "${COMMANDS[@]}"; do
    echo "正在执行命令: $CMD"
    if $CMD; then
        echo "命令执行成功: $CMD"
    else
        echo "命令执行失败: $CMD"
        exit 1  # 如果某个命令失败，停止运行
    fi
done

echo "所有任务执行完成！"