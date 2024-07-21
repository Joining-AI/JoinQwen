import dashscope
import concurrent.futures
from http import HTTPStatus
import os
import numpy as np

class QwenEmbedder:
    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('QWEN_API')  # 如果没有提供api_key，尝试从环境变量中获取

    def embed_text(self, text):
        resp = dashscope.TextEmbedding.call(
            model=dashscope.TextEmbedding.Models.text_embedding_v1,
            api_key=self.api_key,
            input=text
        )
        if resp.status_code == HTTPStatus.OK:
            return resp.output["embeddings"][0]["embedding"]
        else:
            print(resp)
            return None
        
    def embed_list(self, texts, num_threads=40):
        def process_text(text):
            embedding = self.embed_text(text)
            return text, embedding

        embeddings = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_text = {executor.submit(process_text, text): text for text in texts}
            for future in concurrent.futures.as_completed(future_to_text):
                text = future_to_text[future]
                try:
                    _, embedding = future.result()
                    embeddings[text] = embedding
                except Exception as exc:
                    embeddings[text] = None
                    print(f'Text {text} generated an exception: {exc}')
        
        return embeddings
    
    def partition_by_similarity(self, embeddings_dict, threshold=0.8):
        def cosine_similarity_matrix(matrix):
            norm = np.linalg.norm(matrix, axis=1)
            return np.dot(matrix, matrix.T) / np.outer(norm, norm)

        keys = list(embeddings_dict.keys())
        embeddings = np.array([embeddings_dict[key] for key in keys])

        # 计算相似度矩阵
        similarity_matrix = cosine_similarity_matrix(embeddings)
        np.fill_diagonal(similarity_matrix, 0)  # 自己与自己的相似度设置为0

        result = {}
        valid_indices = set(range(len(keys)))

        for i in range(len(keys)):
            if i not in valid_indices:
                continue

            similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
            similar_keys = [keys[j] for j in similar_indices if j in valid_indices]

            for idx in similar_indices:
                valid_indices.discard(idx)

            result[keys[i]] = {'Similar_keys': similar_keys}

        return result

    def calculate_similarity(self, text1, text2):

        embedding1 = self.embed_text(text1)
        embedding2 = self.embed_text(text2)

        if embedding1 is None or embedding2 is None:
            return None

        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)

        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity
