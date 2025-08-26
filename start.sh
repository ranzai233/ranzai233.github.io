#!/bin/bash

echo "========================================"
echo "   DeepSeek AI 助手 - 启动脚本"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "检查Python依赖..."
if ! python3 -c "import flask, torch, transformers" &> /dev/null; then
    echo "警告: 缺少必要的Python依赖包"
    echo "正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖包安装失败"
        exit 1
    fi
fi

echo "依赖检查完成"
echo

# 设置环境变量
export FLASK_ENV=development
export FLASK_DEBUG=true

echo "环境变量设置完成："
echo "- FLASK_ENV: $FLASK_ENV"
echo "- FLASK_DEBUG: $FLASK_DEBUG"
echo

# 询问是否自动加载模型
read -p "是否在启动时自动加载模型？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    export AUTO_LOAD_MODEL=true
    echo "- AUTO_LOAD_MODEL: $AUTO_LOAD_MODEL"
    echo
fi

echo "正在启动应用..."
echo "注意：首次运行可能需要下载模型文件，请耐心等待..."
echo

# 启动应用
python3 app.py

