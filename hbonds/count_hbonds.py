import csv
import os

import numpy as np
import pandas
from bokeh.models import Whisker, ColumnDataSource
from bokeh.plotting import figure

moe_dir = "/Users/olivia/Documents/GitHub/hbonds-web/moe"

MOE_HEADERS = ["PDB", "Type", "cb.cb", "sc_.exp_avg", "hb_energy", "Residue.1",
               "Residue.2", "chainId", "expressionHost", "source", "refinementResolution",
               "averageBFactor", "chainLength", "ligandId", "hetId", "residueCount"]


def add_trendline(p):
    """
    TODO
    :param p:
    :return:
    """
    return p


def build_output(upload_folder, filters_file, filter_out):
    """
    Generate file w/ hbond counts filtered from original output file.

    :param upload_folder: folder to write files to
    :param filters_file: list of PDBS to use/filter out
    :param filter_out: whether or not to use/filter out input PDBs
    :return: filepath to newly created file
    """
    pdbs = []

    filters = open(os.path.join(upload_folder, filters_file), encoding='utf-8-sig')

    with filters:
        reader = csv.DictReader(filters)
        for i, row in enumerate(reader):
            pdbs.append(row["PDB"])

    moe = open(os.path.join(moe_dir, "output.csv"))
    output_filepath = os.path.join(upload_folder, "output_" + filters_file)
    output = open(output_filepath, "w+")

    with moe, output:
        reader = csv.DictReader(moe)

        output_headers = ["PDB", "hbonds", "residues", "hbonds/residues", "resolution"]
        writer = csv.DictWriter(output, fieldnames=output_headers)
        writer.writeheader()

        for row in reader:
            if filter_out and row["PDB"] in pdbs:
                continue
            elif not filter_out and row["PDB"] not in pdbs:
                continue
            else:
                writer.writerow(row)

    return output_filepath


def build_means_output(upload_folder, output_file):
    """
    Generate file w/ calculated means, standard deviations, etc. for
    hbond/residue ratio buckets.

    :param upload_folder: folder to write files to
    :param output_file: file w/ raw hbond data
    :return: filepath to newly written means file
    """
    output_file_name = output_file.rsplit("/", 1)[1]
    means_filepath = os.path.join(upload_folder, "means_" + output_file_name)
    means_file = open(means_filepath, "w+")
    csvfile = open(output_file, encoding="utf-8-sig")

    with csvfile, means_file as out:
        reader = csv.DictReader(csvfile, delimiter=",")

        fieldnames = ["type", "value", "count", "mean", "std"]
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()

        buckets = {}

        for i, row in enumerate(reader):
            if float(row["residues"]) <= 50 or float(row["resolution"]) <= 1:
                continue

            headers = {
                "hbond_residue": round(float(row["hbonds/residues"]), 3),
            }

            resolution = float(row["resolution"])

            for key, value in headers.items():
                pair = (key, float(value))
                if pair in buckets:
                    resolutions = buckets[pair]
                    resolutions.append(resolution)
                    buckets[pair] = resolutions
                else:
                    buckets[pair] = [resolution]

        for key in sorted(buckets.keys()):
            writer.writerow({
                "type": key[0],
                "value": key[1],
                "count": len(buckets[key]),
                "mean": np.average(buckets[key]),
                "std": np.std(buckets[key])
            })

    return means_filepath


def build_full_scatter(filters_file=None):
    """
    Generate scatter plot from full hbond count data.

    :param filters_file: path to output file
    :return: scatter plot
    """
    if filters_file is None:
        data_file = os.path.join(moe_dir, "output.csv")
    else:
        data_file = filters_file

    data = pandas.read_csv(data_file)

    # filter out peptides and high-res species
    data = data[data["residues"] > 50]
    data = data[data["resolution"] > 1]

    x = data["hbonds/residues"]
    y = data["resolution"]

    p = figure()
    p.scatter(x, y)

    return p


def build_means_scatter(data_file):
    """
    Generate scatter plot from hbond means data.

    :param data_file: path to means file
    :return: scatter plot
    """
    data = pandas.read_csv(data_file)
    data = data[data["count"] > 20]

    x = data["value"]
    y = data["mean"]
    error = data["std"]
    upper = [y_val + e for y_val, e in zip(y, error)]
    lower = [y_val - e for y_val, e in zip(y, error)]

    p = figure(y_range=[1, 4])
    p.scatter(x, y)

    source = ColumnDataSource(data=dict(x=x, y=y, upper=upper, lower=lower))

    p.add_layout(
        Whisker(source=source, base="x", upper="upper", lower="lower", level="overlay")
    )

    return p
