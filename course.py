from flask import request,jsonify,Blueprint
from .auth.myrole import *
from .models import Course
from .app import db

mycourse = Blueprint('mycourse',__name__)


@mycourse.route("/create_course", methods=['POST'])
@role_required(1)
def create():
    cid = request.json["cid"]
    cname = request.json["cname"]
    description = request.json["description"]
    fee = request.json["fee"]
    ctime = request.json["ctime"]
    rating = request.json["rating"]
    new_course = Course(cid=cid,cname=cname,description=description,fee=fee,ctime=ctime,rating=rating)
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'course created successfully'}), 201



@mycourse.route('/get_course', methods=['GET'])
@role_required(1)
def get_course():
    course = Course.query.all()
    output = []
    for c in course:
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
