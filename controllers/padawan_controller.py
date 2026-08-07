from flask import jsonify, request


from db import db
from models.padawan import Padawans, padawan_schema, padawans_schema
from models.courses import Courses, course_schema, courses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate

@authenticate_return_auth
def add_padawan(auth_info):
    if auth_info.user.force_rank not in ['Master', 'Grand Master', 'Council Member']:
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.get_json()

    new_padawan = Padawans.new_padawan_object()

    populate_object(new_padawan, post_data)

    try:
        db.session.add(new_padawan)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({
        "message": "padawan created",
        "result": padawan_schema.dump(new_padawan)
    }), 201

@authenticate_return_auth
def add_padawan_course_association(auth_info):
    post_data = request.form if request.form else request.json
    padawan_id = post_data.get('padawan_id')
    course_id = post_data.get('course_id')

    if auth_info.user.force_rank not in ['Master', 'Grand Master', 'Council Member']:
            return jsonify({"message": "unauthorized"}), 401

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not padawan_query or not course_query:
        return jsonify({
            "message": "padawan or course record does not exist"
        }), 400
    
    if padawan_query and course_query:
        padawan_query.courses.append(course_query)
        db.session.commit()

    return jsonify({
        "message": "course added to padawan", "result": padawan_schema.dump(padawan_query)
    })



@authenticate_return_auth
def get_all_padawans(auth_info):
    if auth_info.user.force_rank not in ['Master', 'Council Member', 'Grand Master']:
            return jsonify({"message": "unauthorized"}), 401
    padawans_query = db.session.query(Padawans).all()
    return jsonify({"message": "padawans found", "results": padawans_schema.dump(padawans_query)}), 200



@authenticate
def get_all_active_padawans():
    padawans_query = db.session.query(Padawans).filter(Padawans.graduation_date == None).all()

    return jsonify ({
        "message": "padawans found",
        "results": padawans_schema.dump(padawans_query)
    }),200


@authenticate_return_auth
def update_padawan_training(padawan_id, auth_info):
    post_data = request.form if request.form else request.json

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "unable to update record"}), 400

    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.user.user_id != padawan_query.master_id:
        return jsonify({"message": "unauthorized"}), 401

    populate_object(padawan_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "padawan updated", "result": padawan_schema.dump(padawan_query)}), 200


@authenticate_return_auth
def promote_padawan(padawan_id, auth_info):
    if auth_info.user.force_rank not in ['Council Member', 'Grand Master']:
        return jsonify({"message": "unauthorized"}), 401

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "unable to update record"}), 400

    padawan_query.user.force_rank = "Grand Master"

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "padawan promoted", "result": padawan_schema.dump(padawan_query)}), 200


@authenticate_return_auth
def delete_padawan_by_id(padawan_id, auth_info):
    if auth_info.user.force_rank not in ['Council Member', 'Grand Master']:
        return jsonify({"message": "unauthorized"}), 401
    
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404

    db.session.delete(padawan_query)
    db.session.commit()

    return jsonify({
        "message": "padawan deleted"
    }), 200