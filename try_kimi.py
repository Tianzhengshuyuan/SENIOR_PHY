from openai import OpenAI

# 配置 Kimi API 客户端
client = OpenAI(api_key="sk-ODuizMlUC22phanBhvYz6dBjx2yrz7vhKhcjKnoIrYssThQo", base_url="https://api.moonshot.cn/v1")

text = """从许多实验和生活现象中我们都会发现，不同种物质能够彼此进入对方。
在物理学中，人们把这类现象叫作扩散（diffusion）。
扩散现象并不是外界作用（例如对流、重力作用等）引起的，也不是化学反应的结果，而是由物质分子的无规则运动产生的。
扩散现象是物质分子永不停息地做无规则运动的证据之一。
扩散现象在科学技术中有很多应用。
例如，在生产半导体器件时，需要在纯净半导体材料中掺入其他元素。
这一过程可以在高温条件下通过分子的扩散来完成。
19世纪初，一些人观察到，悬浮在液体中的小颗粒总在不停地运动。
1827年，英国植物学家布朗首先在显微镜下研究了这种运动。
下面我们做一个类似的实验。"""

def call_kimi_api(question):
    """
    调用 Kimi API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = client.chat.completions.create(
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

prompt = "对于下面的文本，每一行是一个句子，有的句子表达的意思是完整的，有的句子是不完整的，需要和它前面或后面的一个或多个句子连接在一起，才能表达完整的意思。请帮我整理文本，连接前后句子成一个段落，以表达完整意思，描述物理学中的客观事实。连续的句子只要能表达完整意思就划分为段落，不要让段落里包含太多句子。每一完整段落前面加上从“1. ”开始的序号。文本如下：\n"
send_text = prompt + text
response = call_kimi_api(send_text)
print("kimi API 返回的答案:")
print(response)