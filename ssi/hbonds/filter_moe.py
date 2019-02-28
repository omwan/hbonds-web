import csv
import os
from time import time

from ssi.db import moe

moe_headers = ["", "PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source",
               "refinementResolution", "averageBFactor", "chainLength",
               "ligandId", "hetId", "residueCount", "X"]


def add_quotes(string, quotation):
    return quotation + string + quotation


def categorical_operator(f):
    if f["filtered"]:
        return "!="
    else:
        return "="


def build_filter_string(f):
    header = add_quotes(f["header"], "\"")
    operator = f.get("comparator", categorical_operator(f))
    value = add_quotes(f["name"], "'") if "name" in f else f["comparedValue"]
    bool = f.get("bool", "")

    return " ".join([header, operator, value, bool])


def build_residue_filter_string(f):
    query_string = """
    (substring("Residue.1", 6, 3) = '{0}' 
    OR substring("Residue.2", 6, 3) = '{0}')
    """
    bool = f.get("bool", "")

    return " ".join([query_string.format(f["name"]), bool])


def strip_trailing_bool(filter_string):
    string, last_word = filter_string.rsplit(" ", 1)
    if last_word == "and" or last_word == "or":
        return string
    else:
        return filter_string


def filter_moe(upload_folder, filters):
    filter_strings = []
    count_residues = False

    for f in filters:
        if f["header"] == "residue":
            count_residues = True
            filter_strings.append(build_residue_filter_string(f))
        else:
            filter_strings.append(build_filter_string(f))

    final_string = strip_trailing_bool(" ".join(filter_strings))

    if not count_residues:
        result = moe.get_data_from_filters(final_string)
    else:
        result = moe.get_residue_data_from_filters(final_string)

    filename = "filtered_pdbs_%s.csv" % int(time())
    output = open(os.path.join(upload_folder, filename), "w+")

    with output:
        output_headers = ["PDB", "hbonds", "residues", "hbonds/residues", "resolution"]
        writer = csv.DictWriter(output, fieldnames=output_headers)
        writer.writeheader()
        for row in result:
            writer.writerow(dict(row))

    return filename
