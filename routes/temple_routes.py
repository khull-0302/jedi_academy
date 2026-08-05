from flask import Blueprint
import controllers

temple = Blueprint('temple', __name__)

@temple.route("/temple", methods=["POST"])
def add_temple():
    return controllers.add_temple()


@temple.route("/temples", methods=["GET"])
def get_all_temples():
    return controllers.get_all_temples()

@temple.route("/temple/<temple_id>", methods=["GET"])
def get_temple_by_id(temple_id):
    return controllers.get_temple_by_id(temple_id)

@temple.route("/temple/<temple_id>", methods=["PUT"])
def update_temple_by_id(temple_id):
    return controllers.update_temple_by_id(temple_id)


@temple.route("/temple/<temple_id>", methods=["DELETE"])
def deactivate_temple_by_id(temple_id):
    return controllers.deactivate_temple_by_id(temple_id)