import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Masters(db.Model):
    __tablename__ = "Masters"

    master_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    species_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Species.species_id"), nullable=False)
    master_name = db.Column(db.String(), nullable=False, unique=True)
    specialization = db.Column(db.String())
    years_training = db.Column(db.Integer())
    max_padawans = db.Column(db.Integer())

    user = db.relationship("Users", back_populates="master")
    species = db.relationship("Species", back_populates="masters")
    courses = db.relationship("Courses", back_populates="instructor", cascade="all, delete-orphan")
    padawans = db.relationship("Padawans", back_populates="master")

    def __init__(self, user_id, species_id, master_name, specialization=None, years_training=None, max_padawans=None):
        self.user_id = user_id
        self.species_id = species_id
        self.master_name = master_name
        self.specialization = specialization
        self.years_training = years_training
        self.max_padawans = max_padawans

    def new_master_object():
        return Masters("", "", "", None, None, None)


class MastersSchema(ma.Schema):
    class Meta:
        fields = ['master_id', 'master_name', 'specialization', 'years_training', 'max_padawans', 'user', 'species', 'courses', 'padawans']

    master_id = ma.fields.UUID()
    master_name = ma.fields.String(required=True)
    specialization = ma.fields.String(allow_none=True)
    years_training = ma.fields.Integer(allow_none=True)
    max_padawans = ma.fields.Integer(allow_none=True)

    user = ma.fields.Nested("UsersSchema", exclude=['master', 'padawan'])
    species = ma.fields.Nested("SpeciesSchema", exclude=['masters', 'padawans'])
    courses = ma.fields.Nested("CoursesSchema", many=True, exclude=['instructor', 'padawans'])
    padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['master', 'user', 'courses', 'species'])


master_schema = MastersSchema()
masters_schema = MastersSchema(many=True)