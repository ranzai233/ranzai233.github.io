# DeepSeek AI 助手配置文件

import os

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 模型配置
    MODEL_CONFIG = {
        # Ollama模型参数
        'max_length': 256,           # 减少最大生成长度，提高响应速度
        'temperature': 0.5,          # 降低温度参数，减少随机性，提高速度
        'top_p': 0.8,               # 降低top-p采样，提高速度
        'do_sample': True,           # 是否使用采样
    }
    
    # 应用配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # 是否自动加载模型
    AUTO_LOAD_MODEL = os.environ.get('AUTO_LOAD_MODEL', 'false').lower() == 'true'
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 安全配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # 性能配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB最大请求大小
    
    @classmethod
    def get_ollama_config(cls):
        """获取Ollama配置"""
        return {
            'base_url': os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'model_name': os.environ.get('OLLAMA_MODEL_NAME', 'deepseek-coder'),
            'timeout': 60
        }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """获取配置对象"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
