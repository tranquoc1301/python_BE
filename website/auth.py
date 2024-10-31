from flask import Blueprint, request, jsonify, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail
from .db import db
from .models import Students
from flask_login import login_user
from itsdangerous import URLSafeTimedSerializer
import os

# Khởi tạo các thành phần
bcrypt = Bcrypt()
mail = Mail()  # Khởi tạo Mail
s = URLSafeTimedSerializer(os.environ.get('KEY'))
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    student = Students.query.filter_by(username=username).first()

    # Kiểm tra xem người dùng có hoạt động hay không
    if student and student.is_active and bcrypt.check_password_hash(student.password, password):
        login_user(student)
        return jsonify({
            "message": "Login successful!",
            "user": {
                "id": student.id,
                "fullname": student.fullname
            }
        }), 200

    return jsonify({"error": "Incorrect username or password, or the account is inactive."}), 401


@auth.route('/signup', methods=['POST'])
def signup():
    id = request.json.get('id')
    fullname = request.json.get('fullname')
    gender = request.json.get('gender')
    class_name = request.json.get('class_name')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match."}), 400
    if Students.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    # Mã hóa mật khẩu
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_student = Students(
        id=id,
        fullname=fullname,
        gender=gender,
        class_name=class_name,
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )

    db.session.add(new_student)
    db.session.commit()

    # Tạo token xác nhận và gửi email
    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    send_welcome_email(email, fullname)
    send_confirmation_email(email, confirm_url)

    return jsonify({"message": "Sign Up successful! Please check your email to confirm your account."}), 201

# Hàm gửi email xác nhận


def send_confirmation_email(email, confirm_url):
    msg = Message('Confirm your account', recipients=[email])
    msg.body = f'Please click the following link to confirm your account: {confirm_url}'
    mail.send(msg)


def send_welcome_email(email, fullname):
    msg = Message('Welcome to Our Community!',
                  sender='dutlibrary1301@gmail.com',
                  recipients=[email])
    msg.body = (
        f'Hello {fullname},\n\n'
        'Welcome to our community! We are thrilled to have you join us.\n\n'
        'Feel free to explore our features and don’t hesitate to reach out if you need any assistance.\n\n'
        'To get full access to all our features, please confirm your email address.\n\n'
        'Thank you for joining us! We’re excited to see you in our community.\n\n'
        'Best regards,\n'
    )
    mail.send(msg)


@auth.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm',
                        max_age=3600)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    student = Students.query.filter_by(email=email).first()

    # Kích hoạt tài khoản
    student.is_active = True
    db.session.commit()
    return render_template('mail_confirm_success.html'), 200

