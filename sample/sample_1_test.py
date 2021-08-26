## 상위폴더로 옮겨서 실행해야 함

import json
from ss_js.parameters import ModelParams, Params
from ss_js.env.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.result import OptimalResult
import datetime
import plotly as py

dt = datetime.datetime
time_delta = datetime.timedelta
pyplt = py.offline.plot

file_path = "data/data.json"
with open(file_path, 'r') as f:
    json_data = json.load(f)

schedule = Schedule(json_data)
result = OptimalResult(schedule) 

if result.is_optimal:     
    result.optimal_schedule()
    result.set_task_dict()



   