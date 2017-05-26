import psutil
import subprocess
from time import sleep
import os

TIME_STEP = 1
WATCHER_IP = "0.0.0.0"
WATCHER_STEP = "/proc/step"
WATCHER_START = "/proc/start"
WATCHER_END = "/proc/end"

SERVER_IP = "localhost"
SERVER_END = "/task/{}/end"   # SERVER_END.format(taskID)



class Monitor():

    def __init__(self, taskID, task_array):
        self.taskID = taskID
        self.task_array = task_array

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
        # p.status() != "zombie"  <--- czy dobre?!?!?!
        while psutil.pid_exists(pid) and p.status() != "zombie":
            try:
                proc_info = p.as_dict(attrs=[
                    'cpu_percent',
                    'cpu_times',
                    'status',
                    'num_threads',
                    'memory_full_info'
                ])
                proc_info['cpu_times'] = dict(proc_info['cpu_times']._asdict())
                proc_info['memory_full_info'] = dict(proc_info['memory_full_info']._asdict())

                # add task info

            except:
                break
                print "Process probably exited"

            self._send_proc_info(proc_info)
            sleep(TIME_STEP)

        # get here result from self.output ?

    def _run_task(self):
        p = subprocess.Popen(self.task_array, stdout=self.output)
        return p.pid

    def _send_start_info(self, proc_info):
        pass
        # send REST to Watcher
        # NOTE: probably it should be done from WorkerServer. Because of the task parameters

    def _send_proc_info(self, proc_info):
        print proc_info
        # send REST to Watcher

    def _send_end_info(self, proc_info):
        pass
        # send REST to WorkerServer(?)



if __name__ == '__main__':
    taskID = 1
    task = ["python2.7", "monte_carlo.py", "" + str(taskID)]

    monitor = Monitor(taskID, task)
    monitor.run()
