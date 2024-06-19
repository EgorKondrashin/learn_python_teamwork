from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Text

from db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    password = Column(String)
    created_at = Column(Date)
    email = Column(String)
    discount = Column(Integer)

    def __repr__(self):
        return f'User: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}'


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    status = Column(Boolean, default=True)

    def __repr__(self):
        return f'Schedule: {self.id}, date: {self.date}, time: {self.time}'


class Price(Base):
    __tablename__ = "price_list"

    id = Column(Integer, primary_key=True)
    procedure = Column(String)
    description = Column(Text)
    price = Column(Integer)

    def __repr__(self):
        return f'Procedure: {self.id}, name: {self.procedure}, price: {self.price}'


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    schedule_id = Column(Integer, ForeignKey(Schedule.id), index=True, nullable=False)
    name_procedure = Column(String)
    status = Column(Boolean, default=True)

    def __repr__(self):
        return f'Appointment: {self.id}'


class Photo(Base):
    __tablename__ = "photo_procedure"

    id = Column(Integer, primary_key=True)
    procedure_id = Column(ForeignKey(Price.id), index=True, nullable=False)
    photo = Column(String)

    def __repr__(self):
        return f'Photo: {self.id}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
