#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama服务状态检查脚本
用于检查Ollama服务是否正常运行以及模型是否可用
"""

import requests
import json
import sys
import os

def check_ollama_service(base_url="http://localhost:11434"):
    """检查Ollama服务状态"""
    try:
        print(f"正在检查Ollama服务: {base_url}")
        
        # 检查服务是否运行
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✓ Ollama服务正在运行")
            return True
        else:
            print(f"✗ Ollama服务响应异常: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到Ollama服务，请确保Ollama正在运行")
        return False
    except requests.exceptions.Timeout:
        print("✗ Ollama服务响应超时")
        return False
    except Exception as e:
        print(f"✗ 检查Ollama服务时出错: {str(e)}")
        return False

def list_available_models(base_url="http://localhost:11434"):
    """列出可用的模型"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            if models:
                print(f"\n可用的模型 ({len(models)}个):")
                print("-" * 50)
                for i, model in enumerate(models, 1):
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 0)
                    size_mb = size / (1024 * 1024) if size > 0 else 0
                    modified = model.get('modified_at', 'Unknown')
                    
                    print(f"{i}. {name}")
                    print(f"   大小: {size_mb:.1f} MB")
                    print(f"   修改时间: {modified}")
                    print()
            else:
                print("\n⚠ 没有找到可用的模型")
                print("请使用以下命令安装模型:")
                print("  ollama pull deepseek-coder")
                print("  ollama pull deepseek-coder:instruct")
                print("  ollama pull deepseek-coder:chat")
                
            return models
        else:
            print(f"✗ 获取模型列表失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"✗ 获取模型列表时出错: {str(e)}")
        return []

def test_model_generation(base_url="http://localhost:11434", model_name="deepseek-coder"):
    """测试模型生成功能"""
    try:
        print(f"\n正在测试模型生成: {model_name}")
        
        test_prompt = "你好，请简单介绍一下你自己"
        
        request_data = {
            "model": model_name,
            "prompt": test_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 100
            }
        }
        
        response = requests.post(
            f"{base_url}/api/generate",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '').strip()
            
            if ai_response:
                print("✓ 模型生成测试成功")
                print(f"测试提示: {test_prompt}")
                print(f"AI回复: {ai_response[:100]}...")
                return True
            else:
                print("✗ 模型生成测试失败: 回复为空")
                return False
        else:
            print(f"✗ 模型生成测试失败: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ 模型生成测试超时")
        return False
    except Exception as e:
        print(f"✗ 模型生成测试出错: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("           Ollama 服务检查工具")
    print("=" * 60)
    print()
    
    # 从环境变量获取配置
    base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    model_name = os.environ.get('OLLAMA_MODEL_NAME', 'deepseek-coder')
    
    print(f"配置信息:")
    print(f"- Ollama服务地址: {base_url}")
    print(f"- 默认模型名称: {model_name}")
    print()
    
    # 检查服务状态
    service_ok = check_ollama_service(base_url)
    
    if not service_ok:
        print("\n❌ Ollama服务检查失败")
        print("\n请确保:")
        print("1. Ollama已正确安装")
        print("2. Ollama服务正在运行")
        print("3. 服务地址配置正确")
        sys.exit(1)
    
    # 列出可用模型
    models = list_available_models(base_url)
    
    if not models:
        print("\n❌ 没有可用的模型")
        sys.exit(1)
    
    # 检查指定模型是否存在
    model_names = [model.get('name', '') for model in models]
    
    if model_name not in model_names:
        print(f"\n⚠ 指定的模型 '{model_name}' 未找到")
        print(f"可用模型: {', '.join(model_names)}")
        print(f"\n请使用以下命令安装模型:")
        print(f"  ollama pull {model_name}")
        
        # 询问是否测试其他模型
        if models:
            first_model = models[0]['name']
            print(f"\n是否测试第一个可用模型 '{first_model}'? (y/N): ", end="")
            response = input().strip().lower()
            if response == 'y':
                model_name = first_model
            else:
                sys.exit(1)
    
    # 测试模型生成
    generation_ok = test_model_generation(base_url, model_name)
    
    if generation_ok:
        print(f"\n🎉 Ollama服务检查完成！")
        print(f"✓ 服务地址: {base_url}")
        print(f"✓ 模型名称: {model_name}")
        print(f"✓ 模型生成: 正常")
        print(f"\n现在可以启动Flask应用了:")
        print(f"  python app.py")
    else:
        print(f"\n❌ 模型生成测试失败")
        print(f"请检查模型是否正确安装")

if __name__ == "__main__":
    main()

