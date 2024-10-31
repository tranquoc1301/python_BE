from flask import Flask
import os
from .books.controller import books
from .db import db, ma
from .auth import auth
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()  


def create_app():
    app = Flask(__name__)
    app.config.from_object('website.config')  # Lấy cấu hình từ config.py

    # Khởi tạo Mail với app
    mail.init_app(app)

    # Khởi tạo SECRET_KEY nếu chưa có
    if 'SECRET_KEY' not in app.config:
        app.config['SECRET_KEY'] = 'default_secret_key'

    # Khởi tạo database và schema
    db.init_app(app)
    ma.init_app(app)

    # Khởi tạo LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(books)
    app.register_blueprint(auth)

    return app
