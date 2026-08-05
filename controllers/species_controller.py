from flask import jsonify, request


from db import db
from models.species import Species, species_schema, species_schemas
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate

@authenticate_return_auth
def add_species(auth_info):
    if auth_info.user.force_rank not in ['Master', 'Grand Master']:
        return jsonify({"message": "unauthorized"}), 401

    post_data = request.form if request.form else request.get_json()

    new_species = Species.new_species_object()

    populate_object(new_species, post_data)

    try:
        db.session.add(new_species)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({
        "message": "species created",
        "result": species_schema.dump(new_species)
    }), 201


@authenticate
def get_all_species():
    species_query = db.session.query(Species).all()
    return jsonify({"message": "species found", "results": species_schemas.dump(species_query)}), 200



@authenticate
def get_species_by_id(species_id):
    
    species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

    return jsonify ({
        "message": "species found",
        "results": species_schema.dump(species_query)
    }),200


