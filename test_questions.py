import re
import os
import json
import openai
import argparse
from openai import OpenAI
    
os.environ["HTTP_PROXY"] = "http://localhost:7890"
os.environ["HTTPS_PROXY"] = "http://localhost:7890"

# 初始化 DeepSeek API 客户端
deepseek_client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")
kimi_client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")

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
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
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
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 时出错: {e}")
        return "API 调用失败"
    
def process_questions(filename):
    # 打开并读取JSON文件
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    count = 0
    correct = 0
    # 处理每个问题条目
    for entry in data:
        count += 1
        question = entry['question']
        options = entry['A'], entry['B'], entry['C'], entry['D']
        prompt = "这道题的正确答案是什么，只回复答案，不用解释"

        # 拼接问题和选项
        full_question = f"{question}\nA: {entry['A']}\nB: {entry['B']}\nC: {entry['C']}\nD: {entry['D']}\n{prompt}"
        correct_answer = entry['answer']
        if args.api == 'deepseek':
            answer = call_deepseek_api(full_question)
        elif args.api == 'gpt':
            answer = call_gpt_api(full_question)
        elif args.api == 'kimi':
            answer = call_kimi_api(full_question)
        print("模型回答:", answer)
        
        extracted_answer = re.findall(r'[A-D]', answer) 

        # 分割正确答案和模型的回答，确保模型的回答严格匹配正确答案
        correct_answer_set = set(correct_answer)  # 正确答案转为集合
        response_answer_set = set(extracted_answer)  # 模型的回答转为集合

        # 判断模型的回答是否完全等于正确答案
        if response_answer_set == correct_answer_set:
            correct += 1
        # 打印结果
        print(full_question)
        print("正确答案:", correct_answer)

    print(f"总题数: {count}, 正确答案数: {correct}, 正确率: {correct / count:.2%}")

if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description='调用不同的API来处理问题')
    parser.add_argument('--input', default="questions.json", type=str, help='输入文件名')
    parser.add_argument('--api', type=str, choices=['deepseek', 'gpt', 'kimi'], default='deepseek')
    args = parser.parse_args()

    # 调用处理函数
    process_questions(args.input)