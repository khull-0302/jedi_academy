from flask import Blueprint
import controllers

padawan = Blueprint('padawan', __name__)

@padawan.route("/padawan", methods=["POST"])
def add_padawan():
    return controllers.add_padawan()

@padawan.route("/padawans", methods=["GET"])
def get_all_padawans():
    return controllers.get_all_padawans()

@padawan.route("/padawans/active", methods=["GET"])
def get_all_active_padawans():
    return controllers.get_all_active_padawans()

@padawan.route("/padawan/<padawan_id>", methods=["PUT"])
def update_padawan_training(padawan_id):
    return controllers.update_padawan_training(padawan_id)

@padawan.route("/padawan/<padawan_id>/promote", methods=["PUT"])
def promote_padawan(padawan_id):
    return controllers.promote_padawan(padawan_id)


@padawan.route("/padawan/<padawan_id>", methods=["DELETE"])
def delete_padawan_by_id(padawan_id):
    return controllers.delete_padawan_by_id(padawan_id)