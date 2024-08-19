from webapp import db
from webapp.models import Price, Schedule, Appointment


def get_sum_duration(procedures):
    return sum([p.duration for p in procedures])


def process_get_schedule(duration, id_date):
    target_date = Schedule.get_some_schedule(id=id_date).first()
    nearby_dates = Schedule.get_nearby_dates(
        schedule=target_date.date_time_schedule,
        duration=duration).all()
    for schedule in nearby_dates:
        if not schedule.is_active:
            return
    return nearby_dates


def create_appointment(user_id, schedule, procedure):
    appointment = Appointment(
        user_id=user_id,
        schedule=schedule,
        procedure=procedure
    )
    db.session.add(appointment)


def reservation_schedule(schedules):
    Schedule.query.where(Schedule.id.in_(schedules)).update({'is_active': False})


def create_appointment_and_reservation_schedule(user_id, ids_procedure, id_date):
    procedures = Price.get_target_procedures(ids_list=ids_procedure).all()
    sum_duration = get_sum_duration(procedures=procedures)
    result = process_get_schedule(duration=sum_duration,
                                  id_date=id_date)

    if result is None:
        return

    create_appointment(user_id=user_id,
                       schedule=result,
                       procedure=procedures)
    reservation_schedule(schedules=[date.id for date in result])
    db.session.commit()

    return result[0].format_date, procedures
