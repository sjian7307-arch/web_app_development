# 初始化 routes 模組，並提供註冊 Blueprint 的函式
from .event_routes import event_bp
from .registration_routes import registration_bp

def register_routes(app):
    """將所有的 Blueprint 註冊到 Flask 應用程式"""
    app.register_blueprint(event_bp)
    app.register_blueprint(registration_bp)
