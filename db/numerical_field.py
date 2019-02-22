from db import db


class NumericalField(db.Model):
    __tablename__ = 'numerical_fields'

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(120), unique=False, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False)


def get_all():
    query = NumericalField.query.all()
    return list(map(lambda x: {
        "id": x.id,
        "header": x.header,
        "value": x.value,
        "count": x.count
    }, query))
