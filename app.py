import os

from bokeh.embed import components
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from hbonds import count_hbonds

UPLOAD_FOLDER = '/Users/olivia/Documents/moe'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return app.config["UPLOAD_FOLDER"], filename


@app.route("/", methods=["GET", "POST"])
def chart():
    scatter_div = ""
    scatter_script = ""

    means_div = ""
    means_script = ""

    if request.method == "POST":
        filter_out = request.form.get("filter-out") is None
        folder, file = get_file()

        output_file = count_hbonds.build_output(folder, file, filter_out)
        scatter_plot = count_hbonds.build_full_scatter(output_file)
        scatter_script, scatter_div = components(scatter_plot)

        means_file = count_hbonds.build_means_output(folder, output_file)
        # print(means_file)
        means_plot = count_hbonds.build_means_scatter(means_file)
        means_script, means_div = components(means_plot)

    return render_template("index.html",
                           scatter_div=scatter_div, scatter_script=scatter_script,
                           means_div=means_div, means_script=means_script)
