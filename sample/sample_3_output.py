import json
from ss_js.parameters import ModelParams, Params
from ss_js.schedule.schedule import Schedule
from ortools.sat.python import cp_model
from ss_js.optimize.optimizer import OptimizerCallback
from ss_js import io
import datetime
import plotly as py
from ss_js.optimize import chart
import random

pyplt = py.offline.plot
file_path = "data/generated.json"

with open(file_path, 'r', encoding="utf-8") as f:
    json_data = json.load(f)

schedule = Schedule(json_data)

result_path = "experiment/solution0_tasklist.json"
chart.create_gantt(result_path, "experiment", schedule)
# excel
json_tasklist_path = "experiment/solution0_tasklist.json"
excel_tasklist_path = "experiment/solution0_tasklist.xlsx"
chart.task_list_to_excel(json_tasklist_path, excel_tasklist_path)

json_labortime_path = "experiment/solution0_labortime.json"
excel_labortime_path = "experiment/solution0_labortime.xlsx"
chart.labor_time_to_excel(json_labortime_path, excel_labortime_path)




