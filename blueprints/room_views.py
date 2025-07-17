from flask import Blueprint, render_template, request
from services.room_service import RoomService

room_blueprint = Blueprint("room", __name__, template_folder="../templates/rooms")

@room_blueprint.route("/rooms")
def room_list():
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    guests = request.args.get("guests", type=int)

    rooms = RoomService.get_available_rooms(check_in, check_out, guests)

    return render_template(
        "rooms/list.html",
        rooms=rooms,
        check_in=check_in,
        check_out=check_out,
        guests=guests
    )


@room_blueprint.route("/rooms/modal/<int:room_id>")
def room_modal(room_id):
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    guests = request.args.get("guests")

    room = RoomService.get_room_by_id(room_id)
    available_rooms = RoomService.get_available_rooms(check_in, check_out, guests)
    is_available = any(r.id == room.id for r in available_rooms)

    return render_template(
        "rooms/_room_modal.html",
        room=room,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        is_available=is_available
    )