import csv
import os
from time import time

moe_headers = ["", "PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source",
               "refinementResolution", "averageBFactor", "chainLength",
               "ligandId", "hetId", "residueCount", "X"]


def get_filename():
    return "filtered_pdbs_%s.csv" % int(time())


def filter_moe(filters):
    moe = open("moe/moe6.csv")
    output = open(os.path.join("moe", get_filename()), "w+")

    col_filters = build_filter(filters)

    with moe, output:
        reader = csv.DictReader(moe)
        writer = csv.DictWriter(output, fieldnames=["PDB"])
        writer.writeheader()

        pdbs = set()

        for i, row in enumerate(reader):
            if i % 500000 == 0:
                print("Reached row %s" % i)

            write_row = False
            for key, value in row.items():
                if (key, value) in col_filters["use"]:
                    write_row = True

            for key, value in row.items():
                if (key, value) in col_filters["ignore"]:
                    write_row = False

            if write_row:
                if row["PDB"] not in pdbs:
                    pdbs.add(row["PDB"])
                    writer.writerow({"PDB": row["PDB"]})
                else:
                    continue

    return output.name


def build_filter(filters):
    final_filter = {
        "use": set(),
        "ignore": set()
    }

    for f in filters:
        if f["filtered"]:
            ignores = final_filter["ignore"]
            ignores.add((f["header"], f["name"]))
            final_filter["ignore"] = ignores
        else:
            used = final_filter["use"]
            used.add((f["header"], f["name"]))
            final_filter["use"] = used

    return final_filter
