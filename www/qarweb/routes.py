
from flask import Blueprint, jsonify, render_template
import speedtest

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Home')

@main.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome')

@main.route('/speedtest', methods=['POST'])
def speedtest_endpoint():
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()
    st.download()
    st.upload()
    results = st.results.dict()

    data = {
        'download': results['download'] / 1000,
        'upload': results['upload'] / 1000
    }

    return jsonify(data)
