data_template='''
[
{
    "名称": name_str,
    "类型": type_str,
    "相关度": float
},...,
]
'''

prompt='''
现在有一些实体{input_2}
我们关心其中属于{input_1}的实体，
请你帮我进行这个归类，并为其打上相关度分数，这个分数是一个浮点数，位于0到10之间，以如下结构返回:
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
        if '类型' not in item or not isinstance(item['类型'], str):
            return False
        if '相关度' not in item or not isinstance(item['相关度'], float):
            return False
    
    return True

correction='''
下列内容中含有一个错误的数据格式：

{answer}

请你修改它，使其符合以下格式：

{data_template}
'''