import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow

load_dotenv()

# Khởi tạo SQLAlchemy
db = SQLAlchemy()
ma = Marshmallow()