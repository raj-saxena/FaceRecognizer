import subprocess

from bottle import route, run, hook, response, request

from Constants import HOST_IP
from Constants import HOST_PORT


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@route('/train')
def train():
    name = request.query['name']
    output = subprocess.check_output(["python", "Train.py", name])
    return output


@route('/predict')
def predict():
    output = subprocess.check_output(["python", "Predict.py"])
    return output.split('\n')


if __name__ == '__main__':
    run(host=HOST_IP, port=HOST_PORT, debug=True)
