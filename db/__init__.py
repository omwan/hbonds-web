from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def convert_to_map(query):
    return list(map(lambda x: {
        "id": x.id,
        "header": x.header,
        "value": x.value,
        "count": x.count
    }, query))
