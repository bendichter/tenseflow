from flask import Flask, render_template, request
from change_tense.change_tense import change_tense
import pdb

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('form.html')

@app.route('/result/', methods=['GET', 'POST'])
def result():
    text = request.form['input_text']
    text_out = change_tense(text, 'future')
    return render_template('result.html', input_text=text, text=text_out)
