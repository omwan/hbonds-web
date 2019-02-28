import json
import os

from bokeh.embed import components
from flask import request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from ssi import app
from ssi.db import numerical_field, categorical_field, moe
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
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return app.config["UPLOAD_FOLDER"], filename


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

        scatter_plot = count_hbonds.build_full_scatter(os.path.join(app.config["UPLOAD_FOLDER"], file))
        scatter_script, scatter_div = components(scatter_plot)

        means_file = count_hbonds.build_means_output(folder, file)
        means_plot = count_hbonds.build_means_scatter(means_file, bucket_size)
        means_script, means_div = components(means_plot)

        graph_name = file.split(".csv")[0]

    return render_template("index.html", name=graph_name,
                           scatter_div=scatter_div, scatter_script=scatter_script,
                           means_div=means_div, means_script=means_script)


@app.route("/api/numericals/<header>")
def get_numerical_fields(header):
    limit = request.args.get("limit")
    return jsonify(numerical_field.get_highest_counts(limit))


@app.route("/api/categoricals/<header>")
def get_categorical_fields(header):
    limit = request.args.get("limit")
    return jsonify(categorical_field.get_highest_counts(header, limit))


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


# @app.route("/api/moe/<pdb>")
# def get_moes(pdb):
#     return jsonify([row.to_map() for row in moe.get_all_by_pdb(pdb)])
#
#
# @app.route("/api/moe/counts")
# def get_counts():
#     # return jsonify(dict(moe.get_hbond_type_counts()))
#     return jsonify([dict(row) for row in moe.get_hbond_type_counts()])
