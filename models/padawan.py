import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.padawan_courses_xref import padawans_courses_association_table



class Padawans(db.Model):
    __tablename__ = "Padawans"

    padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    master_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    species_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Species.species_id"), nullable=False)
    padawans_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer())
    training_level = db.Column(db.Integer())
    graduation_date = db.Column(db.DateTime())

    user = db.relationship("Users", back_populates="padawan")
    master = db.relationship("Masters", back_populates="padawans")
    species = db.relationship("Species", back_populates="padawans")
    courses = db.relationship("Courses", secondary=padawans_courses_association_table, back_populates="padawans")

    def __init__(self, master_id, user_id, species_id, padawans_name, age=None, training_level=None, graduation_date=None):
        self.master_id = master_id
        self.user_id = user_id
        self.species_id = species_id
        self.padawans_name = padawans_name
        self.age = age
        self.training_level= training_level
        self.graduation_date = graduation_date

    def new_padawan_object():
        return Padawans("", "", "", "", None, None, None)


class PadawansSchema(ma.Schema):
    class Meta:
        fields = ['padawan_id', 'padawans_name', 'age', 'training_level', 'graduation_date', 'master', 'user', 'species', 'courses']

    padawan_id = ma.fields.UUID()
    padawans_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    training_level = ma.fields.Integer(allow_none=True)
    graduation_date = ma.fields.DateTime(allow_none=True)

    master = ma.fields.Nested("MastersSchema", exclude=['padawans'])
    user = ma.fields.Nested("UsersSchema", exclude=['padawan'])
    species = ma.fields.Nested("SpeciesSchema", exclude=['padawans'])
    courses = ma.fields.Nested("CoursesSchema", many=True, exclude=['padawans'])


padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)