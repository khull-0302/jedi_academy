from flask import Blueprint
import controllers

course = Blueprint('course', __name__)

@course.route("/course", methods=["POST"])
def add_course():
    return controllers.add_course()

@course.route("/course/<course_id>", methods=["PUT"])
def update_course(course_id):
    return controllers.update_course(course_id)

@course.route("/course/<course_id>", methods=["DELETE"])
def delete_course_by_id(course_id):
    return controllers.delete_course_by_id(course_id)