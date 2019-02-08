from bokeh.embed import components

from hbonds import count_hbonds

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/olivia/Documents/moe'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def chart():
    fields = count_hbonds.MOE_HEADERS

    if request.method == "POST":
        print(request.files)

    plot = count_hbonds.build_graph()
    script, div = components(plot)

    return render_template("index.html",
                           div=div, script=script, fields=fields)
