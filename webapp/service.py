from webapp import db
from webapp.models import Price, Schedule, Appointment


def get_sum_duration(procedures):
    return sum([p.duration for p in procedures])


def process_get_data(ids_procedure, id_date):
    procedures = Price.get_target_procedures(ids_list=ids_procedure).all()
    sum_duration = get_sum_duration(procedures=procedures)
    target_date = Schedule.get_some_schedule(id=id_date).first()
    nearby_dates = Schedule.get_nearby_dates(
        schedule=target_date.date_time_schedule,
        duration=sum_duration).all()
    return procedures, target_date, nearby_dates


def checking_data_for_overlap(id_date, nearby_dates):
    ids_list = [id_date]
    for date_time in nearby_dates:
        if not date_time.is_active:
            return
        ids_list.append(date_time.id)
    list_schedules = Schedule.get_target_schedules(ids_list).all()
    return ids_list, list_schedules


def adding_data_into_db(user_id, schedule_id, schedule, procedure):
    appointment = Appointment(
        user_id=user_id,
        schedule_id=schedule_id,
        schedule=schedule,
        procedure=procedure
    )
    db.session.add(appointment)
    db.session.commit()


def update_schedule_in_db(schedules):
    Schedule.query.where(Schedule.id.in_(schedules)).update({'is_active': False})
    db.session.commit()


def process_data(user_id, ids_procedure, id_date):
    procedures, date, nearby_dates = process_get_data(ids_procedure=ids_procedure,
                                                      id_date=id_date)

    lists_data = checking_data_for_overlap(id_date=date.id, nearby_dates=nearby_dates)

    if lists_data is None:
        return

    adding_data_into_db(user_id=user_id,
                        schedule_id=date.id,
                        schedule=lists_data[1],
                        procedure=procedures)
    update_schedule_in_db(schedules=lists_data[0])

    return date.format_date, procedures
