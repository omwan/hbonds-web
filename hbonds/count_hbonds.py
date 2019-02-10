import csv
import os

import pandas
from bokeh.plotting import figure

moe_dir = "/Users/olivia/Documents/GitHub/hbonds-web/moe"

MOE_HEADERS = ["PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source", "refinementResolution",
               "averageBFactor", "chainLength", "ligandId", "hetId", "residueCount"]


def build_graph(filters_file=None):
    if filters_file is None:
        data_file = os.path.join(moe_dir, "output.csv")
    else:
        data_file = filters_file

    data = pandas.read_csv(data_file)

    # filter out peptides and high-res species
    filtered_data = data[data["hbonds"] > 50]
    filtered_data = filtered_data[data["resolution"] > 1]

    x = filtered_data["hbonds/residues"]
    y = filtered_data["resolution"]

    p = figure()
    p.scatter(x, y)

    return p


def build_output(upload_folder, filters_file, filter_out):
    pdbs = []

    filters = open(os.path.join(upload_folder, filters_file), encoding='utf-8-sig')
    with filters:
        reader = csv.DictReader(filters)
        for i, row in enumerate(reader):
            pdbs.append(row["PDB"])

    moe = open(os.path.join(moe_dir, "output.csv"))
    output = open(os.path.join(upload_folder, "output_" + filters_file), "w+")

    with moe, output:
        reader = csv.DictReader(moe)

        output_headers = ["PDB", "hbonds", "residues", "hbonds/residues", "resolution"]
        writer = csv.DictWriter(output, fieldnames=output_headers)
        writer.writeheader()

        for i, row in enumerate(reader):
            if i % 500000 == 0:
                print("Reached row %s" % i)

            if filter_out:
                if row["PDB"] in pdbs:
                    continue
            else:
                if row["PDB"] not in pdbs:
                    continue

            writer.writerow(row)

    return os.path.join(upload_folder, "output_" + filters_file)
