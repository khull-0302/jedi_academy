import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.padawan_courses_xref import padawans_courses_association_table



class Species(db.Model):
    __tablename__ = "Species"

    species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    species_name = db.Column(db.String(), nullable=False, unique=True)
    homeworld = db.Column(db.String())
    avg_lifespan = db.Column(db.Integer())
    

    padawans = db.relationship("Padawans", back_populates="species")
    masters = db.relationship("Masters", back_populates="species")
    

    def __init__(self, species_name, homeworld=None, avg_lifespan=None):
        self.species_name = species_name
        self.homeworld = homeworld
        self.avg_lifespan = avg_lifespan

    def new_species_object():
        return Species("", None, None)


class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ['species_id', 'species_name', 'homeworld', 'avg_lifespan', 'masters', 'padawans']

    species_id = ma.fields.UUID()
    species_name = ma.fields.String(required=True)
    homeworld = ma.fields.String(allow_none=True)
    avg_lifespan = ma.fields.Integer(allow_none=True)
   

    masters = ma.fields.Nested("MastersSchema", many=True, exclude=['species', 'padawans', 'user', 'courses'])
    padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['species', 'master', 'user','courses'])


species_schema = SpeciesSchema()
species_schemas = SpeciesSchema(many=True)