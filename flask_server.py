from flask import Flask, flash, jsonify, render_template, request
from query_main import start_query
app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query_text = request.form['query_text']
    result_list = start_query(query_text)

    return render_template('display_results.html', result_list=result_list)