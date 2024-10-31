from .db import db


class Students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(10), primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(5), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255), default=None)
    bookmarks = db.Column(db.Text)
    role = db.Column(db.Enum('user', 'admin'), nullable=False, default='user')
    created_on = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, id, fullname, gender, class_name, username, email, password, avatar=None, bookmarks=None, role='user', is_active=True):
        self.id = id
        self.fullname = fullname
        self.gender = gender
        self.class_name = class_name
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.bookmarks = bookmarks
        self.role = role
        self.is_active = is_active

    def get_id(self):
        return self.id


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publish_year = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text)
    cover = db.Column(db.String(255), default=None)
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(255), default=None)

    def __init__(self, category_id, title, publish_year, author, publisher, summary=None, cover=None, view_count=0, download_count=0,  file_path=None):
        self.category_id = category_id
        self.title = title
        self.publish_year = publish_year
        self.author = author
        self.publisher = publisher
        self.summary = summary
        self.cover = cover
        self.view_count = view_count
        self.download_count = download_count
        self.file_path = file_path


class Category(db.Model):
    __table_name__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))

    def __init__(self, category, image=None):
        self.category = category
        self.image = image


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'books.id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey(
        'students.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, nullable=True,
                           server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def __init__(self, book_id, student_id, content):
        self.book_id = book_id
        self.student_id = student_id
        self.content = content


class favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey(
        'students.id'), nullable=False)
    added_on = db.Column(db.TIMESTAMP, nullable=True,
                         server_default=db.func.current_timestamp())

    def __init__(self, book_id, student_id):
        self.book_id = book_id
        self.student_id = student_id
