from flask import request,jsonify,Blueprint
from .auth.myrole import *
from .models import Enroll,Progress,Course,User,Assignment
from .app import db
from datetime import datetime, timedelta
from sqlalchemy import func 

student_track = Blueprint("student_track",__name__)



@student_track.route('/progress/track',methods=['POST'])
@role_required(2)
def my_progress():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    created_at = datetime.now().strftime("%Y-%m-%dT%H:%M")
    lesson_completed = data.get("lesson_completed")
    eid = db.session.query(Enroll.eid).filter(Enroll.uid==uid).first()
    id = eid[0]
    lessons=5
    total = (lesson_completed/lessons) * 100
    myprogress = f"{total}%"
    progress = Progress(uid=uid, cid=cid, created_at=created_at,eid=id, lesson_completed=lesson_completed, myprogress=myprogress)
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
    
 
@student_track.route('/eligibility', methods=['GET'])
@role_required(2)
def CheckEligibility():
    data = request.get_json()
    uid = data.get("uid")
    cid = data.get("cid")
    assignments = Assignment.query.filter_by(cid=cid).all()
    serialized_assignments = [assignment.serialize() for assignment in assignments]
    # myprogress = Progress.query.filter_by(uid=uid, cid=cid)
    # myprogress = Progress.query.filter_by(uid=uid, cid=cid).order_by(Progress.created_at.desc()).first()

    myprogress=(db.session.query(Progress.sid, Progress.cid,func.max(Progress.created_at).label('created_at'))
                   .group_by(Progress.sid, Progress.cid)
                   .first())
    # myprogress = Progress.query.filter_by(uid=uid, cid=cid).order_by(Progress.sid.desc())
    if not myprogress:
        return jsonify({"error": "Progress not found for the student in this course."}), 404
    if myprogress == "100%" :
        return jsonify({"message":"you are eligible"}), 200
    else:
        return jsonify({"message": "Keep working! You are not eligible for the assignment yet."}), 200
    

@student_track.route('/assignments/<int:cid>', methods=['GET'])
def get_assignments_by_course(cid):
    assignments = Assignment.query.filter_by(cid=cid).all()
    serialized_assignments = [assignment.serialize() for assignment in assignments]
    return jsonify(serialized_assignments)

