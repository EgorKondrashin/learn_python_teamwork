from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy_utils import PhoneNumberType
from webapp import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    user = db.session.get(User, int(id))
    if user is None:
        admin = db.session.get(Admin, int(id))
        return admin
    return user


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

    reviews: so.WriteOnlyMapped['Review'] = so.relationship(
        back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'''User: {self.id}, first_name: {self.first_name},
         last_name: {self.last_name}, email: {self.email}'''


class Schedule(db.Model):
    __tablename__ = "schedules"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date_time_shedule: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    def __repr__(self):
        return f'Schedule: {self.id}, date: {self.date_time_shedule}'


class Price(db.Model):
    __tablename__ = "price_list"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    procedure: so.Mapped[str] = so.mapped_column(sa.String(25))
    description: so.Mapped[str] = so.mapped_column(sa.String(150))
    price: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return f'''Procedure: {self.id}, name: {self.procedure},
         price: {self.price}'''


class Appointment(db.Model):
    __tablename__ = "appointments"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    schedule_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Schedule.id),
                                                   index=True)
    name_procedure: so.Mapped[str] = so.mapped_column(sa.String(120))
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)

    def __repr__(self):
        return f'Appointment: {self.id}'


class Photo(db.Model):
    __tablename__ = "photo_procedure"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    procedure_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Price.id),
                                                    index=True)
    link_photo_by_procedure: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'Photo: {self.id}'


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


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
