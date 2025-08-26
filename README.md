# DeepSeek AI 助手 - Ollama集成版

这是一个基于Ollama部署DeepSeek大语言模型的AI聊天助手，使用Flask作为后端，提供现代化的Web界面。通过集成Ollama，可以更轻松地管理和使用大语言模型。

## 🚀 功能特性

- 🤖 基于Ollama的DeepSeek大语言模型
- 💬 实时AI对话交互
- 🎨 现代化响应式UI设计
- 📱 支持移动端和桌面端
- ⚡ 快速响应和流畅体验
- 🔒 完全本地化，保护隐私
- 🚀 无需复杂配置，一键启动

## 📋 系统要求

### 硬件要求
- **CPU**: 支持AVX2指令集的现代处理器
- **内存**: 至少16GB RAM（推荐32GB+）
- **存储**: 至少20GB可用空间（用于模型文件）
- **显卡**: 支持CUDA的NVIDIA显卡（推荐8GB+显存）

### 软件要求
- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8+ 
- **Ollama**: 最新版本（用于管理大语言模型）

## 🛠️ 安装步骤

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd 前端练习
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 3. 安装Ollama模型
使用Ollama安装DeepSeek模型：

```bash
# 安装基础版本
ollama pull deepseek-coder

# 或安装指令调优版本
ollama pull deepseek-coder:instruct

# 或安装聊天版本
ollama pull deepseek-coder:chat
```

## 🚀 启动应用

### 方法1: 使用批处理文件（Windows）
双击 `start_ollama.bat` 文件（推荐）

### 方法2: 命令行启动
```bash
python app.py
```

### 方法3: 设置环境变量启动
```bash
# Windows
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL_NAME=deepseek-coder
python app.py

# Linux/macOS
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL_NAME=deepseek-coder
python app.py
```

## 🌐 访问应用

启动成功后，在浏览器中访问：
- **本地访问**: http://localhost:5000
- **局域网访问**: http://你的IP地址:5000

## 📖 使用说明

### 首次使用
1. 确保Ollama服务正在运行
2. 打开应用后，会看到"模型未加载"状态
3. 点击"加载模型"按钮检查Ollama服务状态
4. 如果Ollama服务正常，状态变为"模型已加载"

### 开始对话
1. 在输入框中输入你的问题或指令
2. 按Enter键或点击"发送"按钮
3. AI会生成回复并显示在对话区域

### 支持的指令类型
- 一般问答
- 代码生成和解释
- 文本创作
- 逻辑推理
- 数学计算

## ⚙️ 配置选项

### 环境变量配置
可以通过环境变量配置Ollama服务：

```bash
# Ollama服务地址
OLLAMA_BASE_URL=http://localhost:11434

# 使用的模型名称
OLLAMA_MODEL_NAME=deepseek-coder

# Flask应用配置
FLASK_ENV=development
FLASK_DEBUG=true
```

### 模型参数调整
在 `config.py` 中可以调整以下参数：

```python
MODEL_CONFIG = {
    'max_length': 512,      # 最大生成长度
    'temperature': 0.7,     # 温度参数（0.1-1.0，越低越确定性）
    'top_p': 0.9,          # top-p采样参数
    'do_sample': True,      # 是否使用采样
}
```

### 端口配置
修改 `config.py` 中的端口设置：
```python
HOST = '0.0.0.0'
PORT = 5000
```

## 🔧 故障排除

### 常见问题

#### 1. Ollama服务连接失败
- 确保Ollama服务正在运行
- 检查Ollama服务地址配置
- 使用 `ollama list` 命令检查模型是否安装

#### 2. 模型未找到
- 使用 `ollama pull deepseek-coder` 安装模型
- 检查模型名称是否正确
- 使用 `ollama list` 查看可用模型

#### 3. 响应速度慢
- 确保Ollama使用GPU加速（如果可用）
- 调整模型参数（temperature、top_p等）
- 使用更小的模型版本

#### 4. 端口被占用
- 修改端口号
- 关闭占用端口的其他应用

### 性能优化建议

1. **使用GPU**: 确保Ollama使用GPU加速，可以显著提升推理速度
2. **模型选择**: 根据需求选择合适的模型版本（base/instruct/chat）
3. **参数调优**: 调整temperature和top_p参数以获得最佳效果
4. **服务优化**: 确保Ollama服务有足够的系统资源

## 📁 项目结构

```
前端练习/
├── app.py                 # Flask后端应用（Ollama集成版）
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── start_ollama.bat      # Ollama版本启动脚本（推荐）
├── start.bat             # 基础启动脚本
├── check_ollama.py       # Ollama服务检查工具
├── README.md             # 项目文档
└── templates/            # HTML模板
    └── index.html       # 主页面
```

## 🔒 安全注意事项

- 此应用完全在本地运行，不会向外部发送数据
- 建议在内网环境中使用
- 如需公网访问，请配置适当的防火墙规则
- 定期更新依赖包以修复安全漏洞

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🙏 致谢

- [DeepSeek AI](https://github.com/deepseek-ai) - 提供优秀的开源大语言模型
- [Hugging Face](https://huggingface.co/) - 提供模型托管和Transformers库
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至：[your-email@example.com]

---

**注意**: 首次运行需要下载模型文件，请确保网络连接正常并有足够的存储空间。
