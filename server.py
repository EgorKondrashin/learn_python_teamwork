import sqlalchemy as sa
import sqlalchemy.orm as so
from webapp import app, db
from webapp.models import Appointment, Price, User, Schedule, Photo, \
    Review


@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'Appointment': Appointment,
        'Price': Price,
        'User': User,
        'Schedule': Schedule,
        'Photo': Photo,
        'Review': Review
    }
