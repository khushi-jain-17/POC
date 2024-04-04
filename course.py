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
def get_courses():
    course = Course.query.all()
    output = []
    for c in course:
        course_data = {
            'cid': c.cid,
            'cname': c.cname,
            'description':c.description,
            'fee':c.fee,
            'ctime':c.ctime,
            'rating':c.rating
        }
        output.append(course_data)
    return jsonify(output)


@mycourse.route('/get_course/<int:cid>',methods=['GET'])
@role_required(1)
def getbyid(cid):
    course = Course.query.get_or_404(cid)
    output=[]
    cdata = {
        'cname': course.cname,
        'description': course.description,
        'fee':course.fee,
        'ctime':course.ctime,
        'rating':course.rating
    }
    output.append(cdata)
    return jsonify({'course':output})


@mycourse.route("/update_course/<int:cid>",methods=['PUT'])
@role_required(1)
def update(cid):
    course = Course.query.get_or_404(cid)
    data = request.get_json()
    course.cname = data.get("cname")
    course.description = data.get("description")
    course.fee = data.get("fee")
    course.ctime = data.get("ctime")
    course.rating = data.get("rating")
    db.session.commit()
    return jsonify({'message':'Course Updated Successfully'})


@mycourse.route("/delete_course/<int:cid>", methods=['DELETE'])
@role_required(1)
def delete(cid):
    course = Course.query.get_or_404(cid)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course Deleted Successfully'})



@mycourse.route('/course/<int:cid>', methods=['GET'])
@role_required(1)
def course_analytics(cid):
    course = Course.query.get(cid)
    if course:
        return jsonify(course.serialize())
    else:
        return jsonify({'error': 'Course not found'}), 404
    

@mycourse.route('/sorting',methods=['GET'])
def sorting():
    courses = Course.query.order_by(Course.rating.desc()).all()
    output = []
    for c in courses:
        course_data = {
            'cid': c.cid,
            'cname': c.cname,
            'description':c.description,
            'fee':c.fee,
            'ctime':c.ctime,
            'rating':c.rating
        }
        output.append(course_data)
    return jsonify(output)


@mycourse.route("/course", methods=['GET'])
def paginate():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    course = Course.query.paginate(
        page=page, per_page=per_page, error_out=True
    )
    output = []
    for c in course:
        cdata = {
            "cid": c.cid,
            'cname': c.cname,
            'description':c.description,
            'fee':c.fee,
            'ctime':c.ctime,
            'rating':c.rating
        }
        output.append(cdata)
    return jsonify({"course": output})


# @mycourse.route('/searching',methods=['GET'])
# def search():

#     query = Course.query.filter(Course.cname.ilike("%keyword%"))



@app.route('/courses/search', methods=['GET'])
def search_courses():
    keyword = request.args.get('keyword')
    query = Course.query
    if keyword:
        query = query.filter(Course.cname.ilike(f"%{keyword}%"))
    courses = query.all()
    data = [{'cid': course.cid, 'cname': course.cname, 'description': course.description, 'fee': course.fee, 'ctime': course.ctime, 'rating': course.rating} for course in courses]
    return jsonify(data)    