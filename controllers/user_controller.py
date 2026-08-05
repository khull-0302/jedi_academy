from flask import jsonify, request
from flask_bcrypt import generate_password_hash


from db import db
from models.user import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth

def add_user():
    post_data = request.form if request.form else request.get_json()

    new_user = Users.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"{e}: unable to create record"}), 400

    return jsonify({"message": "user created", "result": user_schema.dump(new_user)}), 201


@authenticate_return_auth
def get_all_users(auth_info):
    if auth_info.user.force_rank not in ['Council Member', 'Grand Master']:
            return jsonify({"message": "unauthorized"}), 401
    users_query = db.session.query(Users).all()
    return jsonify({"message": "users found", "results": users_schema.dump(users_query)}), 200


@authenticate_return_auth
def update_user_profile(user_id, auth_info):
    if auth_info.user.force_rank not in ['Council Member', 'Grand Master'] and auth_info.user.user_id != user_id:
        return jsonify({"message": "unauthorized"}), 401
    
    post_data = request.form if request.form else request.json

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        populate_object(user_query, post_data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400
        
        return jsonify({"message": "user updated", "result": user_schema.dump(user_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    if auth_info.user.force_rank != 'Grand Master': 
            return jsonify({"message": "unauthorized"}), 401
    
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(user_query)
    db.session.commit()

    return jsonify({
        "message": "user deleted"
    }), 200
     