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


def get_file():
    """
    Retrieve a file from the request object.
    """
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return app.config["UPLOAD_FOLDER"], filename
    else:
        return app.config["MOE_FOLDER"], "output.csv"


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
        bucket_size = int(request.form.get("min-bucket-size", default=20))
        folder, file = get_file()

        scatter_plot = count_hbonds.build_full_scatter(os.path.join(folder, file))
        scatter_script, scatter_div = components(scatter_plot)

        means_file = count_hbonds.build_means_output(folder, app.config["UPLOAD_FOLDER"], file)
        means_plot = count_hbonds.build_means_scatter(means_file, bucket_size)
        means_script, means_div = components(means_plot)

        graph_name = file.split(".csv")[0]

        # TODO: decide how/when to implement this
        # if folder == app.config["UPLOAD_FOLDER"]:
        #     os.remove(os.path.join(folder, file))
        # os.remove(means_file)

    return render_template("index.html", name=graph_name,
                           scatter_div=scatter_div, scatter_script=scatter_script,
                           means_div=means_div, means_script=means_script)


@app.route("/api/categoricals/<header>")
def get_categorical_fields(header):
    limit = request.args.get("limit")
    return jsonify(categorical_field.get_highest_counts(header, limit))


@app.route("/api/categoricals/hetId")
def get_het_ids():
    limit = request.args.get("limit")
    return jsonify(moe.get_het_ids(limit))


@app.route("/api/pdbfilter", methods=["POST"])
def build_new_moe():
    filters = json.loads(request.data)
    return jsonify({
        "filename": filter_moe.filter_moe(app.config["UPLOAD_FOLDER"], filters),
        "params": filters
    })


@app.route("/api/filters/<filename>")
def download_filter(filename):
    folder = app.config["UPLOAD_FOLDER"]
    return send_from_directory(folder, filename, as_attachment=True)
