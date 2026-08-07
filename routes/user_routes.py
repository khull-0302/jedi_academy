from flask import Blueprint
import controllers

user = Blueprint('user', __name__)

@user.route("/user", methods=["POST"])
def add_user():
    return controllers.add_user()

@user.route("/users", methods=["GET"])
def get_all_users():
    return controllers.get_all_users()

@user.route("/user/profile", methods=["GET"])
def get_user_profile():
    return controllers.get_user_profile()

@user.route("/user/<user_id>", methods=["PUT"])
def update_user_profile(user_id):
    return controllers.update_user_profile(user_id)


@user.route("/user/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    return controllers.delete_user_by_id(user_id)