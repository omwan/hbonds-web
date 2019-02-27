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


def filter_moe(upload_folder, filters):
    filter_string = []
    for f in filters:
        header = add_quotes(f["header"], "\"")
        operator = f.get("comparator", "=")
        value = add_quotes(f["name"], "'") if "name" in f else f["comparedValue"]
        bool = f.get("bool", "")

        filter_string.append(" ".join([header, operator, value, bool]))

    result = moe.get_pdbs_by_filters(" ".join(filter_string))

    filename = "filtered_pdbs_%s.csv" % int(time())
    output = open(os.path.join(upload_folder, filename), "w+")

    with output:
        output_headers = ["PDB", "hbonds", "residues", "hbonds/residues", "resolution"]
        writer = csv.DictWriter(output, fieldnames=output_headers)
        writer.writeheader()
        for row in result:
            writer.writerow(dict(row))

    return filename
