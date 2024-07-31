import threading
import time
import random
from queue import Queue
from tqdm import tqdm

class MultiProcessor:

    def __init__(self, llm, parse_method, data_template, prompt_template, correction_template, validator):
        self.llm = llm  # 大型语言模型 (LLM) 用于处理任务
        self.parse_method = parse_method  # 解析LLM输出的方法
        self.data_template = data_template  # 数据输入模板
        self.prompt_template = prompt_template  # 生成提示的模板
        self.correction_template = correction_template  # 生成纠正提示的模板
        self.validator = validator  # 验证结构化数据正确性的函数

    def generate_prompt(self, **kwargs):
        kwargs['data_template'] = self.data_template  # 将数据模板添加到kwargs中
        return self.prompt_template.format(**kwargs)  # 使用提示模板和kwargs生成提示

    def generate_correction_prompt(self, answer):
        return self.correction_template.format(answer=answer, data_template=self.data_template)  # 使用纠正模板和答案生成纠正提示

    def task_perform(self, **kwargs):
        try:
            prompt = self.generate_prompt(**kwargs)  # 生成提示
            answer = self.llm.ask(prompt)  # 向LLM提出问题并获得答案
            structured_data = self.parse_method(answer)  # 解析LLM的答案为结构化数据
            return structured_data  # 返回结构化数据
        except Exception as e:
            print(f"Error in task_perform: {str(e)}")  # 捕捉异常并打印错误信息
            raise e  # 抛出异常

    def correct_data(self, answer):
        correction_prompt = self.generate_correction_prompt(answer)  # 生成纠正提示
        correction = self.llm.ask(correction_prompt)  # 向LLM提出纠正问题并获得答案
        return correction  # 返回纠正后的答案

    def process_tuple(self, input_tuple):
        try:
            input_data = input_tuple[:-1]  # 提取输入数据
            index = input_tuple[-1]  # 提取索引
            attempts = 0  # 初始化尝试次数
            base_wait_time = 1  # 初始等待时间

            while attempts < 3:
                try:
                    input_dict = {f'input_{i+1}': input_data[i] for i in range(len(input_data))}  # 将输入数据转换为字典
                    structured_data = self.task_perform(**input_dict)  # 执行任务
                    if self.validator(structured_data):  # 验证结构化数据
                        return (structured_data, index)  # 返回结构化数据和索引
                    corrected_answer = self.correct_data(structured_data)  # 纠正数据
                    if corrected_answer and self.validator(corrected_answer):  # 验证纠正后的数据
                        return (corrected_answer, index)  # 返回纠正后的数据和索引
                    break
                except Exception as e:
                    if 'Throttling.RateQuota' in str(e):  # 检查是否遇到限流错误
                        wait_time = base_wait_time * (2 ** attempts) + random.uniform(0, 1)  # 计算等待时间
                        print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds. Attempt {attempts + 1}/3")
                        time.sleep(wait_time)  # 等待一段时间后重试
                        attempts += 1  # 增加尝试次数
                    else:
                        print(f"An error occurred: {str(e)}. Attempt {attempts + 1}/3")  # 打印其他错误信息
                        attempts += 1  # 增加尝试次数

        except Exception as final_error:
            raise RuntimeError(f"Error occurred during process_tuple: {str(final_error)}")  # 捕捉并重新抛出最终错误


    def multitask_perform(self, tuple_list, num_threads):
        results = [None] * len(tuple_list)  # 初始化结果列表
        queue = Queue()  # 创建队列

        for idx, input_tuple in enumerate(tuple_list):
            queue.put((input_tuple, idx))  # 将输入元组和索引加入队列

        def worker(pbar):
            while not queue.empty():
                input_tuple, idx = queue.get()  # 从队列中获取输入元组和索引
                result = None
                thread_result_queue = Queue()  # 创建线程结果队列

                # 启动线程并加入超时机制
                thread = threading.Thread(target=lambda q, arg1: q.put(self.process_tuple(arg1)), args=(thread_result_queue, input_tuple))
                thread.start()
                thread.join(timeout=30)  # 设置单线程30s超时

                if thread.is_alive():
                    print(f"Thread processing {input_tuple} timed out.")
                    thread.join()
                else:
                    if not thread_result_queue.empty():
                        result = thread_result_queue.get()
                        print('A thread has got its result:', result)
                    else:
                        print(f"No result obtained for {input_tuple}")

                # 确保结果被记录
                if result is None:
                    print(f"Force returning a placeholder for {input_tuple}")
                    result = (None, idx)

                results[idx] = result  # 将结果保存到结果列表
                queue.task_done()  # 标记队列任务完成
                pbar.update(1)  # 更新进度条

        with tqdm(total=len(tuple_list)) as pbar:  # 创建进度条
            threads = []
            for _ in range(min(num_threads, len(tuple_list))):
                thread = threading.Thread(target=worker, args=(pbar,))  # 创建工作线程
                threads.append(thread)
                thread.start()  # 启动线程

            queue.join()  # 等待所有队列任务完成

            for thread in threads:
                thread.join()

        return results
