from datetime import timedelta
from webapp.models import Price, Schedule


def get_target_procedures(procedure_list):
    return Price.query.filter(Price.id.in_(procedure_list)).all()


def get_sum_duration(procedures):
    return sum([p.duration for p in procedures])


def get_date_id(id):
    return Schedule.query.where(Schedule.id == id).first()


def get_schedule_ids(ids_list):
    return Schedule.query.filter(Schedule.id.in_(ids_list)).all()


def get_nearby_dates(schedule, duration):
    return Schedule.query.filter(
        Schedule.date_time_schedule > schedule,
        Schedule.date_time_schedule < (schedule + timedelta(minutes=duration))
    ).all()
