from flask import Flask, render_template, request
import subprocess

app = Flask(__name__, template_folder='templates')


@app.route('/startTask/<taskID>', methods=["GET"])
def index(taskID):
    subprocess.call(["echo", "Hello World! " + taskID])

    # zwracamy odpowiedz http, bez czekania na wynik:
    subprocess.Popen(["python2.7", "monte_carlo.py", "" + taskID])
    print "--> when it is called?"
    return "test"


# @app.route("/<username>", methods=["GET"])
# def hello_world(username):
#     return render_template('hello_world.html', username=username)




if __name__ == "__main__":
    # app.debug = True  # TODO remove before deployment
    app.run(host='0.0.0.0', port=50123)
