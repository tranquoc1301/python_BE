from .db import ma


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "fullname", "gender", "class_name",
                  "username", "email", "role", "created_on", "updated_on", "is_active")


class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "category_id", "title", "publish_year",
                  "author", "publisher", "summary", "cover", "view_count", "download_count", "file_path")


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "image")


class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_id", "student_id",
                  "content", "created_on", "updated_on")


class FavoriteSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_id", "student_id", "added_on")
