import threading
from queue import Queue

class MultiProcessor:

    def __init__(self, llm, processor, data_template, prompt_template, correction_template, validator, isList=True):
        self.llm = llm
        self.processor = processor
        self.data_template = data_template
        self.prompt_template = prompt_template
        self.correction_template = correction_template
        self.validator = validator
        self.list_flag = isList
    
    def generate_prompt(self, **kwargs):
        kwargs['data_template'] = self.data_template
        return self.prompt_template.format(**kwargs)
    
    def generate_correction_prompt(self, answer):
        return self.correction_template.format(answer=answer, data_template=self.data_template)
    
    def task_perform(self, **kwargs):
        prompt = self.generate_prompt(**kwargs)
        answer = self.llm.ask(prompt)
        if self.list_flag:
            structured_data = self.processor.parse_list(answer)
        else:
            structured_data = self.processor.parse_dict(answer)
        print(kwargs, structured_data)
        return structured_data
    
    def correct_data(self, answer):
        correction_prompt = self.generate_correction_prompt(answer)
        correction = self.llm.ask(correction_prompt)
        return correction

    def process_tuple(self, input_tuple):
        input_data = input_tuple[:-1]
        index = input_tuple[-1]
        attempts = 0
        
        while attempts < 3:
            try:
                input_dict = {f'input_{i+1}': input_data[i] for i in range(len(input_data))}
                structured_data = self.task_perform(**input_dict)
                if self.validator(structured_data):
                    return (structured_data, index)
                corrected_answer = self.correct_data(structured_data)
                if corrected_answer and self.validator(corrected_answer):
                    return (corrected_answer, index)
                break
            except Exception as e:
                attempts += 1

        return (None, index)
    
    def multitask_perform(self, tuple_list, num_threads):
        results = [None] * len(tuple_list)
        queue = Queue()
        
        for idx, input_tuple in enumerate(tuple_list):
            queue.put((input_tuple, idx))
        
        def worker():
            while not queue.empty():
                input_tuple, idx = queue.get()
                result = self.process_tuple(input_tuple)
                print('result',result)
                results[idx] = result
                queue.task_done()

        threads = []
        for _ in range(min(num_threads, len(tuple_list))):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        queue.join()

        for thread in threads:
            thread.join()

        return results
