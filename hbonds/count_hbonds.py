import csv

import pandas
from bokeh.plotting import figure
import os

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
    current_hbond = []

    filters = open(os.path.join(upload_folder, filters_file), encoding='utf-8-sig')
    with filters:
        reader = csv.DictReader(filters)
        for i, row in enumerate(reader):
            pdbs.append(row["PDB"])

    new_row = {
        "PDB": pdbs[0],
        "hbonds": 0
    }

    moe = open(os.path.join(moe_dir, "moe6.csv"))
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

            if row["refinementResolution"] == "NA" or \
                    float(row["refinementResolution"]) > 4 or \
                    float(row["chainLength"]) == 0:
                continue

            if row["PDB"] == new_row["PDB"]:
                if [row["Residue.1"], row["Residue.2"]] == current_hbond:
                    continue
                else:
                    current_hbond = [row["Residue.1"], row["Residue.2"]]
                    new_row["hbonds"] = new_row["hbonds"] + 1
                    if "residues" not in new_row:
                        new_row["residues"] = row["residueCount"]
                    if "resolution" not in new_row:
                        new_row["resolution"] = row["refinementResolution"]
            else:
                if "residues" in new_row and "resolution" in new_row:
                    hbonds = float(new_row["hbonds"])
                    residues = float(new_row["residues"])
                    new_row["hbonds/residues"] = hbonds / residues
                    writer.writerow(new_row)

                new_row = {
                    "PDB": row["PDB"],
                    "hbonds": 1
                }

    return os.path.join(upload_folder, "output_" + filters_file)
