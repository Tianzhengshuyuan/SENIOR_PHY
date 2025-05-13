from transformers import pipeline

def is_semantically_complete(text):
    """
    判断给定的文本是否为语义完整的表达。
    """
    classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
    # 使用简单的假设：如果文本能被分类为明确的类别，则其语义完整
    result = classifier(text)
    return result[0]['score'] > 0.5  # 只筛选置信度高的语句

def split_into_sentences(text):
    """
    根据中文句号（。）、感叹号（！）和问号（？）将段落切分为句子。
    """
    # 按句号、感叹号和问号分割，并保留分隔符
    import re
    sentences = re.split(r'(。|！|？)', text)  # 保留分隔符
    # 将分割的句子和标点符号重新组合成完整句子
    sentences = [sentences[i] + sentences[i + 1] for i in range(0, len(sentences) - 1, 2)]
    return [sentence.strip() for sentence in sentences if sentence.strip()]  # 去掉空白句子

def extract_complete_options(text):
    """
    提取文本中语义完整的段落或句子。
    """
    # 按句号分割
    sentences = split_into_sentences(text)
    complete_options = []
    for i, sentence in enumerate(sentences):
        print(f"正在检查第{i+1}句：", end=' ')
        print(sentence)
        if is_semantically_complete(sentence):
            complete_options.append(sentence)
    return complete_options

# 示例教材文本
text = """
从许多实验和生活现象中我们都会发现，不同种物质能够彼此进入对方。在物理学中，人们把这类现象叫作扩散（diffusion）。
扩散现象并不是外界作用（例如对流、重力作用等）引起的，也不是化学反应的结果，而是由物质分子的无规则运动产生的。
例如，图1.1-2中酱油的色素分子扩散到了鸡蛋清内。扩散现象是物质分子永不停息地做无规则运动的证据之一。
"""

# 提取完整选项
options = extract_complete_options(text)
print("完整选项：")
for i, option in enumerate(options, 1):
    print(f"{i}. {option}")