import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.padawan_courses_xref import padawans_courses_association_table

class Courses(db.Model):
    __tablename__ = "Courses"

    course_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructor_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"), nullable=False)
    course_name = db.Column(db.String(), nullable=False, unique=True)
    difficulty = db.Column(db.String())
    duration_weeks = db.Column(db.Integer())

    instructor = db.relationship("Masters", back_populates="courses")
    padawans = db.relationship("Padawans", secondary=padawans_courses_association_table, back_populates="courses")

    def __init__(self, instructor_id, course_name, difficulty=None, duration_weeks=None):
        self.instructor_id = instructor_id
        self.course_name = course_name
        self.difficulty = difficulty
        self.duration_weeks = duration_weeks

    def new_course_object():
        return Courses("", "", None, None)


class CoursesSchema(ma.Schema):
    class Meta:
        fields = ['course_id', 'course_name', 'difficulty', 'duration_weeks', 'instructor', 'padawans']

    course_id = ma.fields.UUID()
    course_name = ma.fields.String(required=True)
    difficulty = ma.fields.String(allow_none=True)
    duration_weeks = ma.fields.Integer(allow_none=True)

    instructor = ma.fields.Nested("MastersSchema", exclude=['courses', 'padawans', 'user', 'species'])
    padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['courses', 'user', 'master', 'species'])


course_schema = CoursesSchema()
courses_schema = CoursesSchema(many=True)