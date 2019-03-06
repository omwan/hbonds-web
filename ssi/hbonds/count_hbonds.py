import csv
import os

import numpy as np
import pandas
from bokeh.models import Whisker, ColumnDataSource
from bokeh.plotting import figure


def build_means_output(upload_folder, write_folder, output_file):
    """
    Generate file w/ calculated means, standard deviations, etc. for
    hbond/residue ratio buckets.

    :param upload_folder:   folder to retrieve uploaded file from
    :param write_folder:    folder to write means file to
    :param output_file:     file w/ raw hbond data
    :return: filepath to newly written means file
    """
    means_filepath = os.path.join(write_folder, "means_" + output_file)
    means_file = open(means_filepath, "w+")
    csvfile = open(os.path.join(upload_folder, output_file), encoding="utf-8-sig")

    with csvfile, means_file as out:
        reader = csv.DictReader(csvfile, delimiter=",")

        fieldnames = ["type", "value", "count", "mean", "std"]
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()

        buckets = {}

        for i, row in enumerate(reader):
            if row["resolution"] == "" or float(row["residues"]) <= 50 or float(row["resolution"]) <= 1:
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


def filter_data(data_folder, data_file, pdb_filters_file, exclude_filters):
    """
    Filter scatter plot data on a list of PDB IDs.

    :param data_folder:         folder containing output file
    :param data_file:           name of output file
    :param pdb_filters_file:    file containing PDB IDs to filter in/out
    :param exclude_filters:     whether or not to filter in/out given PDB IDs
    :return: name of filtered file
    """
    d_file = open(os.path.join(data_folder, data_file))
    pdb_filters = pandas.read_csv(os.path.join(data_folder, pdb_filters_file))
    output_filename = os.path.join(data_folder, "filtered_" + data_file)
    output = open(output_filename, "w+")

    with d_file, output:
        reader = csv.DictReader(d_file)
        writer = csv.DictWriter(output, fieldnames=["PDB", "hbonds", "residues",
                                                    "hbonds/residues", "resolution"])
        writer.writeheader()
        pdbs = set(pdb_filters["PDB"])

        for i, row in enumerate(reader):
            if not exclude_filters and row["PDB"] in pdbs:
                writer.writerow(row)

            if exclude_filters and row["PDB"] not in pdbs:
                writer.writerow(row)

    return "filtered_" + data_file


def build_full_scatter(data_folder, data_file, pdb_filters_file, exclude_filters):
    """
    Generate scatter plot from full hbond count data.

    :param data_folder:         folder containing output file
    :param data_file:           name of output file
    :param pdb_filters_file:    path to file w/ PDB IDs to filter in/out
    :param exclude_filters:     whether or not to filter in/out given PDB IDs
    :return: scatter plot and name of file w/ data
    """
    if pdb_filters_file is not None:
        data_file = filter_data(data_folder, data_file, pdb_filters_file, exclude_filters)

    data = pandas.read_csv(os.path.join(data_folder, data_file))

    # filter out peptides and high-res species
    data = data[data["residues"] > 50]
    data = data[data["resolution"] > 1]
    data = data[data["resolution"] < 4]

    x = data["hbonds/residues"]
    y = data["resolution"]

    source = ColumnDataSource(data=dict(
        x=x,
        y=y,
        pdb=data["PDB"]
    ))

    p = figure(x_range=[0, 0.2], tooltips="@pdb", title="Full data scatter")
    p.xaxis.axis_label = "# Hydrogen Bonds / # Residues"
    p.yaxis.axis_label = "Resolution (Angstroms)"
    p.scatter('x', 'y', source=source)

    return p, data_file


def build_means_scatter(data_file, bucket_size):
    """
    Generate scatter plot from hbond means data.

    :param data_file:   path to means file
    :param bucket_size: only display buckets with at least this many values
    :return: scatter plot
    """
    data = pandas.read_csv(data_file)
    data = data[data["count"] > bucket_size]

    x = data["value"]
    y = data["mean"]
    error = data["std"]
    upper = [y_val + e for y_val, e in zip(y, error)]
    lower = [y_val - e for y_val, e in zip(y, error)]

    p = figure(y_range=[1, 4], title="Mean values")
    p.xaxis.axis_label = "# Hydrogen Bonds / # Residues"
    p.yaxis.axis_label = "Resolution (Angstroms)"

    source = ColumnDataSource(data=dict(
        x=x,
        y=y,
        upper=upper,
        lower=lower,
    ))

    p.add_layout(
        Whisker(source=source, base="x", upper="upper",
                lower="lower", level="overlay")
    )

    p.scatter('x', 'y', source=source)

    return p
