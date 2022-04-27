import flask
from flask import request, jsonify
from data import db_session
from data.places import Place

blueprint = flask.Blueprint("places_api", __name__, template_folder="templates")


@blueprint.route("/api/places")
def get_places():
    db_sess = db_session.create_session()
    places = db_sess.query(Place).all()
    return jsonify(
        {
            "places": [
                item.to_dict(
                    only=(
                        "id",
                        "name",
                        "address",
                        "about",
                        "created_datetime"
                    )
                )
                for item in places
            ]
        }
    )


@blueprint.route("/api/places/<int:place_id>", methods=["GET"])
def get_one_place(place_id):
    db_sess = db_session.create_session()
    places = db_sess.query(Place).get(place_id)
    if not places:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "places": places.to_dict(
                only=(
                    "id",
                    "name",
                    "address",
                    "about",
                    "created_datetime"
                )
            )
        }
    )


@blueprint.route("/api/places", methods=["POST"])
def add_place():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(
            key in request.json
            for key in ["name", "address", "about", "created_datetime"]
    ):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    place = Place(
        id=request.json["id"],
        name=request.json["name"],
        address=request.json["address"],
        about=request.json["about"],
        created_datetime=request.json["created_datetime"]
    )
    if db_sess.query(Place).filter(Place.id == place.id).first():
        return jsonify({"error": "Id already exists"})
    db_sess.add(place)
    db_sess.commit()
    return jsonify({"success": "OK"})
