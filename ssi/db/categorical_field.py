from ssi.db import db, convert_to_map


class CategoricalField(db.Model):
    __tablename__ = 'categorical_fields'

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(120), unique=False, nullable=False)
    value = db.Column(db.String(1000), unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False)


def get_all():
    query = CategoricalField.query.all()
    return convert_to_map(query)


def get_highest_counts(header, limit=500):
    query = CategoricalField.query\
        .filter_by(header=header) \
        .order_by(CategoricalField.count.desc()) \
        .limit(limit) \
        .all()
    return convert_to_map(query)
