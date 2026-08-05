from flask import jsonify, request


from db import db
from models.lightsabers import Lightsabers, lightsaber_schema, lightsabers_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate

@authenticate_return_auth
def add_lightsaber(auth_info):
    if auth_info.user.force_rank == 'Youngling':
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.get_json()

    new_lightsaber = Lightsabers.new_lightsaber_object()

    populate_object(new_lightsaber, post_data)

    try:
        db.session.add(new_lightsaber)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({
        "message": "lightsaber created",
        "result": lightsaber_schema.dump(new_lightsaber)
    }), 201


@authenticate
def get_lightsaber_by_owner_id(owner_id):
    
    lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.owner_id == owner_id).first()

    return jsonify ({
        "message": "lightsaber found",
        "results": lightsaber_schema.dump(lightsaber_query)
    }),200


@authenticate_return_auth
def update_saber_by_id(saber_id, auth_info):
    post_data = request.form if request.form else request.json

    saber_query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()

    if not saber_query:
        return jsonify({"message": "unable to update record"}), 400

    if auth_info.user.user_id != saber_query.owner_id:
        return jsonify({"message": "unauthorized"}), 401

    populate_object(saber_query, post_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "saber updated", "result": lightsaber_schema.dump(saber_query)}), 200



@authenticate_return_auth
def delete_saber_by_id(saber_id, auth_info):
    saber_query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()

    if not saber_query:
        return jsonify({"message": "saber not found"}), 404

    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.user.user_id != saber_query.owner_id:
        return jsonify({"message": "unauthorized"}), 401

    db.session.delete(saber_query)
    db.session.commit()

    return jsonify({
        "message": "saber destroyed"
    }), 200