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
    print("schedule")    
    for data in result.result_data:
        print(data)
    
    print("시간별 task/alter")
    for time, task in result.task_dict.items(): 
        print(time, task)
    
    print("시간별 labor 숫자")    
    for time, labor_info in result.num_labor_dict.items():
        print(time, labor_info)

    print("간트차트")
    result.create_gantt("chart.html")




   