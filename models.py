from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Gallery(db.Model):
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Admission(db.Model):
    __tablename__ = "admissions"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    course_name = db.Column(db.String(100), nullable=False)

    duration = db.Column(db.String(50), nullable=False)

    fees = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text)

    image_path = db.Column(db.String(255))

class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    designation = db.Column(db.String(100), nullable=False)

    qualification = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    experience = db.Column(db.String(50), nullable=False)

    image_path = db.Column(db.String(255), nullable=False)