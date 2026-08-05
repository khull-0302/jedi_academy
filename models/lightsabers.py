import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Lightsabers(db.Model):
    __tablename__ = "Lightsabers"

    saber_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    saber_name = db.Column(db.String(), nullable=False, unique=True)
    blade_color = db.Column(db.String(), nullable=False)

    owner = db.relationship("Users", back_populates="lightsaber")

    def __init__(self, owner_id, saber_name, blade_color):
        self.owner_id = owner_id
        self.saber_name = saber_name
        self.blade_color = blade_color

    def new_lightsaber_object():
        return Lightsabers("", "", "")


class LightsabersSchema(ma.Schema):
    class Meta:
        fields = ['saber_id', 'saber_name', 'blade_color', 'owner']

    saber_id = ma.fields.UUID()
    saber_name = ma.fields.String(required=True)
    blade_color = ma.fields.String(required=True)

    owner = ma.fields.Nested("UsersSchema", exclude=['lightsaber'])


lightsaber_schema = LightsabersSchema()
lightsabers_schema = LightsabersSchema(many=True)