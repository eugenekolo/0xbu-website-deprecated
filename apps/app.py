from flask import Flask, render_template, request, url_for
from flask.ext.cors import CORS

import requests
import kolobyte
import argparse

app = Flask(__name__)
cors = CORS(app)

@app.route('/subscribe', methods=['POST'])
def index():
    try:
        email = request.form['email']
        data = 'email={}&fullname=&pw=&pw-conf=&digest=0&email-button=Subscribe'.format(email)
        requests.post('http://cs-mailman.bu.edu/mailman/subscribe/builds-list', data=data)
	print("[*] Subscribed {}".format(email))
        return "Success", 200
    except:
        return "Error", 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False,
        help='Enable debugging, default=False')
    parser.add_argument('-x', '--host', default='127.0.0.1',
        help='The host to bind to, default=127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=8001,
        help='The port of the host to bind to, default=8001')
    args = parser.parse_args()

    app.run(debug=args.debug, host=args.host, port=args.port, threaded=True)

