data_template=f'''
['实体1',...,'实体n']
'''

prompt='''
你是一个聪明的助手，你的工作是帮助人们理解文本中的信息。
给定一个可能与这个活动相关的文本，请你完整、详细地找出文本中的所有实体，同时保证每个实体都是完整而有价值的。
请你找出所有实体。对每个找到的实体，提取以下信息：
   - 实体名称：原文中的实体名称

--------------------------------------------------------------------------------
请根据给定的文本，给出其中提到的实体。
对于这一段文字:

{input_1}

我希望你完整、详细地抽取出它其中的所有实体，并且采用下面的格式回复，只允许你输出单个列表：

{data_template}
'''

def validation(data):
    """
    检查数据是否符合
    {string: {'相关性分数': float, '实体类型': string}, ..., string: {'相关性分数': float, '实体类型': string}}
    的格式。

    参数:
        data (dict): 待检查的数据。

    返回:
        bool: 如果数据符合格式则返回True，否则返回False。
    """
    if not isinstance(data, list):
        return False
    
    for item in data:
        if not isinstance(item, str):
            return False
    
    return True

correction='''
下列内容中含有一个错误的数据格式：

{answer}

请你修改它，使其符合以下格式：

{data_template}
'''