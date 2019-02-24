from db import db, convert_to_map


class NumericalField(db.Model):
    __tablename__ = 'numerical_fields'

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(120), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False)


def get_all():
    query = NumericalField.query.all()
    return convert_to_map(query)


def get_highest_counts(limit):
    query = NumericalField.query \
        .order_by(NumericalField.count.desc()) \
        .limit(limit) \
        .all()
    return convert_to_map(query)
