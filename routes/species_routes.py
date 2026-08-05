from flask import Blueprint
import controllers

species = Blueprint('species', __name__)

@species.route("/species", methods=["POST"])
def add_species():
    return controllers.add_species()

@species.route("/all/species", methods=["GET"])
def get_all_species():
    return controllers.get_all_species()

@species.route("/species/<species_id>", methods=["GET"])
def get_species_by_id(species_id):
    return controllers.get_species_by_id(species_id)