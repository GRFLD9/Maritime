from datetime import datetime, date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from exceptions import ValidationError
from forms.booking_form import BookingForm
from services.booking_service import BookingService
from services.room_service import RoomService

DATE_FORMAT = "%d.%m.%Y"

booking_blueprint = Blueprint("booking", __name__, template_folder="templates")


@booking_blueprint.route("/book/<int:room_id>", methods=["GET", "POST"])
def book_room(room_id):
    form = BookingForm(current_user=current_user)
    today = date.today()

    room = RoomService.get_room_by_id(room_id)
    if not room:
        flash("Комната не найдена.", "danger")
        return redirect(url_for("room.room_list"))

    check_in_str = request.args.get("check_in")
    check_out_str = request.args.get("check_out")
    guests = request.args.get("guests", type=int)

    check_in = datetime.strptime(check_in_str, DATE_FORMAT).date() if check_in_str else None
    check_out = datetime.strptime(check_out_str, DATE_FORMAT).date() if check_out_str else None

    if request.method == "GET":
        if check_in:
            form.check_in.data = check_in
        if check_out:
            form.check_out.data = check_out
        if guests:
            form.guests.data = guests

    form = BookingForm()

    if form.validate_on_submit():
        if not form.validate(user_authenticated=current_user.is_authenticated):
            flash("Проверьте введённые данные", "danger")
        else:
            data = {
                "room_id": room_id,
                "check_in": form.check_in.data,
                "check_out": form.check_out.data,
                "guests": form.guests.data,
                "notes": form.notes.data,
                "user_id": current_user.id if current_user.is_authenticated else None,
            }

            if not current_user.is_authenticated:
                data.update({
                    "guest_name": form.guest_name.data,
                    "guest_phone": form.guest_phone.data,
                    "guest_email": form.guest_email.data,
                })

            try:
                BookingService.create_booking(data)
                flash("Бронирование успешно!", "success")
                return redirect(url_for("room.room_list"))
            except ValidationError as e:
                flash(str(e), "danger")

    return render_template(
        "bookings/book.html",
        form=form,
        room=room,
        today=today.strftime(DATE_FORMAT),
        check_in=check_in,
        check_out=check_out
    )


@booking_blueprint.route("/bookings")
@login_required
def user_bookings():
    bookings = BookingService.get_user_bookings(current_user.id)
    return render_template("bookings/list.html", bookings=bookings)
