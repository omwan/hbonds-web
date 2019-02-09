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
    fields = count_hbonds.MOE_HEADERS

    if request.method == "POST":
        folder, file = get_file()
        output_file = count_hbonds.build_output(folder, file)
        plot = count_hbonds.build_graph(output_file)
        script, div = components(plot)
    else:
        div = ""
        script = ""

    return render_template("index.html", div=div, script=script, fields=fields)
