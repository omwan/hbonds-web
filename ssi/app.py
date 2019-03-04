import json
import os

from bokeh.embed import components
from flask import request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from ssi import app
from ssi.db import categorical_field, moe
from ssi.hbonds import count_hbonds, filter_moe


def allowed_file(filename):
    """
    Determine if the uploaded file is of the allowed extension.

    :param filename: name of file to check
    :return: whether or not it is a valid filetype
    """
    allowed_extensions = {'csv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_filters_file():
    """
    Retrieve file with PDB IDs to filter in/out from upload form.

    :return: filepath of file w/ PDB IDs.
    """
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return os.path.join(app.config["UPLOAD_FOLDER"], filename)

    return None


def get_scatter_data_file():
    """
    Retrieve file w/ scatter data from filename in request param, or retrieve
    default scatter data if no request param found/given file name does not exist.

    :return: filename and containing folder for scatter data
    """
    if request.args.get("file") is not None:
        file = request.args.get("file")
        folder = app.config["UPLOAD_FOLDER"]

        if os.path.isfile(os.path.join(folder, file)):
            return file, folder

    return "output.csv", app.config["MOE_FOLDER"]


def silent_remove(filepath):
    """
    Remove the file with the given filepath, do nothing if the file does not exist.

    :param filepath: path to file to remove
    """
    try:
        os.remove(filepath)
    except OSError:
        pass


@app.route("/", methods=["GET", "POST"])
def chart():
    """
    Generate charts and render on index page.

    :return: index w/ charts if applicable
    """
    scatter_div = ""
    scatter_script = ""

    means_div = ""
    means_script = ""

    graph_name = None

    if request.method == "POST":
        file, folder = get_scatter_data_file()

        bucket_size = int(request.form.get("min-bucket-size", default=20))
        filters_filepath = get_filters_file()
        exclude_filters = request.form.get("filter-pdbs") is not None

        scatter_plot, scatter_data = count_hbonds \
            .build_full_scatter(folder, file, filters_filepath, exclude_filters)
        scatter_script, scatter_div = components(scatter_plot)

        means_file = count_hbonds \
            .build_means_output(folder, app.config["UPLOAD_FOLDER"], scatter_data)
        means_plot = count_hbonds.build_means_scatter(means_file, bucket_size)
        means_script, means_div = components(means_plot)

        graph_name = file

        if filters_filepath is not None:
            silent_remove(filters_filepath)

    return render_template("index.html", name=graph_name,
                           scatter_div=scatter_div, scatter_script=scatter_script,
                           means_div=means_div, means_script=means_script)


@app.route("/api/categoricals/<header>")
def get_categorical_fields(header):
    """
    Get most common categorical fields from the given header, limited
    by the given limit in request param.

    :param header: PDB column to retrieve values for, eg: expressionHost
    :return: list of categorical fields + counts sorted by descending count
    """
    limit = request.args.get("limit")
    return jsonify(categorical_field.get_highest_counts(header, limit))


@app.route("/api/categoricals/hetId")
def get_het_ids():
    """
    Get most common het IDs from database. Can also be used for ligand IDs.
    Limited by given limit in request params.

    :return: list of het IDs + counts sorted by descending count
    """
    limit = request.args.get("limit")
    return jsonify(moe.get_het_ids(limit))


@app.route("/api/pdbfilter", methods=["POST"])
def build_scatter_plot_data():
    """
    Build the scatter plot data from the filters in the request body.

    :return: filename of generated scatter plot data file + filter params as map
    """
    filters = json.loads(request.data)
    return jsonify({
        "filename": filter_moe.filter_moe(app.config["UPLOAD_FOLDER"], filters),
        "params": filters
    })


@app.route("/api/filters/<filename>")
def download_scatter_plot_data(filename):
    """
    Download the generated scatter plot data file.

    :param filename: name of generated file
    :return: generated scatter plot file
    """
    folder = app.config["UPLOAD_FOLDER"]
    return send_from_directory(folder, filename, as_attachment=True)


@app.route("/api/filters/<filename>", methods=["DELETE"])
def delete_files(filename):
    """
    Delete all generated files associated with the given scatter plot data file name.

    :param filename: name of file to delete + its associated generated files
    :return: no content response
    """
    folder = app.config["UPLOAD_FOLDER"]
    filepatterns = ["filtered_%s", "means_filtered_%s", "means_%s", "%s"]
    for pattern in filepatterns:
        silent_remove(os.path.join(folder, pattern % filename))

    return '', 204
