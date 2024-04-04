from flask import Blueprint
import jwt 
from flask_bcrypt import  generate_password_hash
from flask_bcrypt import check_password_hash
from datetime import datetime
from datetime import datetime, timedelta
from flask import request,jsonify, Blueprint 
from flask_bcrypt import bcrypt 
from flask_bcrypt import Bcrypt 
from .gen_token import * 
from ..validation import *
from ..app import db
from ..models import User,Course,Admin

bcrypt = Bcrypt(app)

auth=Blueprint('auth',__name__)


@auth.route('/signup',methods=['POST'])
def signup():
    user_schema = UserSchema()
    try:
        validated_data = user_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    existing_user = User.query.filter_by(uid=validated_data['uid']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    hashed_password = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
    new_user = User(uid=validated_data['uid'],uname=validated_data['uname'], email=validated_data['email'], 
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    uid = data.get("uid")
    password = data.get("password")
    user = User.query.filter_by(uid=uid).first()
    if user:
        if bcrypt.check_password_hash(user.password, password):
            courses = Course.query.all()
            output = []
            for c in courses:
                course_data = {
                    'cid': c.cid,
                    'cname': c.cname,
                    'descrifption':c.description,
                    'fee':c.fee,
                    'ctime':c.ctime,
                    'rating':c.rating
                }
                output.append(course_data)
            return jsonify(output)              
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404

@auth.route('/create/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    admin_id = data.get("admin_id")
    password = data.get("password")
    role_id = data.get("role_id")
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_admin = Admin(admin_id=admin_id, password=hashed_password, role_id=role_id)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'}), 201        


@auth.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin_id = data.get("admin_id")
    password = data.get("password")
    admin = Admin.query.filter_by(admin_id=admin_id).first()
    if admin:
        hashed_password = admin.password
        if bcrypt.check_password_hash(hashed_password, password):
            token = jwt.encode({
                'admin_id': admin.admin_id,
                'role_id': admin.role_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'token': token}), 201
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'Admin not found'}), 404