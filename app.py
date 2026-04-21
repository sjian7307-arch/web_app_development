from flask import Flask
from app.routes import register_routes
from app.models.db import init_db

def create_app():
    app = Flask(__name__)
    # 設定 SECRET_KEY，用來保護 flash message 與 session
    app.config['SECRET_KEY'] = 'dev_secret_key'

    # 確保資料庫初始化
    init_db()

    # 註冊所有路由
    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
