@echo off
echo ========================================
echo    DeepSeek AI 助手 - 自动加载模型版
echo ========================================
echo.
echo 正在设置环境变量...
set FLASK_ENV=development
set AUTO_LOAD_MODEL=true
set FLASK_DEBUG=true
echo.
echo 环境变量设置完成：
echo - FLASK_ENV: %FLASK_ENV%
echo - AUTO_LOAD_MODEL: %AUTO_LOAD_MODEL%
echo - FLASK_DEBUG: %FLASK_DEBUG%
echo.
echo 正在启动应用...
echo 注意：首次运行需要下载模型文件，请耐心等待...
echo.
pause
python app.py
pause

