import flask
from flask import request, jsonify
from data import db_session
from data.events import Event

blueprint = flask.Blueprint("events_api", __name__, template_folder="templates")


@blueprint.route("/api/events")
def get_events():
    db_sess = db_session.create_session()
    events = db_sess.query(Event).all()
    return jsonify(
        {
            "events": [
                item.to_dict()
                for item in events
            ]
        }
    )


@blueprint.route("/api/events/<int:event_id>", methods=["GET"])
def get_one_place(event_id):
    db_sess = db_session.create_session()
    events = db_sess.query(Event).get(event_id)
    if not events:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "places": events.to_dict()
        }
    )


@blueprint.route("/api/places", methods=["POST"])
def add_event():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(
            key in request.json
            for key in ["name", "description", "created_datetime", "place_id", "required_age", "notes"]
    ):
        return jsonify({"error": "Bad request"})
    db_sess = db_session.create_session()
    event = Event(
        id=request.json["id"],
        name=request.json["name"],
        address=request.json["description"],
        about=request.json["created_datetime"],
        created_datetime=request.json["place_id"],
        place_id=request.json["place_id"],
        required_age=request.json["required_age"],
        notes=request.json["notes"]
    )
    if db_sess.query(Event).filter(Event.id == event.id).first():
        return jsonify({"error": "Id already exists"})
    db_sess.add(event)
    db_sess.commit()
    return jsonify({"success": "OK"})
