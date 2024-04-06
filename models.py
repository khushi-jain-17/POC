from .app import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime


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
    rating = db.Column(db.Float,nullable=False)
    lessons = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'cid': self.cid,
            'cname': self.cname,
            'description': self.description,
            'lessons': [lesson.serialize() for lesson in self.lessons]
        }



class Lesson(db.Model):
    __tablename__ = 'lessons'

    lid = db.Column(db.Integer, primary_key=True)
    l_id = db.Column(db.Integer)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'))
    course = db.relationship('Course', back_populates='lessons')

    def serialize(self):
        return {
            'l_id': self.l_id,
            'title': self.title,
            'content': self.content,
        }


class Enroll(db.Model):
    __tablename__ = 'enrolls'

    eid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    epassword = db.Column(db.String(500),nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'), nullable=False)
    etime = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), default=2)  
    role = db.relationship('Role', backref=db.backref('enrolls', lazy=True))
    course = db.relationship('Course',backref=db.backref('courses',lazy=True))
    user = db.relationship('User',backref=db.backref('users',lazy=True))

