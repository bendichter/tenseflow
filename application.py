from flask import Flask, render_template, request
from change_tense.change_tense import change_tense

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('form.html', text_in='enter text here', text_out='', tense='past')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if 'input_text' in request.form:
        text_in = request.form['input_text']
    else:
        text_in = ''
    text_out = change_tense(text_in, request.form['tense'])
    return render_template('form.html', text_in=text_in, text_out=text_out, tense=request.form['tense'])
