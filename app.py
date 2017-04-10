from flask import Flask, render_template, request
from change_tense.change_tense import change_tense
from rq import Queue
from rq.job import Job
from worker import conn
import time

app = Flask(__name__)

q = Queue(connection=conn)


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('form.html', text_in='', text_out='', tense='past')


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if 'input_text' in request.form:
        text_in = request.form['input_text']
    else:
        text_in = ''
    try:
        job = q.enqueue_call(
            func=change_tense, args=(text_in, request.form['tense']), result_ttl=5000
        )
        while not job.is_finished:
            time.sleep(.1)
        text_out = str(job.result)
    except:
        text_out = 'ERROR!!!!!!'
    return render_template('form.html', text_in=text_in, text_out=text_out, tense=request.form['tense'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202
