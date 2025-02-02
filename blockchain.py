# Python module imports
import datetime as dt
import hashlib
import webbrowser
from flask import Flask, request, render_template, Response
from threading import Timer
from datetime import datetime
import os

# Importing local functions and classes
from block import *
from genesis import create_genesis_block
from newBlock import next_block, add_block
from getBlock import find_records
from checkChain import check_integrity
from smartpy_functions import *

# Flask declarations
app = Flask(__name__)
response = Response()
response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

# Initializing blockchain with the genesis block
blockchain = create_genesis_block()
data = []

# Function to display all blocks of the blockchain
def display_blocks(blockchain):
    blocks_info = []
    for block in blockchain:
        block_info = {
            "Index": block.index,
            "Timestamp": block.timestamp,
            "Data": block.data,
            "Previous Hash": block.previous_hash,
            "Hash": block.hash
        }
        blocks_info.append(block_info)
    return blocks_info

@app.route('/',  methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def parse_request():
    if request.form.get("name"):
        while len(data) > 0:
            data.pop()
        data.append(request.form.get("name"))
        data.append(str(dt.date.today()))
        return render_template("class.html",
                             name=request.form.get("name"),
                             date=dt.date.today())

    elif request.form.get("number"):
        while len(data) > 2:
            data.pop()
        data.append(request.form.get("course"))
        data.append(request.form.get("year"))
        return render_template("attendance.html",
                             name=data[0],
                             course=request.form.get("course"),
                             year=request.form.get("year"),
                             number=int(request.form.get("number")))
    elif request.form.get("roll_no1"):
        while len(data) > 4:
            data.pop()
        return render_template("result.html", 
                             result=add_block(request.form, data, blockchain),
                             datetime=datetime)
    else:
        return "Invalid POST request. This incident has been recorded."

@app.route('/view.html',  methods=['GET'])
def view():
    return render_template("search_records.html")

@app.route('/view.html',  methods=['POST'])
def show_records():
    try:
        data = find_records(request.form, blockchain)
        if data == -1:
            return render_template("result.html", 
                                result="No records found for the given criteria",
                                datetime=datetime)
        return render_template("view.html",
                            name=request.form.get("name"),
                            course=request.form.get("course"),
                            year=request.form.get("year"),
                            status=data,
                            number=int(request.form.get("number")),
                            date=request.form.get("date"))
    except Exception as e:
        return render_template("result.html", 
                            result=f"Error retrieving records: {str(e)}",
                            datetime=datetime)

@app.route('/result.html',  methods=['GET'])
def check():
    return render_template("result.html", 
                         result=check_integrity(blockchain),
                         datetime=datetime)

def open_browser():
    webbrowser.open_new('http://localhost:5000/')

if __name__ == "__main__":
    app.debug = True
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        Timer(1.5, open_browser).start()
    app.run(host='localhost', port=5000)
