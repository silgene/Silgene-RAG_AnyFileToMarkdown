import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)
systempropt="""
# 角色(Role)
    - 实现文本格式转换的工具，将输入的文本转换成md格式。比如一、前加#，1、前加##，如果没有明显标题则需要进行总结出标题。并以md格式输出

# 功能(Skills)
    - 将输入的文本内容转换成 Markdown 格式

# 限制(Constraint)
    - 仅进行文本到 Markdown 格式的转换，不进行其他操作
    - 不输出其他任何无关的内容。仅输出转换后的文本

# 输出(Output)
    - 将输入的文本内容按照 Markdown 的语法规则进行转换后的结果
    - 不输出其他任何无关的内容。仅输出转换后的文本

# 检查(Check)
    - 检查转换后的内容是否符合 Markdown 的语法规范
    - 确保转换过程中没有丢失或错误处理文本信息

# 要求(Claim)
    - 输入的文本应为可理解的自然语言文本
    - 输出的 Markdown 格式应准确无误，符合语法要求 
"""

if __name__ == '__main__':

    filepath=r'L:\ailab2025\RAG_AnyFile-to-Markdown\README.md'
    print('开始将：{}文件转成md文件'.format(filepath))
    outfilepath=filepath[:-4]+'_md.md'
    with open(filepath,'r',encoding='utf-8') as f:
        data=f.readlines()
        data=''.join(data)



    stream = client.chat.completions.create(
        model = "ep-20250208182605-lnn2p",  # your model endpoint ID
        messages = [
            {"role": "system", "content": systempropt},
            {"role": "user", "content": data},
        ],
        stream=True
    )

    outText=''
    for chunk in stream:
        if not chunk.choices:
            continue
        print(chunk.choices[0].delta.content, end="")
        outText+=chunk.choices[0].delta.content
    with open(outfilepath,'w',encoding='utf-8') as w:
        w.write(outText)




