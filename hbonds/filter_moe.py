import csv
import os
from time import time

moe_headers = ["PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source",
               "refinementResolution", "averageBFactor", "chainLength",
               "ligandId", "hetId", "residueCount"]


def get_filename():
    return "filtered_moe_%s.csv" % int(time())


def filter_moe(filters):
    moe = open("moe/moe6.csv")
    output = open(os.path.join("moe", get_filename()), "w+")

    source = filters["source"]["name"]
    filter_source = filters["source"]["filtered"]

    with moe, output:
        reader = csv.DictReader(moe)
        writer = csv.DictWriter(output, fieldnames=moe_headers)
        writer.writeheader()

        for i, row in enumerate(reader):
            if i % 500000 == 0:
                print("Reached row %s" % i)

            if row["source"] == source:
                if filter_source:
                    continue
                else:
                    writer.writerow(row)

    return output.name
