from flask import jsonify, request


from db import db
from models.master import Masters, master_schema, masters_schema
from models.padawan import Padawans, padawan_schema, padawans_schema
from models.courses import Courses, course_schema, courses_schema

from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth

@authenticate_return_auth
def add_master(auth_info):
    if auth_info.user.force_rank not in ['Grand Master']:
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.get_json()

    new_master = Masters.new_master_object()

    populate_object(new_master, post_data)

    try:
        db.session.add(new_master)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({
        "message": "master created",
        "result": master_schema.dump(new_master)
    }), 201

@authenticate_return_auth
def get_all_masters(auth_info):
    if auth_info.user.force_rank == 'Youngling':
            return jsonify({"message": "unauthorized"}), 401
    masters_query = db.session.query(Masters).all()
    return jsonify({"message": "masters found", "results": masters_schema.dump(masters_query)}), 200


@authenticate_return_auth
def update_master_profile(master_id, auth_info):
    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.master.master_id != master_id:
        return jsonify({"message": "unauthorized"}), 401
    
    post_data = request.form if request.form else request.json

    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if master_query:
        populate_object(master_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400
        
        return jsonify({"message": "master updated", "result": master_schema.dump(master_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

@authenticate_return_auth
def remove_master_status(master_id, auth_info):
    if auth_info.user.force_rank != 'Grand Master':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.json
    new_master_id = post_data.get("new_master_id")

    master_query = db.session.query(Masters).filter(
        Masters.master_id == master_id
    ).first()

    if not master_query:
        return jsonify({"message": "master not found"}), 404

    for padawan in master_query.padawans:
        padawan.master_id = new_master_id

    db.session.delete(master_query)
    db.session.commit()

    return jsonify({
        "message": "master status removed"
    }), 200



@authenticate_return_auth
def delete_master_by_id(master_id, auth_info):
    if auth_info.user.force_rank != 'Grand Master':
        return jsonify({"message": "unauthorized"}), 401
    
    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if not master_query:
        return jsonify({"message": "master not found"}), 404

    db.session.delete(master_query)
    db.session.commit()

    return jsonify({
        "message": "master removed"
    }), 200


@authenticate_return_auth
def order_66(auth_info):
    if auth_info.user.force_rank != 'Grand Master':
        return jsonify({"message": "unauthorized"}), 401

    db.session.query(Padawans).delete()
    db.session.query(Masters).delete()
    db.session.query(Courses).delete()


    db.session.commit()

    return jsonify({
        "message": "order 66 executed"
    }), 200