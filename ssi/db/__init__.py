from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def convert_to_map(query, mapping_function):
    """
    Convert query result to list of map objects.

    :param query:               query result
    :param mapping_function:    function to build map from query object
    :return: list of maps representing query data
    """
    return list(map(mapping_function, query))
