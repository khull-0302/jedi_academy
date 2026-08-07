from flask import jsonify, request


from db import db
from models.courses import Courses, course_schema, courses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth

@authenticate_return_auth
def add_course(auth_info):
    if auth_info.user.force_rank not in ['Master', 'Council Member', 'Grand Master']:
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json

    new_course = Courses.new_course_object()

    populate_object(new_course, post_data)

    try:
        db.session.add(new_course)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "course created", "result": course_schema.dump(new_course)}), 201


def get_courses_by_difficulty(difficulty):
    course_query = (
        db.session.query(Courses)
        .filter(Courses.difficulty == difficulty)
        .all()
    )

    return jsonify({
        "message": "courses found",
        "results": courses_schema.dump(course_query)
    }), 200

@authenticate_return_auth
def update_course(course_id, auth_info):
    post_data = request.form if request.form else request.json

    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not course_query:
        return jsonify({"message": "unable to update record"}), 400

    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.user.user_id != course_query.instructor_id:
        return jsonify({"message": "unauthorized"}), 401

    populate_object(course_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "course updated", "result": course_schema.dump(course_query)}), 200



@authenticate_return_auth
def delete_course_by_id(course_id, auth_info):
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not course_query:
        return jsonify({"message": "course not found"}), 404

    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.user.user_id != course_query.instructor_id:
        return jsonify({"message": "unauthorized"}), 401

    db.session.delete(course_query)
    db.session.commit()

    return jsonify({
        "message": "course deleted"
    }), 200