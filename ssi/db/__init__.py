from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def convert_to_map(query, mapping_function):
    return list(map(mapping_function, query))
