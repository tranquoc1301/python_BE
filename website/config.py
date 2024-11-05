import os

# Cấu hình gửi email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'dutlibrary1301@gmail.com'
MAIL_PASSWORD = 'jxxv bhdn vhbg wcbh'
MAIL_DEFAULT_SENDER = 'dutlibrary1301@gmail.com'

# Cấu hình chung cho Flask
SECRET_KEY = os.environ.get('KEY')  # Lấy từ biến môi trường
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
