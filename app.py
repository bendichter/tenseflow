from flask import Flask, render_template, request
from tenseflow.database import db_session
from tenseflow.models import Answer


from tenseflow import change_tense

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('form.html', text_in='', text_out='', tense='past')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    print(list(request.form.iteritems()))
    if 'input_text' in request.form:
        text_in = request.form['input_text']
        tense = request.form['tense']
    else:
        text_in = ''
        tense = ''

    try:
        text_out = change_tense(text_in, request.form['tense'])
    except:
        text_out = 'ERROR!!!!!!'

    if 'correction' in request.form:
        correction = request.form['correction']
    else:
        correction = ''

    if 'errortick' in request.form:
        incorrect = request.form['errortick']
    else:
        incorrect = False

    db_session.add(Answer(text_in, tense, text_out, incorrect=incorrect, correction=correction))
    db_session.commit()

    return render_template('form.html', text_in=text_in, text_out=text_out, tense=request.form['tense'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
