from datetime import datetime, timezone, timedelta
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy_utils import PhoneNumberType
from webapp import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


appointment_price_table = sa.Table(
    "appointment_price_table",
    db.Model.metadata,
    sa.Column("appointment_id", sa.ForeignKey("appointments.id"),
              primary_key=True),
    sa.Column("price_id", sa.ForeignKey("price_list.id"), primary_key=True)
)

appointment_schedule_table = sa.Table(
    "appointment_schedule_table",
    db.Model.metadata,
    sa.Column("appointment_id", sa.ForeignKey("appointments.id"),
              primary_key=True),
    sa.Column("schedule_id", sa.ForeignKey("schedules.id"),
              primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(40))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50))
    phone: so.Mapped[str] = so.mapped_column(PhoneNumberType())
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    discount: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    role: so.Mapped[str] = so.mapped_column(sa.String(25), default='user')

    reviews: so.WriteOnlyMapped['Review'] = so.relationship(
        back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'''User: {self.id}, first_name: {self.first_name},
         last_name: {self.last_name}, email: {self.email}'''


class Schedule(db.Model):
    __tablename__ = "schedules"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date_time_schedule: so.Mapped[datetime] = so.mapped_column(sa.DateTime,
                                                               unique=True)
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    def __repr__(self):
        return f'Schedule: {self.id}, date: {self.date_time_schedule}'

    @property
    def split_schedule_date(self):
        return self.date_time_schedule.date()

    @property
    def split_schedule_time(self):
        return self.date_time_schedule.time()

    @property
    def format_date(self):
        return self.date_time_schedule.strftime("%d.%m.%Y - %H:%M")

    def get_some_schedule(id):
        return Schedule.query.where(Schedule.id == id)

    def get_nearby_dates(schedule, duration):
        return Schedule.query.filter(
            Schedule.date_time_schedule > schedule,
            Schedule.date_time_schedule < (schedule + timedelta(minutes=duration))
        )


class Price(db.Model):
    __tablename__ = "price_list"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    procedure: so.Mapped[str] = so.mapped_column(sa.String(25))
    description: so.Mapped[str] = so.mapped_column(sa.String)
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    duration: so.Mapped[int] = so.mapped_column(sa.Integer)
    link_photo_by_procedure: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'''Procedure: {self.id}, name: {self.procedure},
         price: {self.price}'''

    def __str__(self) -> str:
        return self.procedure

    @property
    def hour(self):
        return self.duration // 60

    @property
    def minute(self):
        return self.duration % 60

    def get_target_procedures(ids_list):
        return Price.query.filter(Price.id.in_(ids_list))


class Appointment(db.Model):
    __tablename__ = "appointments"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    schedule_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Schedule.id),
                                                   index=True)
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    procedure: so.Mapped[List[Price]] = so.relationship(
        secondary=appointment_price_table)
    schedule: so.Mapped[List[Schedule]] = so.relationship(
        secondary=appointment_schedule_table)

    def __repr__(self):
        return f'Appointment: {self.id}'


class Review(db.Model):
    __tablename__ = "reviews"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(150))
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    author: so.Mapped[User] = so.relationship(back_populates='reviews')

    def __repr__(self):
        return f'Review {self.body}'
