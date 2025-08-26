# 🚀 DeepSeek AI 助手 - 快速启动指南

## 📋 前置要求

1. **安装Python 3.8+**
2. **安装Ollama** - [下载地址](https://ollama.ai/)
3. **安装DeepSeek模型**

## ⚡ 5分钟快速启动

### 步骤1: 安装Python依赖
```bash
pip install -r requirements.txt
```

### 步骤2: 安装DeepSeek模型
```bash
# 启动Ollama服务（如果还没启动）
ollama serve

# 安装模型（选择其中一个）
ollama pull deepseek-coder        # 基础版本
ollama pull deepseek-coder:instruct  # 指令调优版本
ollama pull deepseek-coder:chat      # 聊天版本
```

### 步骤3: 检查Ollama服务
```bash
python check_ollama.py
```

### 步骤4: 启动应用
```bash
# Windows用户
start_ollama.bat

# 或手动启动
python app.py
```

### 步骤5: 访问应用
打开浏览器访问: http://localhost:5000

## 🔧 常见问题解决

### Q: Ollama服务无法连接
**A:** 确保Ollama服务正在运行
```bash
# Windows
ollama serve

# macOS/Linux
ollama serve &
```

### Q: 模型未找到
**A:** 检查已安装的模型
```bash
ollama list
```

### Q: 响应速度慢
**A:** 检查Ollama是否使用GPU
```bash
ollama ps
```

## 📱 使用说明

1. **加载模型**: 点击"加载模型"按钮检查服务状态
2. **开始对话**: 在输入框中输入问题，按Enter发送
3. **支持功能**: 代码生成、问答、文本创作等

## 🌟 推荐配置

```bash
# 环境变量配置
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL_NAME=deepseek-coder:instruct
set FLASK_ENV=development
```

## 📞 获取帮助

- 运行 `python check_ollama.py` 诊断问题
- 查看 `README.md` 获取详细文档
- 检查控制台日志信息

---

**提示**: 首次启动可能需要几分钟来检查Ollama服务状态。

