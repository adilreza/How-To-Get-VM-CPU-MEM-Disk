from flask import Flask
from flask import jsonify
from flask.wrappers import Response
from psutil import cpu_percent
import json
import worker
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'welcome to resource ' + worker.mytestfun() +" testing ping"

@app.route('/name/<boss>')
def hello_guest(boss):
   return 'Hello %s as devops' % boss

@app.route("/get_json")
def summary():
    return jsonify (
        data1 = "data1",
        data2 = "this is data2",
        
    )
@app.route("/get-cpu-memory-hdd")
def cpumemhdd():
    data_list = [
        {
            "cpu_core_count":worker.core_count(),"cpu_used_percent":worker.cpu_percentage(),
            "ram_in_total":worker.total_in_mb(),"ram_used_percent":worker.memory_use_percentage(),
            "ram_used_MB": worker.used_in_mb(),
            "total_disk_in_GB":worker.total_disk(),
            "used_disk_in_GB":worker.total_usage(),
            "Free_disk_in_GB":worker.total_free(),
        }
    ]
    return Response(json.dumps(data_list), mimetype="application/json")




app.debug = True

# run the app 
if __name__ == '__main__':
    # app.run(host, port, debug, options)

   app.run()