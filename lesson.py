from flask import request,jsonify,Blueprint
from .auth.myrole import *
from .models import Lesson
from .app import db

mylesson = Blueprint('mylesson',__name__)



@mylesson.route("/create_lesson", methods=['POST'])
@role_required(1)
def create():
    lid = request.json["lid"]
    title = request.json["title"]
    content = request.json["content"]
    cid = request.json["cid"]
    new_lesson = Lesson(lid=lid,title=title,content=content,cid=cid)
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson created successfully'}), 201




@mylesson.route("/update_lesson/<int:lid>", methods=['PUT'])
@role_required(1)
def update(lid):
    lesson = Lesson.query.get_or_404(lid)
    data = request.get_json()
    lesson.title = data.get("title")
    lesson.content = data.get("content")
    lesson.cid = data.get("cid")
    db.session.commit()
    return jsonify({'message':'Lesson Updated Successfully'})
   

@mylesson.route("/delette_lesson/<int:lid>", methods=['DELETE'])
@role_required(1)
def delete(lid):
    lesson = Lesson.query.get_or_404(lid)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson Deleted Successfully'})

