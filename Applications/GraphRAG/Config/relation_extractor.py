data_template='''
[
{
    "实体名称1": name_str,
    "实体名称2": name_str,
    "关系类型": type_str
},...,
]
'''

prompt='''

你是一个聪明的助手，你的工作是帮助人们理解文本中的信息。
给定一个可能与这个活动相关的文本{input_1}和一个实体列表{input_2}，请你指出实体列表中有相关性的实体
对于找到的每一对相关的实体，提取以下信息：
   - 实体名称1：相关实体对中更主要的那个实体
   - 实体名称2：相关实体对中相对次要的那个实体
   - 关系类型：他们之间的关系类型

--------------------------------------------------------------------------------
现在我有一些实体{input_2}
他们出自这个文段{input_1}，
请你帮我依据本文段给出这些实体的相关对，以如下数据结构返回:
{data_template}
'''

def validation(data):
    if not isinstance(data, list):
        return False
    
    for item in data:
        if not isinstance(item, dict):
            return False
        if '实体名称1' not in item or not isinstance(item['实体名称1'], str):
            return False
        if '实体名称2' not in item or not isinstance(item['实体名称2'], str):
            return False
        if '关系类型' not in item or not isinstance(item['关系类型'], str):
            return False
    
    return True

correction='''
下列内容中含有一个错误的数据格式：

{answer}

请你修改它，使其符合以下格式：

{data_template}
'''
