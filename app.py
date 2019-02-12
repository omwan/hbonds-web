import os

from bokeh.embed import components
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from hbonds import count_hbonds

UPLOAD_FOLDER = '/Users/olivia/Documents/moe'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
flask_env = os.getenv("FLASK_ENV")

if flask_env == "development":
    app.config.from_object("config.DevelopmentConfig")
elif flask_env == "production":
    app.config.from_object("config.ProductionConfig")


def allowed_file(filename):
    """
    Determine if the uploaded file is of the allowed extension.

    :param filename: name of file to check
    :return: whether or not it is a valid filetype
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        filter_out = request.form.get("filter-out") is not None
        folder, file = get_file()

        output_file = count_hbonds.build_output(folder, file, filter_out)
        scatter_plot = count_hbonds.build_full_scatter(output_file)
        scatter_script, scatter_div = components(scatter_plot)

        means_file = count_hbonds.build_means_output(folder, output_file)
        means_plot = count_hbonds.build_means_scatter(means_file)
        means_script, means_div = components(means_plot)

        graph_name = file.split(".csv")[0]

    return render_template("index.html", name=graph_name,
                           scatter_div=scatter_div, scatter_script=scatter_script,
                           means_div=means_div, means_script=means_script)
