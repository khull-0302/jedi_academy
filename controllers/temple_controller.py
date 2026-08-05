from flask import jsonify, request


from db import db
from models.temple import Temples, temple_schema, temples_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


def add_temple():
    post_data = request.form if request.form else request.get_json()

    new_temple = Temples.new_temple_object()

    populate_object(new_temple, post_data)

    try:
        db.session.add(new_temple)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({
        "message": "temple created",
        "result": temple_schema.dump(new_temple)
    }), 201

@authenticate
def get_all_temples():
    temples_query = db.session.query(Temples).all()
    return jsonify({"message": "temples found", "results": temples_schema.dump(temples_query)}), 200


@authenticate
def get_temple_by_id(temple_id):
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    return jsonify ({
        "message": "temple found",
        "results": temple_schema.dump(temple_query)
    }),200


@authenticate_return_auth
def update_temple_by_id(temple_id, auth_info):
    if auth_info.user.force_rank != 'Grand Master':
        return jsonify({"message": "unauthorized"}), 401
    
    post_data = request.form if request.form else request.json

    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if temple_query:
        populate_object(temple_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400
        
        return jsonify({"message": "temple updated", "result": temple_schema.dump(temple_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


@authenticate_return_auth
def deactivate_temple_by_id(temple_id, auth_info):
    if auth_info.user.force_rank != 'Grand Master':
        return jsonify({"message": "unauthorized"}), 401
    
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if not temple_query:
        return jsonify({"message": "temple not found"}), 404

    temple_query.is_active = False
    db.session.commit()

    return jsonify({
        "message": "temple deactivated"
    }), 200