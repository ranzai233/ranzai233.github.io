#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek模型下载脚本
用于预先下载模型文件，避免首次运行时等待
"""

import os
import sys
import argparse
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def download_model(model_name, output_dir, model_type="base"):
    """下载DeepSeek模型"""
    
    # 支持的模型列表
    supported_models = {
        "base": "deepseek-ai/deepseek-coder-6.7b-base",
        "instruct": "deepseek-ai/deepseek-coder-6.7b-instruct",
        "chat": "deepseek-ai/deepseek-coder-6.7b-chat",
        "math": "deepseek-ai/deepseek-math-7b-instruct"
    }
    
    if model_type not in supported_models:
        print(f"错误: 不支持的模型类型 '{model_type}'")
        print(f"支持的模型类型: {', '.join(supported_models.keys())}")
        return False
    
    model_path = supported_models[model_type]
    
    if model_name:
        model_path = model_name
    
    print(f"正在下载模型: {model_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    try:
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("步骤 1/2: 下载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=True,
            cache_dir=output_dir
        )
        
        # 保存tokenizer
        tokenizer_path = os.path.join(output_dir, "tokenizer")
        tokenizer.save_pretrained(tokenizer_path)
        print(f"✓ Tokenizer已保存到: {tokenizer_path}")
        
        print("\n步骤 2/2: 下载模型...")
        print("注意: 这可能需要很长时间，取决于你的网络速度...")
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="cpu",  # 下载时使用CPU
            trust_remote_code=True,
            cache_dir=output_dir
        )
        
        # 保存模型
        model_path_local = os.path.join(output_dir, "model")
        model.save_pretrained(model_path_local)
        print(f"✓ 模型已保存到: {model_path_local}")
        
        print("\n🎉 模型下载完成！")
        print(f"模型文件位置: {output_dir}")
        print("\n现在你可以修改 config.py 中的 local_model_path 来使用本地模型")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="下载DeepSeek模型")
    parser.add_argument(
        "--model-type", 
        choices=["base", "instruct", "chat", "math"],
        default="base",
        help="模型类型 (默认: base)"
    )
    parser.add_argument(
        "--model-name",
        help="自定义模型名称或路径"
    )
    parser.add_argument(
        "--output-dir",
        default="./models/deepseek-coder-6.7b-base",
        help="输出目录 (默认: ./models/deepseek-coder-6.7b-base)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("           DeepSeek 模型下载工具")
    print("=" * 60)
    print()
    
    # 检查磁盘空间
    output_path = Path(args.output_dir)
    if output_path.exists():
        print(f"警告: 输出目录已存在: {args.output_dir}")
        response = input("是否继续？这可能会覆盖现有文件 (y/N): ")
        if response.lower() != 'y':
            print("下载已取消")
            return
    
    # 估算所需空间
    estimated_size = {
        "base": "约13GB",
        "instruct": "约13GB", 
        "chat": "约13GB",
        "math": "约14GB"
    }
    
    print(f"预估所需空间: {estimated_size[args.model_type]}")
    print()
    
    # 开始下载
    success = download_model(args.model_name, args.output_dir, args.model_type)
    
    if success:
        print("\n✅ 下载成功完成！")
        print("\n下一步:")
        print("1. 修改 config.py 中的 local_model_path 为你的模型路径")
        print("2. 运行 python app.py 启动应用")
    else:
        print("\n❌ 下载失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()

