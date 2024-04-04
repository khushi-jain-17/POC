from .app import db
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True )
    uname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)


class Role(db.Model):
    __tablename__ = 'roles'
    
    role_id = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(100), unique=True, nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), default=1)
    role = db.relationship('Role', backref=db.backref('admin', lazy=True))


class Course(db.Model):
    __tablename__ = 'courses'

    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500),nullable=False)
    fee = db.Column(db.String(100))
    ctime = db.Column(db.String(100),nullable=True)
    rating = db.Column(db.Float)



class Lesson(db.Model):
    __tablename__ = 'lessons'

    lid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'))
    # course = relationship('Course', back_populates='lessons')
    course = db.relationship('Course', backref=db.backref('lessons', lazy=True))
