# JoinQwen

[![Official Website](https://img.shields.io/badge/Official%20Website-sjtujoining.com-blue?style=for-the-badge&logo=world&logoColor=white)](https://sjtujoining.com)

[![GitHub Repo stars](https://img.shields.io/github/stars/Joining-AI/JoinQwen?style=social)](https://github.com/Joining-AI/JoinQwen)

## 快速开始

JoinQwen 是一个简单的工具，用于测试和使用 Qwen API。通过本项目，您可以初始化 API，进行提问，并进行文本嵌入。

## 安装要求

请确保您已安装以下依赖项。您可以通过 `requirements.txt` 文件来安装这些依赖项。

```bash
pip install -r requirements.txt
```

## 配置

在项目根目录下创建一个 `.env` 文件，并添加您的 API 密钥：

```
QWEN_API=your_api_key_here
```

## 使用方法

### 初始化服务

首先，初始化 Qwen 服务：

```python
from Packages.LLM_BenchMarker.qwen_rater import *

tester = QwenRater()
```

### 进行 RPM 测试

您可以通过以下命令进行 RPM 测试：

```python
rpm = tester.rpm_test()
print(f"Final RPM: {rpm}")
```

### 初始化 API

```python
import os
from local_packages import *

# 初始化 API
agentopener = AgentOpener(service_type='qwen', version='long')

llm = agentopener.service
embedder = QwenEmbedder()
```

### 提问

您可以向 LLM 提问：

```python
answer = llm.ask('你好')
print(answer)
```

输出示例：

```
你好！有什么我能帮助你的吗？
```

### 文本嵌入

您可以对文本进行嵌入：

```python
vec = embedder.embed_text(answer)
print(vec)
```

输出示例：

```
[0.11480577290058136, 3.1070446968078613, -2.426426887512207, 1.8947781324386597, -1.4686617851257324, 2.1084201335906982, 1.4298882484436035, -0.3828396201133728, -0....]
```

### 寻找相似文档

您可以在给定的语料库列表中查找前k个与您给出的信息最相似的文档：

```python
documents = [
   '在处理解方程问题时，解完一定要检验',
   '平方根问题考虑多解',
   '钝角',
   '钝的角'
]
query = '120度的角叫什么角'
print(embedder.retrieve_k_most_relevant_documents(documents,query,2))
```

输出示例：

```
['钝的角', '钝角']
```

## 贡献

如果您有任何建议或发现了问题，请提交 Issue 或 Pull Request。

## 许可证

本项目采用 Apache 2.0 许可证。详细信息请参阅 LICENSE 文件。
