import random

import flask
from flask import Flask
import socket as sck
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO, StringIO

app = Flask(__name__)
internalIP = sck.gethostbyname(sck.gethostname())
externalIP = sck.gethostbyname(sck.getfqdn())
PORT = 11666

@app.route('/')
@app.route('/<int:num>')
def calc(num = None):
    return flask.render_template('button.html', num=num)

@app.route('/calculate', methods=['POST'])
def calculate():
    if flask.request.method == 'POST':
        temp = flask.request.form['num']
    else:
        temp = None
    return flask.redirect(flask.url_for('calc', num=int(temp)**2))

@app.route('/next', methods=['POST'])
def next_click():
    if flask.request.method == 'POST':
        return flask.render_template('Click.html')

@app.route('/graph', methods=['POST'])
def next_graph(mean = 0, var = 0):
    if flask.request.method == 'POST':
        return flask.render_template('Graph.html',mean = int(random.random()*100), var = int(random.random()*10))

@app.route('/fig/<int:mean>_<int:var>')
def fig(mean, var):
  plt.figure(figsize=(4, 3))
  xs = np.random.normal(mean, var, 100)
  ys = np.random.normal(mean, var, 100)
  plt.scatter(xs, ys, s=100, marker='h', color='red', alpha=0.3)
  """
  file로 저장하는 것이 아니라 binary object에 저장해서 그대로 file을 넘겨준다고 생각하면 됨
  """
  img = BytesIO()
  plt.savefig(img, format='png', dpi=300)
  img.seek(0)## object를 읽었기 때문에 처음으로 돌아가줌

  return flask.send_file(img, mimetype='image/png')
  # plt.savefig(img, format='svg')
  # return send_file(img, mimetype='image/svg')

@app.route('/user/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'

if __name__ == '__main__':
    app.run(internalIP, PORT, threaded = False, debug = True)