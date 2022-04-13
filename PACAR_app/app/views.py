import datetime
import json

import requests
from flask import render_template, redirect, request, url_for, session, flash

from functools import wraps

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []


def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

app.secret_key = "hello pipo"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
       if 'logged_in' in session:
            return f(*args, **kwargs)
       else:
            flash('You need to login')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():
    fetch_posts()
    return render_template('index.html',
                           title='PACAR: Patient Care App',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')


@app.route('/logoutpage')
def logoutpage():
    return render_template('logoutpage.html')


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in ('admin','Jeff','Hector','Michael') or request.form['password'] != 'admin':
          error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            #flash('You are logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error = error)


@app.route('/logout')
@login_required
def logout():
      session.pop('logged_in', None)
      flash('You were logged out!')
      return redirect(url_for('logoutpage'))