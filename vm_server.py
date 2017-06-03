from flask import Flask, render_template, request, jsonify
import subprocess

from time import sleep, time
from monitor_process import Monitor

import requests
import json

from watcher_params import *
from machine_params import machine_params

app = Flask(__name__)

SERVER_IP = "http://34.253.103.15:8080"
SERVER_PATH = "/returnResult"


# =========================== REST API ========================================

@app.route('/startTask/<taskID>', methods=["POST"])
def index(taskID):
    print request.json

    taskType = request.json["type"]
    taskParams = request.json["taskParams"]

    try:
        monitor = Monitor(taskID, taskType, taskParams)
    except Exception as e:
        response = jsonify({'message': str(e)})
        response.status_code = 400
        return response

    monitor.start()
    return "ok"

    # send start info to Watcher
    # data = {"id": 1, "taskType:" "PI", "taskParams": {"pointsNo": 20000}, "workerParams" : machineParams}
    # print "data to send: " + data
    #
    # watcher_url = WATCHER_IP + WATCHER_START
    # while True:
    #     try:
    #         response = requests.post(watcher_url, data=data)
    #     except requests.exceptions.ConnectionError as e:
    #         print e
    #         sleep(1)
    #         continue
    #     break


@app.route('/task/<taskID>/end', methods=["POST"])
def task_end(taskID):
    print "---\tTASK ENDED: ", taskID
    print "---\t", request.json

    send_res_to_server(taskID, request.json['answer'])

    data = request.json
    del data['answer']
    send_res_to_watcher(data)

    return "ok"


# ======================= sending requests ====================================

def send_res_to_server(taskID, answerData):
    answer = (answerData).replace("'", "").replace("\n", " ").replace("\r", " ")

    data = '{"id":' + taskID + ', "answer":"' + answer + '"}'
    headers = {'content-type': 'application/json'}

    print ">>>\tdata to send: " + data
    server_url = SERVER_IP + SERVER_PATH

    tries = 10
    while tries > 0:
        try:
            response = requests.post(server_url, data=json.dumps(data), headers=headers)
        except requests.exceptions.ConnectionError as e:
            print e

            sleep(10)
            tries -= 1
            continue
        break

def send_res_to_watcher(data):

    # NOTE: data = {'taskType': 'taskType', 'taskParams': {}, 'executeStats' = {}}
    data['workerParams'] = machine_params
    headers = {'content-type': 'application/json'}

    print "@@@\tdata to send: " + str(data)
    server_url = WATCHER_IP + WATCHER_END

    tries = 2
    while tries > 0:
        try:
            response = requests.post(server_url, data=json.dumps(data), headers=headers)
        except requests.exceptions.ConnectionError as e:
            print e

            sleep(10)
            tries -= 1
            continue
        break



if __name__ == "__main__":
    # app.debug = True  # TODO remove before deployment
    app.run(host='0.0.0.0', port=80)
