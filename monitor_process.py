import psutil
import subprocess

import os
import threading
from time import sleep, time
import json

import requests

from watcher_params import *
from machine_params import machine_params

TIME_STEP = 1
SERVER_IP = "http://localhost"
SERVER_END = "/task/{}/end"   # SERVER_END.format(taskID)


class Monitor(threading.Thread):

    def __init__(self, taskID, taskType, taskParams):
        threading.Thread.__init__(self)
        self.taskID = taskID

        self.taskType = taskType
        self.taskParams = taskParams

        # np. ["python2.7", "monte_carlo.py", "" + str(pointsNo)]
        self.task_array = self._createTask(taskType, taskParams)


        # create process output file
        filename = "./outputs/{}".format(taskID)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        self.output = open(filename, "w")

    def run(self):
        pid = self._run_task()

        p = psutil.Process(pid)
        while psutil.pid_exists(pid) and p.status() != "zombie":
            try:

                sys_info = {}

                proc_info = p.as_dict(attrs=[
                    'cpu_percent',
                    'cpu_times',
                    'status',
                    'num_threads',
                    'memory_full_info',
                    'io_counters'
                ])
                proc_info['cpu_times'] = dict(proc_info['cpu_times']._asdict())
                proc_info['memory_full_info'] = dict(proc_info['memory_full_info']._asdict())
                proc_info['io_counters'] = dict(proc_info['io_counters']._asdict())

                proc_info['id'] = self.taskID
                proc_info['timestamp'] = time()

                # add task info

            except Exception as e:
                print "Process probably exited.", e
                break

            # self._send_proc_info(proc_info)  # send to watcher
            sleep(TIME_STEP)

        self.output.close()
        self._send_end_info()


    def _run_task(self):
        p = subprocess.Popen(self.task_array, stdout=self.output)
        return p.pid

    def _send_proc_info(self, proc_info):
        print proc_info
        print

        watcher_url = WATCHER_IP + WATCHER_STEP
        try:
            response = requests.post(watcher_url, data=proc_info)
        except requests.exceptions.ConnectionError as e:
            print e
            # TODO: store proc_info for later post


    def _send_end_info(self):
        server_url = SERVER_IP + SERVER_END.format(self.taskID)

        filename = "./outputs/{}".format(self.taskID)
        self.output = open(filename, "r")
        answer = self.output.read()
        self.output.close()

        data = {}
        data['answer'] = answer
        data['taskType'] = self.taskType
        data['taskParams'] = self.taskParams
        data['executeStats'] = {}

        headers = {'content-type': 'application/json'}

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

    def _createTask(self, taskType, taskParams):

        task = []
        if taskType == "PI":
            # task.append("python2.7")
            # task.append("monte_carlo.py")
            # try:
            #     task.append(str(taskParams["pointsNo"]))
            # except:
            #     raise Exception("Wrong task parameters!")

            task.append("/usr/local/bin/mpiexec")
            task.append("-np")
            task.append(str(machine_params['CPUs']))
            task.append("./pi")
            try:
                task.append(str(taskParams[0]))
            except:
                raise Exception("Wrong task parameters!")

        elif taskType == "memtest":
            task.append("memtest")
            # TODO:...
            task.append("--help")

        elif taskType == "dd":
            task.append("dd")
            # TODO:...
            task.append("--help")
        else:
            raise Exception("Wrong task!")

        print task
        return task

if __name__ == '__main__':
    taskID = 1
    task = ["python2.7", "monte_carlo.py", "" + str(20000)]

    monitor = Monitor(taskID, task)
    monitor.start()
