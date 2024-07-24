data_template=f'''
['实体类型1',...,'实体类型n']
'''

prompt='''
你是一个聪明的助手，你的工作是帮助人们理解文本中的信息。
当给定一段文字时，你的任务是为这段文字中的实体进行分类。
非常重要：不要生成重复或重叠的实体类型。例如，如果文本包含"公司"和"组织"，你应该只返回其中一个。
数量不是重点，质量优先。确保你的答案中的每一个内容都与实体提取的上下文相关。
记住，我们需要的是实体类型。
接下来是正式的任务：
--------------------------------------------------------------------------------
请根据给定的文本，给出其中涉及的实体类型。
对于这一段文字:

{input_1}

我希望你识别出它所涉及到的主题，并且采用下面的格式回复：

{data_template}
'''

def validation(data):
    """
    检查数据是否符合[string, ..., string]的格式。

    参数:
        data (list): 待检查的数据。

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
