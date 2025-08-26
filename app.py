from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging
import os
from config import get_config

# 获取配置
config = get_config()

app = Flask(__name__)
app.config.from_object(config)
CORS(app, origins=config.CORS_ORIGINS)

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Ollama配置
OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL_NAME = os.environ.get('OLLAMA_MODEL_NAME', 'deepseek-coder')

def check_ollama_status():
    """检查Ollama服务状态"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            # 检查是否有所需的模型
            model_names = [model['name'] for model in models]
            if OLLAMA_MODEL_NAME in model_names:
                logger.info(f"Ollama服务正常，找到模型: {OLLAMA_MODEL_NAME}")
                return True
            else:
                logger.warning(f"Ollama服务正常，但未找到模型: {OLLAMA_MODEL_NAME}")
                logger.info(f"可用模型: {', '.join(model_names)}")
                return False
        else:
            logger.error(f"Ollama服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"无法连接到Ollama服务: {str(e)}")
        return False

def load_model():
    """检查Ollama模型状态"""
    try:
        logger.info("正在检查Ollama服务状态...")
        if check_ollama_status():
            logger.info("Ollama模型检查完成！")
            return True
        else:
            logger.error("Ollama模型检查失败")
            return False
    except Exception as e:
        logger.error(f"模型检查失败: {str(e)}")
        return False

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI对话接口 - 通过Ollama调用"""
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({'error': '请输入消息'}), 400
            
        # 检查Ollama服务状态
        if not check_ollama_status():
            return jsonify({'error': 'Ollama服务不可用或模型未找到'}), 500
            
        # 构建Ollama API请求
        ollama_request = {
            "model": OLLAMA_MODEL_NAME,
            "prompt": user_input,
            "stream": False,
            "options": {
                "temperature": config.MODEL_CONFIG['temperature'],
                "top_p": config.MODEL_CONFIG['top_p'],
                "num_predict": config.MODEL_CONFIG['max_length']
            }
        }
        
        # 调用Ollama API
        logger.info(f"正在调用Ollama模型: {OLLAMA_MODEL_NAME}")
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=ollama_request,
            timeout=120  # 120秒超时，给模型更多时间思考
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '').strip()
            
            if ai_response:
                return jsonify({
                    'response': ai_response,
                    'status': 'success'
                })
            else:
                return jsonify({'error': 'AI回复为空'}), 500
        else:
            logger.error(f"Ollama API调用失败: {response.status_code} - {response.text}")
            return jsonify({'error': f'Ollama API调用失败: {response.status_code}'}), 500
        
    except requests.exceptions.Timeout:
        logger.error("Ollama API调用超时")
        return jsonify({'error': 'AI响应超时，请稍后重试'}), 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API请求异常: {str(e)}")
        return jsonify({'error': f'网络请求失败: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"生成回复时出错: {str(e)}")
        return jsonify({'error': f'生成回复失败: {str(e)}'}), 500

@app.route('/api/status')
def status():
    """检查Ollama服务状态"""
    try:
        is_available = check_ollama_status()
        return jsonify({
            'model_loaded': is_available,
            'status': 'ready' if is_available else 'loading',
            'ollama_url': OLLAMA_BASE_URL,
            'model_name': OLLAMA_MODEL_NAME
        })
    except Exception as e:
        logger.error(f"状态检查失败: {str(e)}")
        return jsonify({
            'model_loaded': False,
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/load_model', methods=['POST'])
def load_model_api():
    """检查Ollama模型状态接口"""
    try:
        success = load_model()
        if success:
            return jsonify({
                'message': f'Ollama模型 {OLLAMA_MODEL_NAME} 检查成功', 
                'status': 'success'
            })
        else:
            return jsonify({
                'error': f'Ollama模型 {OLLAMA_MODEL_NAME} 检查失败，请确保Ollama服务正在运行', 
                'status': 'error'
            }), 500
    except Exception as e:
        return jsonify({'error': f'模型检查失败: {str(e)}', 'status': 'error'}), 500

if __name__ == '__main__':
    # 启动时检查Ollama服务
    print("正在启动Flask应用...")
    print(f"配置环境: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"监听地址: {config.HOST}:{config.PORT}")
    print(f"Ollama服务地址: {OLLAMA_BASE_URL}")
    print(f"Ollama模型名称: {OLLAMA_MODEL_NAME}")
    print()
    
    # 根据配置决定是否自动检查模型
    if config.AUTO_LOAD_MODEL:
        print("正在检查Ollama服务状态...")
        if load_model():
            print("✓ Ollama服务检查成功！")
        else:
            print("⚠ Ollama服务检查失败，请确保Ollama正在运行")
    else:
        print("跳过Ollama服务检查，启动后手动检查")
    
    print()
    app.run(
        debug=config.DEBUG, 
        host=config.HOST, 
        port=config.PORT
    )
