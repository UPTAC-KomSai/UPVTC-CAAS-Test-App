from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response

import requests


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    name = request.cookies.get('name')
    return render_template('index.html', name=name)


@app.route('/auth/caas/callback/', strict_slashes=False)
def auth_callback():
    service_ticket = request.args.get('serviceTicket')
    redirect_url = request.args.get('redirect_url')

    # Do some logic here.

    r = requests.get('http://192.168.15.3.xip.io:3000/auth/verifyTicket?ticket=' + service_ticket)
    response = r.json()

    return_response = make_response(redirect(redirect_url))
    if 'status' not in response:
        # No errors.
        return_response.set_cookie('name', response['name'])

    return return_response


@app.route('/auth/caas/logout/', strict_slashes=False)
def logout_callback():
    resp = make_response(redirect('http://192.168.15.3.xip.io:3000/signout'))
    resp.set_cookie('name', '', max_age=0)

    return resp


if __name__ == '__main__':
    app.run()
