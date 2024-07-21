data_template='''
[
{
    "名称": name_str,
    "解释": type_str
},...,
]
'''

prompt='''
现在我有一些实体{input_2}
他们出自这个文段{input_1}，
请你帮我依据本文段给出这些实体的解释，以如下结构返回:
{data_template}
'''

def validation(data):
    if not isinstance(data, list):
        return False
    
    for item in data:
        if not isinstance(item, dict):
            return False
        if '名称' not in item or not isinstance(item['名称'], str):
            return False
        if '解释' not in item or not isinstance(item['解释'], str):
            return False
    
    return True

correction='''
下列内容中含有一个错误的数据格式：

{answer}

请你修改它，使其符合以下格式：

{data_template}
'''