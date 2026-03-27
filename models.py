from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    credits_completed = db.Column(db.Integer, default=0)
    gpa = db.Column(db.Float, default=0.0)
    is_honors = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), nullable=False)