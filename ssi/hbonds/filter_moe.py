import csv
import os
from time import time

from ssi.db import moe

moe_headers = ["", "PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source",
               "refinementResolution", "averageBFactor", "chainLength",
               "ligandId", "hetId", "residueCount", "X"]


def add_quotes(string, quotation):
    """
    Helper to prepend + append quotations to a string.

    :param string:      string to add quotes to
    :param quotation:   type of quotation, eg: " or '
    :return: string with quote characters added
    """
    return quotation + string + quotation


def categorical_operator(f):
    """
    Get string SQL equivalent of equals/not equals from a boolean.

    :param f: boolean value
    :return: string equivalent of boolean
    """
    if f["filtered"]:
        return "!="
    else:
        return "="


def build_filter_string(f, or_clause):
    """
    Build portion of SQL where clause for the given filter.

    :param f: filter object to build where clause section from
    :return: SQL string
    """
    header = add_quotes(f["header"], "\"")
    operator = f.get("comparator", categorical_operator(f))
    value = add_quotes(f["name"], "'") if "name" in f else str(f["comparedValue"])
    bool = f.get("bool", "")
    strings = [header, operator, value, bool]

    if not or_clause and bool == "or":
        strings = ["("] + strings
        or_clause = True
    elif or_clause and bool == "and":
        strings.insert(len(strings) - 1, ")")
        or_clause = False

    return " ".join(strings), or_clause


def build_residue_filter_string(f, or_clause):
    """
    Build SQL where clause for residue types to get matching substrings.

    :param f: filter object with residue type to filter on.
    :return: SQL string
    """
    query_string = """
    (substring("Residue.1", 6, 3) = '{0}' 
    OR substring("Residue.2", 6, 3) = '{0}')
    """
    bool = f.get("bool", "")
    strings = [query_string.format(f["name"]), bool]

    if not or_clause and bool == "or":
        strings = ["("] + strings
        or_clause = True
    elif or_clause and bool == "and":
        strings.insert(len(strings) - 1, ")")
        or_clause = False

    return " ".join(strings), or_clause


def strip_trailing_bool(filter_string):
    """
    Strip trailing and/or from SQL where clause string if present.
    :param filter_string: SQL where clause string
    :return: SQL where clause string with trailing boolean stripped, if necessary
    """
    string, last_word = filter_string.rsplit(" ", 1)
    if last_word == "and" or last_word == "or":
        return string
    else:
        return filter_string


def write_output(upload_folder, result):
    """
    Write SQL query result to a CSV file.

    :param upload_folder:   location to write file to
    :param result:          SQL query result
    :return: name of generated file
    """
    filename = "filtered_pdbs_%s.csv" % int(time())
    output = open(os.path.join(upload_folder, filename), "w+")

    with output:
        output_headers = ["PDB", "hbonds", "residues", "hbonds/residues", "resolution"]
        writer = csv.DictWriter(output, fieldnames=output_headers)
        writer.writeheader()

        row_count = 0
        for row in result:
            writer.writerow(dict(row))
            row_count += 1

    return filename, row_count


def filter_moe(upload_folder, filters):
    """
    Build SQL where clause from filters + make SQL query to generate scatter plot data file.

    :param upload_folder: location to write output file to
    :param filters: list of filter objects to generate query from
    :return: name of scatter plot file
    """
    filter_strings = []
    count_residues = False

    or_clause = False
    for f in filters:
        if f["header"] == "residue":
            count_residues = True
            string, or_clause = build_residue_filter_string(f, or_clause)
            filter_strings.append(string)
        else:
            string, or_clause = build_filter_string(f, or_clause)
            filter_strings.append(string)

    final_string = strip_trailing_bool(" ".join(filter_strings))

    if not count_residues:
        result = moe.get_data_from_filters(final_string)
    else:
        result = moe.get_residue_data_from_filters(final_string)

    filename, row_count = write_output(upload_folder, result)
    return filename, row_count, final_string
