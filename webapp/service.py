from webapp import db
from webapp.models import Price, Schedule, Appointment


def get_sum_duration(procedures):
    return sum([p.duration for p in procedures])


def process_get_procedures_and_schedule(ids_procedure, id_date):
    procedures = Price.get_target_procedures(ids_list=ids_procedure).all()
    sum_duration = get_sum_duration(procedures=procedures)
    target_date = Schedule.get_some_schedule(id=id_date).first()
    nearby_dates = Schedule.get_nearby_dates(
        schedule=target_date.date_time_schedule,
        duration=sum_duration).all()
    return [procedures, target_date, nearby_dates]


def checking_schedule_for_overlap(date, nearby_dates):
    ids_list = [date.id]
    list_schedules = [date]
    for schedule in nearby_dates:
        if not schedule.is_active:
            return
        ids_list.append(schedule.id)
        list_schedules.append(schedule)
    return ids_list, list_schedules


def create_appointment(user_id, schedule_id, schedule, procedure):
    appointment = Appointment(
        user_id=user_id,
        schedule_id=schedule_id,
        schedule=schedule,
        procedure=procedure
    )
    db.session.add(appointment)


def update_schedule_in_db(schedules):
    Schedule.query.where(Schedule.id.in_(schedules)).update({'is_active': False})


def create_appointment_and_update_schedule(user_id, ids_procedure, id_date):
    result = process_get_procedures_and_schedule(ids_procedure=ids_procedure,
                                                 id_date=id_date)

    lists_data = checking_schedule_for_overlap(date=result[1],
                                               nearby_dates=result[2])

    if lists_data is None:
        return

    create_appointment(user_id=user_id,
                       schedule_id=result[1].id,
                       schedule=lists_data[1],
                       procedure=result[0])
    update_schedule_in_db(schedules=lists_data[0])
    db.session.commit()

    return result[1].format_date, result[0]
