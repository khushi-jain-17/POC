from flask import request,jsonify,Blueprint
from .auth.myrole import *
from .models import Lesson
from .app import db

mylesson = Blueprint('mylesson',__name__)

@mylesson.route("/create_lesson", methods=['POST'])
@role_required(1)
def create():
    lid = request.json["lid"]
    l_id = request.json["l_id"]
    title = request.json["title"]
    content = request.json["content"]
    cid = request.json["cid"]
    new_lesson = Lesson(lid=lid,l_id=l_id,title=title,content=content,cid=cid)
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson created successfully'}), 201


@mylesson.route('/get_lesson', methods=['GET'])
@role_required(1)
def get_lesson():
    lesson = Lesson.query.all()
    output = []
    for l in lesson:
        ldata = {
            'l_id': l.l_id,
            'title': l.title,
            'content':l.content,
            'cid': l.cid,
        }
        output.append(ldata)
    return jsonify(output)


@mylesson.route('/get_course/<int:lid>',methods=['GET'])
@role_required(1)
def getbyid(lid):
    lesson = Lesson.query.get_or_404(lid)
    output=[]
    ldata = {
        'l_id': lesson.l_id,
        'title': lesson.title,
        'content':lesson.content,
        'cid': lesson.cid,
    }
    output.append(ldata)
    return jsonify({'lesson':output})


@mylesson.route("/update_lesson/<int:lid>", methods=['PUT'])
@role_required(1)
def update(lid):
    lesson = Lesson.query.get_or_404(lid)
    data = request.get_json()
    lesson.l_id = data.get("l_id")
    lesson.title = data.get("title")
    lesson.content = data.get("content")
    lesson.cid = data.get("cid")
    db.session.commit()
    return jsonify({'message':'Lesson Updated Successfully'})
   

@mylesson.route("/delete_lesson/<int:lid>", methods=['DELETE'])
@role_required(1)
def delete(lid):
    lesson = Lesson.query.get_or_404(lid)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson Deleted Successfully'})


@mylesson.route("/lessons", methods=['GET'])
def paginate():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    lesson = Lesson.query.paginate(
        page=page, per_page=per_page, error_out=True
    )
    output = []
    for l in lesson:
        ldata = {
            "l_id": l.l_id,
            "title": l.title,
            "content": l.content,
        }
        output.append(ldata)
    return jsonify({"lesson": output})


