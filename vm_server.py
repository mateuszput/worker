from flask import Flask, render_template, request
import subprocess

from time import sleep, time
from monitor_process import Monitor

import requests

app = Flask(__name__)

SERVER_IP = "http://34.253.103.15"
SERVER_END = "/returnResult"

@app.route('/startTask/<taskID>', methods=["POST"])
def index(taskID):
    subprocess.call(["echo", "Hello World! " + taskID])

    # zwracamy odpowiedz http, bez czekania na wynik:
    # subprocess.Popen(["python2.7", "monte_carlo.py", "" + taskID])
    task = ["python2.7", "monte_carlo.py", "" + str(taskID)]

    monitor = Monitor(taskID, task)
    monitor.start()
    print "--> when it is called?"


    return "test"

@app.route('/task/<taskID>/end', methods=["POST"])
def task_end(taskID):
    print "TASK ENDED!!!"
    print taskID
    print request.data
    data = "{\"id\":" + taskID + "," + "\"answer\": \"" + request.data + "\"}"
    server_url = SERVER_IP + SERVER_END
    while True:
        try:
            response = requests.post(server_url, data=data)
        except requests.exceptions.ConnectionError as e:
            print e

            sleep(1)
            continue
        break

    return "test"


# @app.route("/<username>", methods=["GET"])
# def hello_world(username):
#     return render_template('hello_world.html', username=username)




if __name__ == "__main__":
    # app.debug = True  # TODO remove before deployment
    # app.run(host='0.0.0.0', port=50123)
    app.run(host='0.0.0.0', port=80)
