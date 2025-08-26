@echo off
echo ========================================
echo    DeepSeek AI 助手 - Ollama版本
echo ========================================
echo.
echo 正在设置环境变量...
set FLASK_ENV=development
set AUTO_LOAD_MODEL=true
set FLASK_DEBUG=true
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL_NAME=deepseek-r1:latest
echo.
echo 环境变量设置完成：
echo - FLASK_ENV: %FLASK_ENV%
echo - AUTO_LOAD_MODEL: %AUTO_LOAD_MODEL%
echo - FLASK_DEBUG: %FLASK_DEBUG%
echo - OLLAMA_BASE_URL: %OLLAMA_BASE_URL%
echo - OLLAMA_MODEL_NAME: %OLLAMA_MODEL_NAME%
echo.
echo 请确保：
echo 1. Ollama服务正在运行
echo 2. 已安装 deepseek-coder 模型
echo 3. 可以通过 ollama list 查看模型
echo.
pause
python app.py
pause

