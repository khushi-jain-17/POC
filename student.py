from flask import request,jsonify,Blueprint
from .auth.myrole import *
from .models import Enroll,Progress,Course,User,Assignment
from .app import db

student_track = Blueprint("student_track",__name__)



@student_track.route('/progress/track',methods=['POST'])
@role_required(2)
def my_progress():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    lesson_completed = data.get("lesson_completed")
    eid = db.session.query(Enroll.eid).filter(Enroll.uid==uid).first()
    id = eid[0]
    lessons=5
    total = (lesson_completed/lessons) * 100
    myprogress = f"{total}%"
    progress = Progress(uid=uid, cid=cid,eid=id, lesson_completed=lesson_completed, myprogress=myprogress)
    db.session.add(progress)
    db.session.commit()
    return jsonify({"message": "Progress recorded successfully"}), 201


@student_track.route('/dashboard/progress',methods=['GET'])
@role_required(1)
def progress_dashboard():
    query = db.session.query(
        Progress.lesson_completed,
        Progress.myprogress,
        Enroll.eid,
        Enroll.etime,
        User.uname,
        Course.cname
    ).join(
        Course,Progress.cid == Course.cid
    ).join(
        User, Progress.uid == User.uid
    ).join(
        Enroll, Progress.eid == Enroll.eid
    )
    results = query.all()
    output = []
    for result in results:
        output.append({
            'lesson_completed': result[0],
            'progess': result[1],
            'eid': result[2],
            'etime': result[3],
            'user_name': result[4],
            'course_name': result[5],
        })
    return jsonify(output), 


@student_track.route("/create/assignment", methods=['POST'])
@role_required(1)
def create():
    qid = request.json["qid"]
    question = request.json["question"]
    cid = request.json["cid"]
    adata = Assignment(qid=qid,question=question,cid=cid)
    db.session.add(adata)
    db.session.commit()
    return jsonify({'message': 'Assignment created successfully'}), 201


@student_track.route('/check_eligibility', methods=['GET'])
@role_required(2)
def check_eligibility():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    progress = Progress.query.filter_by(uid=uid, cid=cid).first()
    if not progress:
        return jsonify({"error": "Progress not found for the student in this course."}), 404
    if progress.myprogress == "100%":
        return jsonify({"message": "You are eligible for the assignment."}), 200
    else:
        return jsonify({"message": "Keep working! You are not eligible for the assignment yet."}), 200