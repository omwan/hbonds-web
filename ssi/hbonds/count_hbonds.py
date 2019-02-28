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

    :param upload_folder: folder to write files to
    :param output_file: file w/ raw hbond data
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


def build_full_scatter(filters_file):
    """
    Generate scatter plot from full hbond count data.

    :param filters_file: path to output file
    :return: scatter plot
    """
    data = pandas.read_csv(filters_file)

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

    p = figure(tooltips="@pdb", title="Full data scatter")
    p.xaxis.axis_label = "# Hydrogen Bonds / # Residues"
    p.yaxis.axis_label = "Resolution (Angstroms)"
    p.scatter('x', 'y', source=source)

    return p


def build_means_scatter(data_file, bucket_size):
    """
    Generate scatter plot from hbond means data.

    :param data_file: path to means file
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
    # p.scatter(x, y)

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
